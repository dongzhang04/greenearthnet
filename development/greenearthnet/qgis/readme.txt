the netCDF outputs from Contextformer are not automatically formatted correctly when imported into QGIS in that the timestamps cannot be selected with there only being a single ndvi group
to see each timestamp individually, you must run the following command in the OSGeo-4W shell:
gdalbuildvrt -separate "output path" "input path"
and then load the vrt into QGIS, with each band being a distinct timestep
gdalbuildvrt -separate "C:\Users\dozhang\Documents\GitHub\greenearthnet\development\greenearthnet\predictions\JAS2021_replicated_minicube_0_29SND_39.29_-8.56.vrt" "C:\Users\dozhang\Documents\GitHub\greenearthnet\development\greenearthnet\predictions\JAS2021_replicated_minicube_0_29SND_39.29_-8.56.nc"
gdalbuildvrt -separate "C:\Users\dozhang\Documents\GitHub\greenearthnet\development\greenearthnet\predictions\minicube_0_29SND_39.29_-8.56.vrt" "C:\Users\dozhang\Documents\GitHub\greenearthnet\development\greenearthnet\predictions\minicube_0_29SND_39.29_-8.56.nc"