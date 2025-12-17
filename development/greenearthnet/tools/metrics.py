import xarray as xr
import numpy as np
from skimage.metrics import structural_similarity as ssim
import seaborn as sns

def ssim_wrapper(img1, img2):
    return ssim(img1, img2, data_range=2.0)

def calculate_metrics(input_nc, reference_nc, roi_lat=None, roi_lon=None, subsampling_factor=1):
    input_ndvi = xr.open_dataset(input_nc)["ndvi_pred"]
    reference = xr.open_dataset(reference_nc)
    reference_B4 = reference["s2_B04"]
    dates = reference.time.values
    
    for i in range(5): 
        if not reference_B4.sel(time=dates[i]).isnull().all().item():
            offset = i
            break
    
    for i in range(dates.size):
        if i < offset:
            reference = reference.drop_sel(time=dates[i])
        else:
            offset += 5
            if offset <55:
                reference = reference.drop_sel(time=dates[i])
    
    reference["ndvi"] = (("time", "x", "y"), np.zeros((20, 128, 128)))
    reference["ndvi"] = (reference["s2_B8A"] - reference["s2_B04"]) / xr.where((reference["s2_B8A"] + reference["s2_B04"]) == 0, np.nan, (reference["s2_B8A"] + reference["s2_B04"]))
    reference_ndvi = reference["ndvi"]

    # input_ndvi = reference_ndvi
    residuals = input_ndvi - reference_ndvi
    U = np.sqrt((residuals**2).mean(dim=("lat", "lon"))) #RMSE
    A = (residuals).mean(dim=("lat", "lon"))
    P = np.sqrt(((residuals - A)**2).mean(dim=("lat", "lon")))
    R = xr.corr(input_ndvi, reference_ndvi, dim=("lat", "lon"))
    SSIM = xr.apply_ufunc(
        ssim_wrapper,
        input_ndvi,
        reference_ndvi,
        input_core_dims=[["lat","lon"], ["lat","lon"]],
        vectorize=True,
        output_dtypes=[float]
    )
    return {
        "Uncertainty": U,
        "Accuracy": A,
        "Precision": P,
        "Pearson Correlation": R,
        "SSIM": SSIM
    }

def plot_metrics():
    pass

if __name__ == "__main__":
    input = r"E:\DZ\predictions\contextformer6M_seed42\MJJ21\minicube_0_29SND_39.29_-8.56.nc"
    reference = r"E:\DZ\greenearthnet\ood-t_chopped\MJJ21\minicube_0_29SND_39.29_-8.56.nc"
    print(calculate_metrics(input, reference))



