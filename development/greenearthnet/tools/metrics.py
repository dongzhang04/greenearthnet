import xarray as xr
import numpy as np
from skimage.metrics import structural_similarity as ssim
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def ssim_wrapper(img1, img2):
    return ssim(img1, img2, data_range=2.0)

#takes in a single prediction minicube pair (file names) to calculate metrics on a single prediction
#outputs a dictionary whose entries are xarrays of a single metric with 20 values (one for each prediction timestep)
def calculate_metrics(input_nc, reference_nc):
    cloud_threshold = 0.2
    input_ndvi = xr.open_dataset(input_nc)["ndvi_pred"]
    reference = xr.open_dataset(reference_nc)
    reference_B4 = reference["s2_B04"]
    dates = reference.time.values
    
    #finding the first date with an S2 image and determining the image offset
    for i in range(len(dates)): 
        if not reference_B4.sel(time=dates[i]).isnull().all().item():
            offset = i%5
            break

    #dropping non S2 imagery dates 
    for i in range(dates.size):
        if i < offset:
            reference = reference.drop_sel(time=dates[i])
        else:
            offset += 5
            if offset <55:
                reference = reference.drop_sel(time=dates[i])   

    #ndvi calculation
    reference["ndvi"] = (("time", "x", "y"), np.zeros((20, 128, 128)))
    reference["ndvi"] = (reference["s2_B8A"] - reference["s2_B04"]) / xr.where((reference["s2_B8A"] + reference["s2_B04"]) == 0, np.nan, (reference["s2_B8A"] + reference["s2_B04"]))
    
    #masking cloudy pixels with NaNs which are handled by numpy and xarray methods
    masked = reference.where(reference["s2_dlmask"] == 0)
    reference_ndvi = masked["ndvi"]
    #NaNs are not handled by skimage, so clouds are masked with the average NDVI value of the timestep
    ssim_reference_ndvi = reference_ndvi.fillna(reference_ndvi.mean(dim=("lat", "lon"), skipna=True))

    residuals = input_ndvi - reference_ndvi
    
    #metrics calculations
    U = np.sqrt((residuals**2).mean(dim=("lat", "lon"))) #RMSE
    A = (residuals).mean(dim=("lat", "lon"))
    P = np.sqrt(((residuals - A)**2).mean(dim=("lat", "lon")))
    R = xr.corr(input_ndvi, reference_ndvi, dim=("lat", "lon"))
    SSIM = xr.apply_ufunc(
        ssim_wrapper,
        input_ndvi,
        ssim_reference_ndvi,
        input_core_dims=[["lat","lon"], ["lat","lon"]],
        vectorize=True,
        output_dtypes=[float]
    )

    #dropping metrics for dates that are too cloudy
    cloud = (reference["s2_dlmask"] == 0).sum(dim=["lat", "lon"]) < (128*128*(1-cloud_threshold))
    for i in range(20):
        if cloud[i].item():
            U[i] = np.nan
            A[i] = np.nan
            P[i] = np.nan
            R[i] = np.nan
            SSIM[i] = np.nan

    return {
        "Uncertainty": U,
        "Accuracy": A,
        "Precision": P,
        "Pearson Correlation": R,
        "SSIM": SSIM
    }

#takes in an array of prediction file names and an array of corresponding minicube file names to calculate metrics on multiple predictions
#outputs a dictionary where each entry contains a collection of xarrays; each xarray corresponds to the given metric of a single prediction
def gather_metrics(input_files, reference_files):
    U = []
    A = []
    P = []
    R = []
    SSIM = []
    for i in range(len(input_files)):
        metrics = calculate_metrics(input_files[i], reference_files[i])
        U.append(metrics["Uncertainty"])
        A.append(metrics["Accuracy"])
        P.append(metrics["Precision"])
        R.append(metrics["Pearson Correlation"])
        SSIM.append(metrics["SSIM"])
    return {
        "Uncertainty": U,
        "Accuracy": A,
        "Precision": P,
        "Pearson Correlation": R,
        "SSIM": SSIM
    }

#expects each dataset to be an array of xarrays
def plot_metric(crop_datasets, forest_datasets, shrub_datasets, metric):
    datasets = [crop_datasets, forest_datasets, shrub_datasets]
    
    #converting xarrays to pandas dataframes, replacing the time dimension's datetimes with intergers corresponding to the timestpe
    #and adding a landcover-type variable
    for l in range(3):
        for i in range(len(datasets[l])):
            datasets[l][i] = datasets[l][i].assign_coords(time=np.arange(1, datasets[l][i].sizes["time"] + 1)).to_dataframe(name=metric).reset_index().assign(land_type=["Crop", "Forest", "Shrub"][l])

    #merging each prediction's dataframe into a single dataframe for the entire landcover-type 
    crop_data = pd.concat(datasets[0], ignore_index=True)
    forest_data = pd.concat(datasets[1], ignore_index=True)
    shrub_data = pd.concat(datasets[2], ignore_index=True)

    #merging all the data into a single dataframe to be plotted
    all_data = pd.concat([crop_data, forest_data, shrub_data], ignore_index=True)
    sns.boxplot(
        data=all_data,
        x="time",
        y=metric,
        hue="land_type"
    )

#returns arrays of prediction files, with the predictions argument specifying whether these are original or retrained predictions
#the three arrays returned correspond to each of the 3 landcover types
def gather_inputs(root, predictions, sites):
    collection = []
    for landcover in sites:
        landcover_sites = []
        for tile in sites[landcover]:
            dir = f"{root}/{landcover}/{tile}/{predictions}/MJJ21"
            for file in os.listdir(dir):
                if file.endswith(".nc"):
                    landcover_sites.append(os.path.join(dir, file))
        collection.append(landcover_sites)
    return collection[0], collection[1], collection[2]

#returns arrays of minicubes files
#the three arrays returned correspond to each of the 3 landcover types
def gather_references(root, sites):
    collection = []
    for landcover in sites:
        landcover_sites = []
        for tile in sites[landcover]:
            dir = f"{root}/{landcover}/{tile}/ood-t_chopped/MJJ21"
            for file in os.listdir(dir):
                if file.endswith(".nc") and not file.endswith(("NE.nc", "NW.nc", "SE.nc", "SW.nc")):
                    landcover_sites.append(os.path.join(dir, file))
        collection.append(landcover_sites)
    return collection[0], collection[1], collection[2]

#returns arrays of blocking treatment related prediction files
#prediction_type = "offset" specifies returniing the averaged prediction, any other value will return the center ("original") prediction
#the three arrays returned correspond to each of the 3 landcover types
def gather_offset_inputs(root, prediction_type, sites):
    collection = []
    for landcover in sites:
        landcover_sites = []
        for tile in sites[landcover]:
            dir = f"{root}/{landcover}/{tile}/predictions/MJJ21"
            for file in os.listdir(dir):
                if prediction_type == "offset":
                    if file.endswith("average.nc"):
                        landcover_sites.append(os.path.join(dir, file))
                else:
                    if file.endswith(".nc") and not file.endswith(("NE.nc", "NW.nc", "SE.nc", "SW.nc", "average.nc")):
                        landcover_sites.append(os.path.join(dir, file))
                        
        collection.append(landcover_sites)
    return collection[0], collection[1], collection[2]


if __name__ == "__main__":
    # input = r"E:\DZ\predictions\contextformer6M_seed42\MJJ21\minicube_225_34TET_47.37_22.05.nc"
    # reference = r"E:\DZ\greenearthnet\ood-t_chopped\MJJ21\minicube_225_34TET_47.37_22.05.nc"
    
    # print(calculate_metrics(input, reference))

    sites = {
        "Crop": ["29TQF",
                "30TWK",
                "30UYU",
                "31TBF", 
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
                "33VUG",
                "34SFF", 
                "34SEJ"],

        "Shrub": ["29SND",
                "29SPC", 
                "29TQF", 
                "30TTK",
                "30STJ", 
                "30UYV",
                "31TBF",
                "32TML", 
                "34SFF", 
                "34TCL"]
    }
    root = "E:/DZ/retraining"
    predictions = "retrained_predictions"
    crop_input, forest_input, shrub_input = gather_inputs(root, predictions, sites)
    crop_reference, forest_reference, shrub_reference = gather_references(root, sites)

    crop_datasets = gather_metrics(crop_input, crop_reference)
    forest_datasets = gather_metrics(forest_input, forest_reference)
    shrub_datasets = gather_metrics(shrub_input, shrub_reference)
    metrics = ["Uncertainty", "Accuracy", "Precision", "Pearson Correlation", "SSIM"]
    for i in range(len(metrics)):
        plt.figure(figsize=(10,6))
        plot_metric(crop_datasets[metrics[i]], forest_datasets[metrics[i]], shrub_datasets[metrics[i]], metrics[i])
        plt.title(f"{metrics[i]} across Land Types over Time")
        plt.xlabel("Time (5-day intervals)")
        plt.ylabel(metrics[i])
        plt.legend(title="Land Type")
        plt.show()  



