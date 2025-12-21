import os
import sys
import subprocess

model_weights = "_regular_val.ckpt"
config = "E:/DZ/model_configs/contextformer/contextformer6M/seed=42.yaml"
path = "E:/DZ/retraining"


prediction_sites = {
    "Crop": ["30UYU", 
            #  "29TQF",
            #  "30TWK",
             "31TBF", 
             "31UFP", 
             "32UNC", 
             "33UWT", 
             "33UXP", 
            #  "34TFL", no minicube
             "34SEJ"],

    "Forest": ["30TTK",
            #    "29TNE",
            #    "31TBF", no minicube
            #    "31UFP", no minicube
               "33UWT", 
            #    "33VVG",
            #    "33VUF", 
            #    "33VUG",
               "34SFF", 
               "34SEJ"],

    "Shrub": ["29SND",
              "29SPC", 
              "29TQF", 
              "30STJ", 
            #   "30UYV", no minicube
            #   "31TBF", no minicube
              "32TML", 
              "34SFF", 
              "34TCL"]
}

if __name__ == "__main__":
    for key in prediction_sites:
        print("Land cover type:", key)
        for tile in prediction_sites[key]:
            dir = path + f"/{key}/{tile}"
            predictions = dir + "/predictions"
            os.makedirs(predictions, exist_ok=True)
            weights = dir + "/" + tile + model_weights
            print("Running predictions for tile:", tile)
            subprocess.run([sys.executable, "C:/Users/dozhang/Documents/GitHub/greenearthnet/development/greenearthnet/test.py", 
                            config,
                            weights,
                            "--track", "ood-t_chopped",
                            "--pred_dir", predictions,
                            "--data_dir", dir], check=True)
    print("finished")