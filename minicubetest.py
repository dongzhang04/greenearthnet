import earthnet_minicuber as emc
import pystac_client

# pc = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
# search = pc.search(
#     collections=["sentinel-2-l2a"],
#     datetime="2018-01-01/2024-12-31",
#     intersects={
#         "type": "Point",
#         "coordinates": [3.087414, 43.598946]  # lon, lat
#     },
# )
# items = list(search.get_items())
# print(len(items))

specs = {
    "lon_lat": (43.598946, 3.087414),  # center pixel
    "xy_shape": (128, 128),  # width, height of cutout around center pixel
    "resolution": 20,  # in meters.. will use this together with grid of primary provider..
    "time_interval": "2018-01-01/2024-12-31",
    "providers": [
        {
            "name": "s2",
            "kwargs": {
                "bands": ["B02", "B03", "B04", "B8A", "SCL"],  # , "B09", "B11", "B12"],
                "best_orbit_filter": False,
                "five_daily_filter": True,
                "brdf_correction": False,
                "cloud_mask": True,
                "cloud_mask_rescale_factor": 2,
                "aws_bucket": "planetary_computer",
            },
        },
        {"name": "srtm", "kwargs": {"bands": ["dem"]}},
        {"name": "alos", "kwargs": {}},
        {"name": "cop", "kwargs": {}},
        {
            "name": "esawc",
            "kwargs": {"bands": ["lc"], "aws_bucket": "planetary_computer"},
        },
        # {
        #     "name": "geom",
        #     "kwargs": {"filepath": "downloads/Geomorphons/geom/geom_90M_africa_europe.tif"}
        # }
        # Also Missing here: EOBS v26 https://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php#datafiles
    ],
}

mc = emc.load_minicube(specs, compute = True)
print("finished")