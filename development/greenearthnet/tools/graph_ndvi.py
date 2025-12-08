import os
import xml.etree.ElementTree as ET
import xarray as xr
import numpy as np
import rasterio
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image


def colormap_from_qgis(qml_path, cmap_name="qgis_ndvi"):
    tree = ET.parse(qml_path)
    root = tree.getroot()

    shader = root.find(".//colorrampshader")
    if shader is None:
        raise ValueError("No <colorrampshader> found in QML.")

    stops = []
    for item in shader.findall("item"):
        value = float(item.get("value"))
        color = item.get("color")
        r = int(color[1:3], 16) / 255
        g = int(color[3:5], 16) / 255
        b = int(color[5:7], 16) / 255
        stops.append((value, (r, g, b)))

    if not stops:
        raise ValueError("QML found but contains no <item> entries.")

    vmin = min(v for v, _ in stops)
    vmax = max(v for v, _ in stops)

    # Normalize values to 0–1 range
    norm_stops = [((v - vmin) / (vmax - vmin), c) for v, c in stops]
    positions = [p for p, _ in norm_stops]
    colors = [c for _, c in norm_stops]

    cmap = LinearSegmentedColormap.from_list(cmap_name, list(zip(positions, colors)))
    return cmap, vmin, vmax


def apply_qgis_style_to_png(tiff_in, png_out, qml_file="C:/Users/dozhang/Documents/GitHub/greenearthnet/development/greenearthnet/qgis/gradient.qml"):
    # Load QGIS colormap
    cmap, vmin, vmax = colormap_from_qgis(qml_file)

    # Read NDVI raster
    with rasterio.open(tiff_in) as src:
        ndvi = src.read(1).astype(float)
        profile = src.profile

    # Handle nodata
    if "nodata" in profile and profile["nodata"] is not None:
        nodata_mask = ndvi == profile["nodata"]
    else:
        nodata_mask = np.isnan(ndvi)

    # Normalize NDVI to 0–1
    ndvi_norm = (ndvi - vmin) / (vmax - vmin)
    ndvi_norm = np.clip(ndvi_norm, 0, 1)

    # Apply colormap (returns float RGBA)
    rgba = cmap(ndvi_norm)
    rgba = (rgba * 255).astype(np.uint8)

    # Make nodata transparent
    rgba[nodata_mask, 3] = 0

    # Convert to PIL image and save
    img = Image.fromarray(rgba, mode="RGBA")
    img.save(png_out)

    print(f"Saved colored image → {png_out}")

def convert_minicube_to_tiff(nc_file, out_dir):
    filename = nc_file.replace("\\", "/").split("/")[-1].replace(".nc", "")
    if out_dir[1] != '/':
        out_dir = out_dir + '/'

    ds = xr.open_dataset(nc_file).rename({"lat": "y", "lon": "x"})
    ds = ds.rio.write_crs("EPSG:4326") 
    timestep = ds.time.min().values
    if ds.sizes["time"] == 150:
        end = ds.sizes["time"]//5
    elif ds.sizes["time"] == 20:
        end = 20
    for i in range(end):
        band = ds.sel(time=timestep)
        band = band.rio.to_raster(f"{out_dir}{filename}_{i+1}.tiff")
        timestep = timestep + np.timedelta64(5, 'D')


    print(f"Converted {nc_file} to tiff files")
    return

def predictions_to_tiff(base_dir, output_root):
    out_dir = ""

    for i in range(26):
        out_dir = f"{output_root}/{i*10}-{(i*10)+9}"
        os.makedirs(out_dir, exist_ok=True)

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".nc"):
                nc_path = os.path.join(root, file)
                name = os.path.splitext(file)[0]
                i = int(name.split("_")[1])//10
                out_dir = f"{output_root}/{i*10}-{(i*10)+9}/"
                print(f"Processing {file} -> {out_dir}")
                convert_minicube_to_tiff(nc_path, out_dir)

def predictions_to_coloured_tiff(input_tiff, base_dir="", output_root=""):
    out_dir = ""

    # for i in range(26):
    #     out_dir = f"{output_root}/{i*10}-{(i*10)+9}"
    #     os.makedirs(out_dir, exist_ok=True)

    # for root, dirs, files in os.walk(base_dir):
    #     for file in files:
    #         if file.endswith(".tiff"):
    #             nc_path = os.path.join(root, file)
    #             name = os.path.splitext(file)[0]
    #             i = int(name.split("_")[1])//10
    #             out_dir = f"{output_root}/{i*10}-{(i*10)+9}/"
    #             print(f"Processing {file} -> {out_dir}")
    #             apply_qgis_style_to_png(file, out_dir)



if __name__ == "__main__":
    pass
    # path = r"C:\Users\dozhang\Downloads\offset\ood-t_chopped\MJJ_minicube_120_32UNC_51.65_10.40.nc"
    # name = path.split("\\")[-1].split(".nc")[0]
    # dir = "C:\\Users\\dozhang\\Downloads\\offset\\"
    # convert_minicube_to_tiff(path, dir)
    # for i in range(30):
    #     apply_qgis_style_to_png(f"{dir}{name}_{i+1}.tiff", f"{dir}c{i+1}.tiff")
    
    

    # base_dir = ""
    # output_root =""
    
    # out_dir = ""
    # for i in range(26):
    #     out_dir = f"{output_root}/{i*10}-{(i*10)+9}"
    #     os.makedirs(out_dir, exist_ok=True)

    # for root, dirs, files in os.walk(base_dir):
    #     for file in files:
    #         if file.endswith(".tiff"):
    #             nc_path = os.path.join(root, file)
    #             name = os.path.splitext(file)[0]
    #             i = int(name.split("_")[1])//10
    #             out_dir = f"{output_root}/{i*10}-{(i*10)+9}/"
    #             print(f"Processing {file} -> {out_dir}")
    #             convert_minicube_to_tiff(nc_path, out_dir)
    # apply_qgis_style_to_png()
