import xarray as xr
import rioxarray as rioxr
import numpy as np

def convert_minicube_to_tiff(nc_file, out_dir):
    filename = nc_file.split("/")[-1].replace(".nc", "")
    if out_dir[1] != '/':
        out_dir = out_dir + '/'

    ds = xr.open_dataset(nc_file).rename({"lat": "y", "lon": "x"})
    ds = ds.rio.write_crs("EPSG:4326") 
    timestep = ds.time.min().values

    for i in range(ds.sizes["time"]):
        band = ds.sel(time=timestep)
        band = band.rio.to_raster(f"{out_dir}{filename}_{i+1}.tiff")
        timestep = timestep + np.timedelta64(5, 'D')


    print(f"Converted {nc_file} to tiff files")
    return

def calculate_minicube_ndvi(nc_file, out_dir):
    filename = nc_file.split("/")[-1].replace(".nc", "")
    if out_dir[1] != '/':
        out_dir = out_dir + '/'

    ds = xr.open_dataset(nc_file).rename({"lat": "y", "lon": "x"})
    ds = ds.rio.write_crs("EPSG:4326") 
    timestep = ds.time.min().values

    for i in range(ds.sizes["time"]):
        bands = ds.sel(time=timestep)
        # if(bands.nir)
        ndvi = (bands.nir - bands.red) / (bands.nir + bands.red)
        ndvi = ndvi.rio.to_raster(f"{out_dir}{filename}_{i+1}.tiff")
        timestep = timestep + np.timedelta64(5, 'D')
    return


def calculate_prediction_fcover(nc_file, out_dir):
    filename = nc_file.split("/")[-1].replace(".nc", "")
    if out_dir[1] != '/':
        out_dir = out_dir + '/'

    ds = xr.open_dataset(nc_file)
    ndvi = ds["ndvi_pred"]
    ndvi_min = ndvi.min(dim=["lat", "lon"])
    ndvi_max = ndvi.max(dim=["lat", "lon"])

    fcover = (ndvi - ndvi_min) / (ndvi_max - ndvi_min)
    fcover = fcover.clip(0, 1)
    fcover.name = "fcover_pred"

    fcover_ds = fcover.to_dataset()

    fcover_ds.to_netcdf(f"{out_dir}{filename}_fcover.nc")

    return
