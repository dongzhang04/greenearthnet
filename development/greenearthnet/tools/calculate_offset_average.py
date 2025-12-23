import xarray as xr
import numpy as np


import os
import subprocess
import sys

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
offset_path = "E:/DZ/offset"

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
    print("finished predictions")

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

    print("finished averaging")

if __name__ == "__main__":
    predict_offsets()
    average_minicube_predictions()
