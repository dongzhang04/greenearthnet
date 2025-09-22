import earthnet_minicuber as emc
import matplotlib.pyplot as plt

import fsspec, xarray as xr

# print("single level reanalysis zarr")
# url = "gs://gcp-public-data-arco-era5/co/single-level-reanalysis.zarr"
# ds = xr.open_zarr(fsspec.get_mapper(url), consolidated=True)
# print(list(ds.data_vars.keys()))

# url = "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"
# mapper = fsspec.get_mapper(url)
# ds_full = xr.open_zarr(mapper, consolidated=True)
# print(list(ds_full.data_vars.keys()))

# minicuber example
specs = {
    ## Locations of interest
    # "lon_lat": (43.598946, 3.087414), # Baidoa
    # "lon_lat": (9.920089, 2.936115), # Kribi
    "lon_lat": (43.598946, 3.087414), # center pixel
    "xy_shape": (256, 256), # width, height of cutout around center pixel
    "resolution": 10, # in meters.. will use this on a local UTM grid..
    "time_interval": "2021-01-01/2021-01-31",
    "providers": [
        {
            "name": "s2",
            "kwargs": {"bands": ["B02", "B03", "B04", "B8A"], "best_orbit_filter": True, "five_daily_filter": False, "brdf_correction": True, "cloud_mask": True, "aws_bucket": "planetary_computer"}
        },

        # stackstac band size issue
        # {
        #     "name": "s1",
        #     "kwargs": {"bands": ["vv", "vh"], "speckle_filter": True, "speckle_filter_kwargs": {"type": "lee", "size": 9}, "aws_bucket": "planetary_computer"} 
        # },

        # SSL certificate error - possibly due to firewall
        # {
        #     "name": "ndviclim",
        #     "kwargs": {"bands": ["mean", "std"]}
        # },
        {
            "name": "cop",
            "kwargs": {}
        },
        {
            "name": "esawc",
            "kwargs": {"bands": ["lc"], "aws_bucket": "planetary_computer"}
        },

        # "This server could not verify that you are authorized to access the document you requested." 
        {
            "name": "era5gcp",
            "kwargs": {"bands": ['t2m', 'pev', 'slhf', 'ssr', 'sp', 'sshf', 'e', 'tp'], "aggregation_types": ["mean", "min", "max"], "zarrurl": "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"}
        }
        ]
}

# greenearthnet example
# specs = {
#     "lon_lat": (43.598946, 3.087414),  # center pixel
#     "xy_shape": (128, 128),  # width, height of cutout around center pixel
#     "resolution": 20,  # in meters.. will use this together with grid of primary provider..
#     "time_interval": "2024-05-01/2024-08-31",
#     "providers": [
#         {
#             "name": "s2",
#             "kwargs": {
#                 "bands": ["B02", "B03", "B04", "B8A", "SCL"],  # , "B09", "B11", "B12"],
#                 "best_orbit_filter": True,
#                 "five_daily_filter": False,
#                 "brdf_correction": True,
#                 "cloud_mask": True,
#                 "cloud_mask_rescale_factor": 2,
#                 "aws_bucket": "planetary_computer",
#             },
#         },

#         # SSL certificate error - possibly due to firewall
#         {"name": "srtm", "kwargs": {"bands": ["dem"]}},
#         {"name": "alos", "kwargs": {}},
#         {"name": "cop", "kwargs": {}},
#         {
#             "name": "esawc",
#             "kwargs": {"bands": ["lc"], "aws_bucket": "planetary_computer"},
#         },
#         # {
#         #     "name": "geom",
#         #     "kwargs": {"filepath": "downloads/Geomorphons/geom/geom_90M_africa_europe.tif"}
#         # }
#         # Also Missing here: EOBS v26 https://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php#datafiles
#     ],
# }



mc = emc.load_minicube(specs, compute = True)
print("finished loading minicube")
print("plotting mc")

plot = emc.plot_rgb(mc)
plt.show() 
print("finished")
