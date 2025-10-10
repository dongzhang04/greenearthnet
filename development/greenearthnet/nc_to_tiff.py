import xarray as xr
import rioxarray as rioxr
import numpy as np

def convert_nc_to_tiff(nc_file, out_dir):
    # Load the NetCDF file using xarray
    filename = nc_file.split("/")[-1].replace(".nc", "")
    if out_dir[1] != '/':
        out_dir = out_dir + '/'

    ds = xr.open_dataset(nc_file).rename({"lat": "y", "lon": "x"})
    timestep = ds.time.min().values

    for i in range(ds.sizes["time"]):
        ndvi = ds.sel(time=timestep)
        ndvi = ndvi.rio.write_crs("EPSG:4326") 
        ndvi = ndvi.rio.to_raster(f"{out_dir}{filename}_{i+1}.tiff")
        timestep = timestep + np.timedelta64(5, 'D')


    print(f"Converted {nc_file} to tiff file")
    return