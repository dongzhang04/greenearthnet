import warnings
import datetime
import xarray as xr
import numpy as np
import pandas as pd

from earthnet_minicuber.minicuber import Minicuber

from pyproj import Transformer
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info

import os
import subprocess
import sys

class OffsetMinicuber(Minicuber):
    def __init__(self, specs, spatial_offset=None, spatial_offset_distance=40, temporal_offset=None):
        super().__init__(specs)
        self.spatial_offset = spatial_offset  # "NE", "NW", "SE", "SW"
        self.spatial_offset_distance = spatial_offset_distance
        self.temporal_offset = temporal_offset # None, str, list[str], or tuple(start, end)

    @property
    def bbox(self):
        utm_epsg = int(query_utm_crs_info(
            datum_name="WGS 84",
            area_of_interest=AreaOfInterest(self.lon_lat[0], self.lon_lat[1], self.lon_lat[0], self.lon_lat[1])
        )[0].code)

        transformer = Transformer.from_crs(4326, utm_epsg, always_xy=True)
        x_center, y_center = transformer.transform(*self.lon_lat)

        # Apply spatial offset
        d = self.spatial_offset_distance
        if self.spatial_offset == "NE":
            x_center += d; y_center += d
        elif self.spatial_offset == "NW":
            x_center -= d; y_center += d
        elif self.spatial_offset == "SE":
            x_center += d; y_center -= d
        elif self.spatial_offset == "SW":
            x_center -= d; y_center -= d

        nx, ny = self.xy_shape

        x_left   = x_center - self.resolution * (nx // 2)
        x_right  = x_center + self.resolution * (nx // 2)
        y_top    = y_center + self.resolution * (ny // 2)
        y_bottom = y_center - self.resolution * (ny // 2)

        return transformer.transform_bounds(
            x_left, y_bottom, x_right, y_top, direction="INVERSE"
        )


    @classmethod
    def load_minicube(cls, specs, spatial_offset=None, spatial_offset_distance=40, temporal_offset=None, verbose=True, compute=False):

        self = cls(specs, spatial_offset=spatial_offset, spatial_offset_distance=spatial_offset_distance, temporal_offset=temporal_offset)
        
        if not compute and (len(self.monthly_intervals) > 3):
            warnings.warn("You are querying a long time interval with compute = False, this might lead to failure in the dask sheduler and high memory consumption upon calling .compute(). Consider using compute = True instead.")

        warnings.filterwarnings('ignore')
        all_data = []
        cube = None

        for time_interval in self.monthly_intervals:
            for provider in self.temporal_providers:
                if verbose:
                    print(f"Loading {provider.__class__.__name__} for {time_interval}")

                product_cube = provider.load_data(self.padded_bbox, time_interval, full_time_interval=self.full_time_interval)

                if product_cube is not None:
                    if cube is None:
                        cube = self.regrid_product_cube(product_cube)
                    else:
                        cube = xr.merge([cube, self.regrid_product_cube(product_cube)])
                else:
                    if verbose:
                        print(f"Skipping {provider.__class__.__name__} for {time_interval}")

            if cube is not None:
                if compute:
                    if verbose:
                        print(f"Downloading for {time_interval}...")
                    all_data.append(cube.compute())
                else:
                    all_data.append(cube)
            cube = None

        cube = xr.merge(all_data, combine_attrs='override')

        for provider in self.spatial_providers:
            if verbose:
                print(f"Loading {provider.__class__.__name__}")
            product_cube = provider.load_data(self.padded_bbox, "not_needed")
            if product_cube is not None:
                if cube is None:
                    cube = self.regrid_product_cube(product_cube)
                else:
                    cube = xr.merge([cube, self.regrid_product_cube(product_cube)])
            else:
                if verbose:
                    print(f"Skipping {provider.__class__.__name__} - no data found.")

        if compute:
            cube = cube.compute()

        if "time" in cube:
            cube['time'] = pd.DatetimeIndex(cube['time'].values)
            cube = cube.drop_duplicates(dim='time').sortby('time')
            cube = cube.sel(time = slice(self.time_interval[:10], self.time_interval[-10:]))

        cube.attrs = {
            "history": f"Created with OffsetMinicuber on {datetime.datetime.now()}, extended from the earthnet-minicuber Python package. See https://github.com/earthnet2021/earthnet-minicuber"
        }

        return cube


    @staticmethod
    def apply_temporal_offset(cube, temporal_offset):
        # Case 1: single timestamp
        if isinstance(temporal_offset, str):
            return cube.drop_sel(time=temporal_offset)

        # Case 2: list of timestamps
        if isinstance(temporal_offset, (list, tuple)) and isinstance(temporal_offset[0], str):
            return cube.drop_sel(time=temporal_offset)

        # Case 3: time range (tuple start, end)
        if isinstance(temporal_offset, tuple) and len(temporal_offset) == 2:
            start, end = temporal_offset
            return cube.drop_sel(time=slice(start, end))

        return cube


    @classmethod
    def save_minicube(cls, specs, savepath, spatial_offset=None, spatial_offset_distance=40, temporal_offset=None, verbose=True):
        minicube = cls.load_minicube(specs, spatial_offset=spatial_offset, spatial_offset_distance=spatial_offset_distance, temporal_offset=temporal_offset, verbose=verbose, compute=True)

        if verbose:
            print(f"Downloading minicube at {specs['lon_lat']}")

        minicube = minicube.compute()
        if temporal_offset is not None:
            minicube = cls.apply_temporal_offset(minicube, temporal_offset)

        if "s2_mask" in minicube.variables and "s2_dlmask" not in minicube.variables:
            minicube = minicube.rename({"s2_mask": "s2_dlmask"})

        if "angle" in minicube.variables:
            minicube = minicube.drop_vars(["angle"])

        if verbose:
            print(f"Saving minicube at {specs['lon_lat']}")

        cls.save_minicube_netcdf(minicube, savepath)



def select_inside_center(offset_ds, ref_ds, var='ndvi_pred'):
    da = offset_ds[var]
    lat_min = ref_ds[var].lat.min()
    lat_max = ref_ds[var].lat.max()
    lon_min = ref_ds[var].lon.min()
    lon_max = ref_ds[var].lon.max()

    da_cropped = da.where(
        (da.lat >= lat_min) & (da.lat <= lat_max) &
        (da.lon >= lon_min) & (da.lon <= lon_max),
        drop=True
    )
    return da_cropped

def generate_offset_minicubes(specs, savepath, offset_distance=40, temporal_offset=None):
    offsets = ["NE", "NW", "SE", "SW"]
    OffsetMinicuber.save_minicube(specs, savepath, temporal_offset=temporal_offset)
    for offset_direction in offsets:
        OffsetMinicuber.save_minicube(specs, f"{savepath.replace('.nc','')}_{offset_direction}.nc", spatial_offset=offset_direction, spatial_offset_distance=offset_distance, temporal_offset=temporal_offset)


def average_offset_predictions(center, output_path):
    file_name = center.split(".nc")[0]
    ne = file_name + "_NE.nc"
    nw = file_name + "_NW.nc"
    se = file_name + "_SE.nc"
    sw = file_name + "_SW.nc"
    files = [center, ne, nw, se, sw]

    datasets = [xr.open_dataset(f) for f in files]
    ref_ds = datasets[0]
    ref_da = ref_ds['ndvi_pred']
    cropped_offsets = [select_inside_center(ds, ref_ds) for ds in datasets]  # returns DataArrays
    aligned_offsets = [
        da.interp(lat=ref_da.lat, lon=ref_da.lon)
        for da in cropped_offsets
    ]

    all_da = [ref_da] + aligned_offsets
    stack = np.stack([da.values for da in all_da], axis=0)  # stack values of DataArrays
    mean_values = np.nanmean(stack, axis=0)
    mean_da = xr.DataArray(mean_values, dims=ref_da.dims, coords=ref_da.coords)
    mean_ds = mean_da.to_dataset(name='ndvi_pred')

    file_name = file_name.replace("\\", "/").split("/")[-1]
    output_path = output_path.replace("\\", "/")
    output_path = output_path if output_path.endswith("/") else output_path + "/"
    # print(file_name)
    # print(output_path)
    mean_ds.to_netcdf(output_path + file_name + "_average.nc")


bands = ['TG', 'TN', 'TX', 'RR', 'PP', 'HU', 'FG', 'QQ']
paths = ["C:/Users/dozhang/Downloads/tg_ens_mean_0.1deg_reg_v26.0e.nc", 
        "C:/Users/dozhang/Downloads/tn_ens_mean_0.1deg_reg_v26.0e.nc",
        "C:/Users/dozhang/Downloads/tx_ens_mean_0.1deg_reg_v26.0e.nc",
        "C:/Users/dozhang/Downloads/rr_ens_mean_0.1deg_reg_v26.0e.nc",
        "C:/Users/dozhang/Downloads/pp_ens_mean_0.1deg_reg_v26.0e.nc",
        "C:/Users/dozhang/Downloads/hu_ens_mean_0.1deg_reg_v26.0e.nc",
        "C:/Users/dozhang/Downloads/fg_ens_mean_0.1deg_reg_v26.0e.nc",
        "C:/Users/dozhang/Downloads/qq_ens_mean_0.1deg_reg_v26.0e.nc"]
bands_dict = dict(zip(bands, paths))
geom_folder = "C:/Users/dozhang/Downloads/geom_90M"


def copy_specs(minicube_path):
    ds = xr.open_dataset(minicube_path)
    ds_B4 = ds["s2_B04"]
    dates = ds.time.values
    end_date = str(dates[-1]).split("T")[0]

    for i in range(len(dates)): 
        if not ds_B4.sel(time=dates[i]).isnull().all().item():
            offset = i%5
            break
    
    if offset != 0:
        days_removed = 5-offset
        dt = dates[0]
        removed_dates = [0]*days_removed
        for i in range(days_removed):
            dt = dt - np.timedelta64(1, "D")
            removed_dates[-1*(i+1)] = str(dt)

        
        start_date = removed_dates[0].split("T")[0]
    else:
        removed_dates = None
        start_date = str(dates[0]).split("T")[0]

    latitude = np.median(ds.lat)
    longitude = np.median(ds.lon)

    geom_lat = int(latitude - (latitude%5))
    geom_lon = int(longitude - (longitude%5))
    if geom_lon >=0:
        if geom_lon < 10:
            geom_lon = "e00" + str(geom_lon)
        else:
            geom_lon = "e0" + str(geom_lon)
    else:
        if longitude == geom_lon:
            longitude-=5
        geom_lon = abs(geom_lon)
        if geom_lon == 5:
            geom_lon = "w005"
        else:
            geom_lon = "w0" + str(geom_lon)

    specs = {
        "lon_lat": (longitude, latitude), # center pixel
        "xy_shape": (128, 128), # width, height of cutout around center pixel
        "resolution": 20, # in meters.. will use this on a local UTM grid..
        "time_interval": f"{start_date}/{end_date}",
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

            #     # RasterioIOError('CURL error: schannel: CertGetCertificateChain trust error CERT_TRUST_IS_UNTRUSTED_ROOT')
            #     # {"name": "srtm", "kwargs": {"bands": ["dem"]}},
                
                {"name": "nasa", "kwargs": {}},
                {"name": "alos", "kwargs": {}},
                {"name": "cop", "kwargs": {}},
            {
                "name": "esawc",
                "kwargs": {"bands": ["lc"], "aws_bucket": "planetary_computer"},
            },
            {
                "name": "geom",
                "kwargs": {"filepath": f"{geom_folder}/geom_90M_n{geom_lat}{geom_lon}.tif"}
            },
            {
                "name": "eobs",
                "kwargs": {"bands": bands_dict}
            }
        ],
    }
    ds.close()
    return specs, removed_dates


sites = {
        "Crop": ["29TQF",
             "30TWK",
             "30UYU",
        ###      "31TBF", 
             "31UFP", 
             "32UNC", 
             "33UWT", 
             "33UXP", 
             "34TFL",
             "34SEJ"],

        "Forest": ["29TNE",
               "30TTK",
               "31TBF",
               "31UFP",
               "33UWT", 
               "33VVG",
               "33VUF", 
        ###        "33VUG",
               "34SFF", 
               "34SEJ"],

        "Shrub": ["29SND",
              "29SPC", 
              "29TQF", 
        ###       "30TTK",
              "30STJ", 
              "30UYV",
              "31TBF",
              "32TML", 
              "34SFF", 
              "34TCL"]
    }
copy_path = "E:/DZ/retraining"
offset_path = "E:/DZ/offset"
def copy_minicubes():
    for landcover in sites:
        print(f"copying {landcover}")
        for tile in sites[landcover]:
            print(tile)
            in_dir = f"{copy_path}/{landcover}/{tile}/ood-t_chopped/MJJ21"
            out_dir = f"{offset_path}/{landcover}/{tile}/ood-t_chopped/MJJ21"
            os.makedirs(out_dir, exist_ok=True)
            for file in os.listdir(in_dir):
                if file.endswith(".nc"):
                    file_path = os.path.join(in_dir, file)
                    specs, removed_dates = copy_specs(file_path)
                    generate_offset_minicubes(specs, out_dir + f"/{file}", temporal_offset=removed_dates)
             

    print("finished")

weights = "E:/DZ/model_weights/contextformer/contextformer6M/seed=42.ckpt"
config = "E:/DZ/model_configs/contextformer/contextformer6M/seed=42.yaml"
def predict_offsets():
    for landcover in sites:
        print("Land cover type:", landcover)
        for tile in sites[landcover]:
            dir = f"{offset_path}/{landcover}/{tile}"
            predictions = dir + "/predictions"
            os.makedirs(predictions, exist_ok=True)

            print("Running predictions for tile:", tile)
            subprocess.run([sys.executable, "C:/Users/dozhang/Documents/GitHub/greenearthnet/development/greenearthnet/test.py", 
                            config,
                            weights,
                            "--track", "ood-t_chopped",
                            "--pred_dir", predictions,
                            "--data_dir", dir], check=True)
    print("finished")

def average_minicube_predictions():
    for landcover in sites:
        print(landcover)
        for tile in sites[landcover]:
            print(tile)
            dir = f"{offset_path}/{landcover}/{tile}/predictions/MJJ21"
            for file in os.listdir(dir):
                if not file.endswith(("NE.nc", "NW.nc", "SE.nc", "SW.nc")) and file.endswith(".nc"):
                    file_path = os.path.join(dir, file)
                    average_offset_predictions(file_path, dir)            

    print("finished")

if __name__ == "__main__":
    
    #requires the minicuber environment
    copy_minicubes()

    #requires the greenearthnet environment, use calculate_offset_average.py for these tasks instead.
    # predict_offsets()
    # average_minicube_predictions()
