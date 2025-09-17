environment setup:
conda create -n minicuber python=3.10 gdal cartopy -c conda-forge
conda activate minicuber
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install scipy matplotlib seaborn netCDF4 xarray zarr dask shapely pillow pandas s3fs fsspec boto3 psycopg2 pystac-client stackstac==0.4.4 planetary-computer rasterio[s3] rioxarray odc-algo segmentation-models-pytorch folium ipykernel ipywidgets sen2nbar
pip install earthnet-minicuber


changes to scripts:
(earthnet-minicuber/providers/ - all scripts requiring epsg)
            if "proj:epsg" in metadata:
                epsg = metadata["proj:epsg"]
            else:
                epsg = metadata["proj:code"].split(":")[-1]
                epsg = int(epsg)


(earthnet-minicuber/providers/esawc)
            stack = stack.sel(band="map").expand_dims("band")
            stack = stack.assign_coords(band=["lc"])

(sen2nbar/c_factor) 
    if "proj:epsg" in item.properties:
        SOURCE_EPSG = item.properties["proj:epsg"]
    else:
        SOURCE_EPSG = int(item.properties["proj:code"].split(":")[-1])