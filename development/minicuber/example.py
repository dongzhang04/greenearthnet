import earthnet_minicuber as emc
import matplotlib.pyplot as plt

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
            "name": "era5",
            "kwargs": {"bands": ['t2m', 'pev', 'slhf', 'ssr', 'sp', 'sshf', 'e', 'tp'], "aggregation_types": ["mean", "min", "max"], "zarrurl": "https://storage.de.cloud.ovh.net/v1/AUTH_84d6da8e37fe4bb5aea18902da8c1170/uc1-africa/era5_africa_0d1_3hourly.zarr"}
        }
        ]
}

# greenearthnet example
# specs = {
#     "lon_lat": (43.598946, 3.087414),  # center pixel
#     "xy_shape": (128, 128),  # width, height of cutout around center pixel
#     "resolution": 20,  # in meters.. will use this together with grid of primary provider..
#     "time_interval": "2024-07-01/2024-08-31",
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
#         # {"name": "srtm", "kwargs": {"bands": ["dem"]}},
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
