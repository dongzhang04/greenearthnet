
import os
import pystac_client
import stackstac
import rasterio
import xarray as xr
import numpy as np
import fsspec
import time
import random

from . import provider_base

class EOBS(provider_base.Provider):

    # bands is taken to be a dictionary, with the keys as variable names and values as netcdf files with the data for the variables
    def __init__(self, bands):

        self.is_temporal = True
        
        # self.bands = list(dict.keys())
        # self.path = list(dict.values())
        # self.dict = zip(bands, path)
        self.bands = bands

    def load_data(self, bbox, time_interval, **kwargs):
        
        agg_eobs_collector = []

        for k in self.bands.keys():
            eobs = xr.open_dataset(self.bands[k])

            center_lon = (bbox[0] + bbox[2])/2
            center_lat = (bbox[1] + bbox[3])/2

            eobs = eobs.sel(latitude = center_lat, longitude = center_lon, method = "nearest").drop_vars(["latitude", "longitude"])

            eobs = eobs.sel(time = slice(time_interval[:10], time_interval[-10:]))
            
            eobs = eobs.rename({k.lower(): f"eobs_{k.lower()}"})
            agg_eobs_collector.append(eobs)
            
        agg_eobs = xr.merge(agg_eobs_collector)


            # for b in self.bands:
            #     for a in self.aggregation_types:

            #         agg_eobs[f"era5land_{b}_{a}"].attrs = {
            #             "provider": "ERA5-Land",
            #             "interpolation_type": "linear",
            #             "description": f"{SHORT_TO_LONG_NAMES[b]} 3-hourly data aggregated by {a}"
            #         }
            

        return agg_eobs