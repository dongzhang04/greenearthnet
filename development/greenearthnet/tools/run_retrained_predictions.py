import os
import sys
import subprocess

prediction_folders = ["retrained_predictions", "original_predictions"]
retrained_weights = "_regular_val.ckpt"
original_weights = "E:/DZ/model_weights/contextformer/contextformer6M/seed=42.ckpt"
config = "E:/DZ/model_configs/contextformer/contextformer6M/seed=42.yaml"
path = "E:/DZ/retraining"

prediction_sites = {
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


if __name__ == "__main__":
    for i in range(len(prediction_folders)):
      print(prediction_folders[i])
      for key in prediction_sites:
          print("Land cover type:", key)
          for tile in prediction_sites[key]:
              dir = path + f"/{key}/{tile}"
              predictions = dir + f"/{prediction_folders[i]}"
              os.makedirs(predictions, exist_ok=True)
              if i == 0:
                weights = dir + "/" + tile + retrained_weights
              else:
                weights = original_weights
              print("Running predictions for tile:", tile)
              subprocess.run([sys.executable, "C:/Users/dozhang/Documents/GitHub/greenearthnet/development/greenearthnet/test.py", 
                              config,
                              weights,
                              "--track", "ood-t_chopped",
                              "--pred_dir", predictions,
                              "--data_dir", dir], check=True)
    print("finished")