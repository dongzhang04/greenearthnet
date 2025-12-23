populate_prediction_minicubes.py and run_retrained_predictions.py are used for running predictions on retrained weights:

populate_prediction_minicubes.py will setup the proper folder structure and copy the desired minicubes to predict on.
This folder structure is as follows: root
                                     |--- Crop
                                       |--- 29TQF
                                         |---ood-t_chopped
                                           |---MJJ21
                                             |---minicube.nc
                                       |--- 30TWK
                                       .
                                       .
                                       .
                                     |--- Forest
                                     |--- Shrub

run_retrained_predictions.py will perform two predictions on the selected minicubes, one with the retrained weights and one with
Vitus' original weights, creating and outputting to the folders "retrained_predictions" and "original_predictions" within each tile folder. 
This script expects there to be a retrained weights file within each tile folder, with the naming convention "{tile}_regular_val.cptk"


generate_offset_minicubes.py and calculate_offset_average.py are used for running the blocking treatment on predictions:

generate_offset_minicubes.py will copy minicubes from a folder with the same structure outlined above to an offset folder (with the same structure).
The script must be run in the minicuber environment, as it must recreate the original minicube as well as four offset minicubes.
The script also contains code for generating predictions and averaging the offsets, but this requires the greenearthnet environment 
so calculate_offset_average.py has been created for this specific task. 

(!) generating a minicube requires the Geomorpho90m dataset. I had simply downloaded this data for the regions between 
30 to 60 degrees north x -30 to 30 degrees east from a google drive folder, however this folder is no longer accessible making 
minicubes outside this range unable to be generated. The article (https://www.nature.com/articles/s41597-020-0479-6) does however
say the following: "Machine-accessible metadata file describing the reported data: https://doi.org/10.6084/m9.figshare.12145791"

calculate_offset_average.py will generate five predictions, one for each minicube created in the above step, and then create one
final averaged prediction. These six predictions will be placed in a 'predictions' folder found within each tile's folder.


metrics.py (and its copy, metrics.ipynb) contains code to generate boxplots of five metrics for the original preditions, retrained predictions, and blocking treatment predictions
for the blocking treatment, because minicubes have to be recreated, a second set of original predictions metrics are calculate from
these recreated minicubes. 
The five metrics are:
Uncertainty (U): Root mean square of estimates minus reference.
Accuracy (A): Mean of estimates minus reference.
Percision (P): Root mean square of estimates minus reference minus A.
Pearson correlation coefficient (R)
Structural Similarity Index Measure (SSIM)


classify_landcover.py is used to sort a folder of minicubes into the three landcover types: crop, forest, and shrub/grassland.
Using the ESA WorldCover map in each minicube, the number of pixels for each landcover type is counted and the one with the largest
count is selected as the minicube's landcover type. A copy of each minicube is created with each of the three landcover percentages
being appended to the file name. 


count_num_minicubes.py counts the number of minicubes in each of the training set's tiles 


graph_ndvi.py splits a prediction file into its 20 timesteps as tiffs and colors ndvi according to the scale used in the QGIS visualizations
this is an alternative to using QGIS to visualize predictions, however the image quality in QGIS is superior so this script is not in use.


nc_to_tiff.py contains functions that:
    splits a prediction into 20 timesteps and outputs each as tiffs
    converts a minicube into a tiff and caluclates its ndvi for visualization in QGIS
    calculates an estimated fcover using ndvi from a given prediction file
this script is not in use outside of the first function which was ran on all the original predictions for identification of hallucinations. 
