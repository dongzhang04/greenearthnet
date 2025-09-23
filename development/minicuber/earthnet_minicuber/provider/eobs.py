
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

    def __init__(self, bands = ['TG', 'TN', 'TX', 'RR', 'PP', 'HU', 'FG', 'QQ'], path = None):
        # self.is_temporal = True
        
        self.bands = bands
        self.path = path

    def load_data(self, bbox, time_interval, **kwargs):
        
        # If an URL is given, loads the cloud zarr, otherwise loads from local zarrpath
        if self.path:
            eobs = xr.open_dataset(self.path, consolidated = False)
        else:
            print(f"Loading EObs for bbox {bbox} failed")
            return None

        eobs = eobs[self.bands]

        center_lon = (bbox[0] + bbox[2])/2
        center_lat = (bbox[1] + bbox[3])/2

        eobs = eobs.sel(lat = center_lat, lon = center_lon, method = "nearest").drop_vars(["lat", "lon"])

        eobs = eobs.sel(time = slice(time_interval[:10], time_interval[-10:]))

        agg_eobs_collector = []
        for aggregation_type in self.aggregation_types:
            if aggregation_type == "mean":
                curr_agg_eobs = eobs.groupby("time.date").mean("time").rename({"date": "time"})
            
            else:
                continue
            curr_agg_eobs["time"] = np.array([str(d) for d in curr_agg_eobs.time.values], dtype="datetime64[D]")
            curr_agg_eobs = curr_agg_eobs.rename({b: f"era5land_{b}_{aggregation_type}" for b in self.bands})
            agg_eobs_collector.append(curr_agg_eobs)
        
        agg_eobs = xr.merge(agg_eobs_collector)


        # for b in self.bands:
        #     for a in self.aggregation_types:

        #         agg_eobs[f"era5land_{b}_{a}"].attrs = {
        #             "provider": "ERA5-Land",
        #             "interpolation_type": "linear",
        #             "description": f"{SHORT_TO_LONG_NAMES[b]} 3-hourly data aggregated by {a}"
        #         }
        

        return agg_eobs