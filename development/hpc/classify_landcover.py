import xarray as xr
import numpy as np
import os
import shutil

# ESA WorldCover codes
FOREST_CODES = [10]                # Tree cover
CROPLAND_CODES = [40]              # Cropland
SHRUB_GRASS_CODES = [20, 30]       # Shrubland + Grassland


def classify_file(file_path):
    try:
        ds = xr.open_dataset(file_path)
        # Replace 'worldcover' with your variable name
        wc = ds['esawc_lc'].values
        ds.close()

        wc = wc.flatten()

        total_pixels = wc.size

        # Count pixels per class
        forest_pixels = sum(np.isin(wc, FOREST_CODES))
        cropland_pixels = sum(np.isin(wc, CROPLAND_CODES))
        shrub_grass_pixels = sum(np.isin(wc, SHRUB_GRASS_CODES))

        # Fractions
        frac_forest = forest_pixels / total_pixels
        frac_cropland = cropland_pixels / total_pixels
        frac_shrub_grass = shrub_grass_pixels / total_pixels

        # Assign class with the largest number of pixels
        pixel_counts = {
            'forest': forest_pixels,
            'cropland': cropland_pixels,
            'shrub_grass': shrub_grass_pixels
        }
        dominant_class = max(pixel_counts, key=pixel_counts.get)

        return dominant_class, frac_forest, frac_cropland, frac_shrub_grass

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 'error', 0, 0, 0

def sort_tile(root, tile):
    # Paths
    output_root = r"/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data"
    input_folder = root + "/" + tile
    forest_folder = output_root + "/forest_dominated/train/" + tile
    cropland_folder = output_root + "/crop_dominated/train/" + tile
    shrub_grass_folder = output_root + "/shrub_dominated/train/" + tile

    # Create output folders if they don't exist
    os.makedirs(forest_folder, exist_ok=True)
    os.makedirs(cropland_folder, exist_ok=True)
    os.makedirs(shrub_grass_folder, exist_ok=True)

    # Loop over all files
    for filename in os.listdir(input_folder):
        if filename.endswith(".nc"):
            file_path = os.path.join(input_folder, filename)
            category, f_frac, c_frac, s_frac = classify_file(file_path)

            # Format fractions to 2 decimal places
            f_str = f"f{f_frac:.2f}"
            c_str = f"c{c_frac:.2f}"
            s_str = f"s{s_frac:.2f}"

            # New filename with fractions
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{f_str}_{c_str}_{s_str}{ext}"

            # Copy file to the appropriate folder
            if category == 'forest':
                shutil.copy(file_path, os.path.join(forest_folder, new_filename))
            elif category == 'cropland':
                shutil.copy(file_path, os.path.join(cropland_folder, new_filename))
            elif category == 'shrub_grass':
                shutil.copy(file_path, os.path.join(shrub_grass_folder, new_filename))
            else:
                print(f"{filename} could not be classified.")

    print("Done classifying files in tile: ", tile)

if __name__ == "__main__":
    base_dir = r"/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/train"
    for root, dirs, files in os.walk(base_dir):
        for dir in dirs:
            print("classifying files in tile: ", dir)
            sort_tile(root, dir)