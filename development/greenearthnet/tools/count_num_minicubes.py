import os


def count_files(root, tile):
    # Loop over all files
    i = 0
    input_folder = root + "\\" + tile
    for filename in os.listdir(input_folder):
        if filename.endswith(".nc"):
            i += 1

    print("Number of minicubes in", tile, ":", i)
    return i, tile

if __name__ == "__main__":
    print("Shrub")
    base_dir = r"E:\DZ\retraining\TrainingData\shrub_dominated"
    max = 0
    location = ""
    for root, dirs, files in os.walk(base_dir):
        for dir in dirs:
            print("counting files in tile: ", dir)
            i, tile = count_files(root, dir)
            if i > max:
                max = i
                location = tile
    print("Max number of minicubes in a tile: ", max, "at:", location)