import xarray as xr
import numpy as np
from skimage.metrics import structural_similarity as ssim
import seaborn as sns

def ssim_wrapper(img1, img2):
    return ssim(img1, img2, data_range=2.0)

def calculate_metrics(input_nc, reference_nc, roi_lat, roi_lon, subsampling_factor=1):
    input_ndvi = xr.open_dataset(input_nc)["ndvi_pred"]
    reference_ndvi = xr.open_dataset(reference_nc)["ndvi"]
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





