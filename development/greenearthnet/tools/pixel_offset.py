import earthnet_minicuber as emc
import xarray as xr
import numpy as np

def generate_minicube(specs = None):
    if specs is None:
        data = ['TG', 'TN', 'TX', 'RR', 'PP', 'HU', 'FG', 'QQ']
        paths = ["C:/Users/dozhang/Downloads/tg_ens_mean_0.1deg_reg_v26.0e.nc", 
                "C:/Users/dozhang/Downloads/tn_ens_mean_0.1deg_reg_v26.0e.nc",
                "C:/Users/dozhang/Downloads/tx_ens_mean_0.1deg_reg_v26.0e.nc",
                "C:/Users/dozhang/Downloads/rr_ens_mean_0.1deg_reg_v26.0e.nc",
                "C:/Users/dozhang/Downloads/pp_ens_mean_0.1deg_reg_v26.0e.nc",
                "C:/Users/dozhang/Downloads/hu_ens_mean_0.1deg_reg_v26.0e.nc",
                "C:/Users/dozhang/Downloads/fg_ens_mean_0.1deg_reg_v26.0e.nc",
                "C:/Users/dozhang/Downloads/qq_ens_mean_0.1deg_reg_v26.0e.nc"]
        bands_dict = dict(zip(data, paths))
        specs = {
            "lon_lat": (-8.56, 39.29), # center pixel
            "xy_shape": (130, 130), # width, height of cutout around center pixel
            "resolution": 20, # in meters.. will use this on a local UTM grid..
            "time_interval": "2021-05-10/2021-10-06",
            "providers": [
                {
                    "name": "s2",
                    "kwargs": {
                        "bands": ["B02", "B03", "B04", "B8A", "SCL"],  # , "B09", "B11", "B12"],
                        "best_orbit_filter": True,
                        "five_daily_filter": False,
                        "brdf_correction": True,
                        "cloud_mask": True,
                        "cloud_mask_rescale_factor": 2,
                        "aws_bucket": "planetary_computer",
                    },
                },

                    # RasterioIOError('CURL error: schannel: CertGetCertificateChain trust error CERT_TRUST_IS_UNTRUSTED_ROOT')
                    # {"name": "srtm", "kwargs": {"bands": ["dem"]}},
                    
                    {"name": "nasa", "kwargs": {}},
                    {"name": "alos", "kwargs": {}},
                    {"name": "cop", "kwargs": {}},
                {
                    "name": "esawc",
                    "kwargs": {"bands": ["lc"], "aws_bucket": "planetary_computer"},
                },
                {
                    "name": "geom",
                    "kwargs": {"filepath": "C:/Users/dozhang/Downloads/geom_90M_n35w010.tif"}
                },
                {
                    "name": "eobs",
                    "kwargs": {"bands": bands_dict}
                }
            ],
        }
    minicube = emc.load_minicube(specs, compute = True)
    return minicube


def generate_pixel_offset(lat, lon, output_path):
    if output_path[-1] != '/':
        output_path = output_path + '/'

    minicube = generate_minicube()
    north = minicube.isel(y=slice(0,-2), x=slice(1,-1))
    south = minicube.isel(y=slice(2, None), x=slice(1,-1))
    east = minicube.isel(y=slice(1,-1), x=slice(2, None))
    west = minicube.isel(y=slice(1,-1), x=slice(0,-2))
    emc.Minicuber.save_minicube_netcdf(north, output_path + "north_offset.nc")
    emc.Minicuber.save_minicube_netcdf(south, output_path + "south_offset.nc")
    emc.Minicuber.save_minicube_netcdf(east, output_path + "east_offset.nc")
    emc.Minicuber.save_minicube_netcdf(west, output_path + "west_offset.nc")

def nanify_offset(ds, direction, var='ndvi_pred'):
    da = ds.copy()[var]

    lat_axis = da.get_axis_num('lat')
    lon_axis = da.get_axis_num('lon')

    lat_descending = ds.lat[0] > ds.lat[-1]
    lon_descending = ds.lon[0] > ds.lon[-1]

    indexer = [slice(None)] * da.ndim

    if direction == "north":
        indexer[lat_axis] = 0 if lat_descending else -1
    elif direction == "south":
        indexer[lat_axis] = -1 if lat_descending else 0
    elif direction == "east":
        indexer[lon_axis] = 0 if lon_descending else -1
    elif direction == "west":
        indexer[lon_axis] = -1 if lon_descending else 0

    da.values[tuple(indexer)] = np.nan
    ds[var] = da
    return ds

def average_predictions(rasters = None):
    if rasters is None:
        ds_original = minicube["s2_B04"].isel(y=slice(1,-1), x=slice(1,-1))
        ds_north = minicube["s2_B04"].isel(y=slice(0,-2), x=slice(1,-1))
        ds_south = minicube["s2_B04"].isel(y=slice(2, None), x=slice(1,-1))
        ds_east = minicube["s2_B04"].isel(y=slice(1,-1), x=slice(2, None))
        ds_west = minicube["s2_B04"].isel(y=slice(1,-1), x=slice(0,-2))
    else:
        ds_original = rasters[0]
        ds_north = rasters[1]
        ds_south = rasters[2]
        ds_east = rasters[3]
        ds_west = rasters[4]

    ds_north = nanify_offset(ds_north, "north")  # drop first row
    ds_south = nanify_offset(ds_south, "south")  # drop last row
    ds_east = nanify_offset(ds_east, "east")     # drop first column
    ds_west = nanify_offset(ds_west, "west")     # drop last column

    datasets = [ds_original, ds_north, ds_south, ds_east, ds_west]

    arrays = [ds['ndvi_pred'].values.astype('float32') for ds in datasets]
    stack = np.stack(arrays, axis=0)  # shape: (n_offsets+1, time, y, x)
    mean = np.nanmean(stack, axis=0)  # shape: (time, 128, 128)
    mean_da = xr.DataArray(mean, dims=ds_original['ndvi_pred'].dims, coords=ds_original['ndvi_pred'].coords)
    mean_ds = mean_da.to_dataset(name='ndvi_pred')
    mean_ds.to_netcdf("E:/DZ/reproduced_predictions/ood-t_chopped/pixel_offset_average_t_225_34TET_47.37_22.05.nc")
