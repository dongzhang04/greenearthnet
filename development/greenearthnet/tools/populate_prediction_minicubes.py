import os
import shutil
crop = {
    "29TQF": r"E:\DZ\crop_dominated\ood-t_chopped\minicube_19_29TQF_40.87_-5.90_f0.02_c0.64_s0.34.nc",
    # r"E:\DZ\crop_dominated\ood-t_chopped\minicube_28_30TWK_39.82_-2.94_f0.00_c0.92_s0.02.nc",
    "30UYU": r"E:\DZ\crop_dominated\ood-t_chopped\minicube_54_30UYU_47.92_1.08_f0.16_c0.69_s0.11.nc",
    "31TBF": r"E:\DZ\crop_dominated\ood-t_chopped\minicube_61_31TBF_41.20_-0.55_f0.01_c0.80_s0.03.nc",
    "31UFP": r"E:\DZ\crop_dominated\ood-t_chopped\minicube_88_31UFP_48.47_4.66_f0.24_c0.56_s0.19.nc",
    "32UNC": r"E:\DZ\crop_dominated\ood-t_chopped\minicube_121_32UNC_52.09_10.49_f0.27_c0.65_s0.06.nc",
    "33UWT": r"E:\DZ\crop_dominated\ood-t_chopped\minicube_168_33UWT_51.61_15.92_f0.03_c0.75_s0.18.nc",
    "33UXP": r"E:\DZ\crop_dominated\ood-t_chopped\minicube_171_33UXP_47.84_16.88_f0.02_c0.83_s0.13.nc",
    "34SEJ": r"E:\DZ\crop_dominated\ood-t_chopped\minicube_199_34SEJ_39.49_21.83_f0.13_c0.70_s0.09.nc"
    # r"E:\DZ\retraining\TrainingData\crop_dominated\train\34TFL\34TFL_2017-07-14_2017-12-10_3385_3513_2105_2233_52_132_32_112_f0.00_c0.96_s0.01.nc" - need to make new minicube
}


forest = {
    # r"E:\DZ\forest_dominated\ood-t_chopped\minicube_11_29TNE_39.87_-8.73_f0.79_c0.00_s0.16.nc",
    "30TTK": r"E:\DZ\forest_dominated\ood-t_chopped\minicube_25_30TTK_40.30_-5.51_f0.49_c0.00_s0.48.nc",
    # r"E:\DZ\retraining\TrainingData\forest_dominated\train\31TBF\31TBF_2017-10-09_2018-03-07_3641_3769_2233_2361_56_136_34_114_f0.93_c0.01_s0.05.nc",
    # r"E:\DZ\retraining\TrainingData\forest_dominated\train\31UFP\31UFP_2018-04-04_2018-08-31_3257_3385_1465_1593_50_130_22_102_f0.97_c0.02_s0.01.nc",
    "33UWT": r"E:\DZ\forest_dominated\ood-t_chopped\minicube_169_33UWT_51.93_15.97_f0.86_c0.05_s0.09.nc",
    # r"E:\DZ\forest_dominated\ood-t_chopped\minicube_187_33VVG_59.54_14.81_f0.95_c0.01_s0.02.nc",
    # r"E:\DZ\forest_dominated\ood-t_chopped\minicube_179_33VUF_59.25_13.11_f0.80_c0.00_s0.02.nc",
    # r"E:\DZ\forest_dominated\ood-t_chopped\minicube_183_33VUG_60.04_12.05_f0.94_c0.03_s0.02.nc",
    "34SFF": r"E:\DZ\forest_dominated\ood-t_chopped\minicube_200_34SFF_36.97_22.64_f0.56_c0.00_s0.38.nc",
    "34SEJ": r"E:\DZ\forest_dominated\ood-t_chopped\minicube_198_34SEJ_39.24_21.03_f0.54_c0.00_s0.01.nc"
}


shrub = {
    "29SND": r"E:\DZ\shrub_dominated\ood-t_chopped\minicube_2_29SND_38.90_-8.35_f0.13_c0.00_s0.86.nc",
    "29SPC": r"E:\DZ\shrub_dominated\ood-t_chopped\minicube_3_29SPC_38.68_-7.65_f0.05_c0.01_s0.92.nc",
    "29TQF": r"E:\DZ\shrub_dominated\ood-t_chopped\minicube_20_29TQF_40.81_-5.66_f0.25_c0.01_s0.70.nc",
    # r"E:\DZ\shrub_dominated\ood-t_chopped\minicube_26_30TTK_39.70_-6.41_f0.00_c0.01_s0.95.nc",
    "30STJ": r"E:\DZ\shrub_dominated\ood-t_chopped\minicube_23_30STJ_39.19_-5.73_f0.00_c0.19_s0.79.nc",
    # r"E:\DZ\retraining\TrainingData\shrub_dominated\train\30UYV\30UYV_2018-04-20_2018-09-16_2745_2873_1465_1593_42_122_22_102_f0.15_c0.04_s0.81.nc" - need to make new minicube,
    # r"E:\DZ\retraining\TrainingData\shrub_dominated\train\31TBF\31TBF_2017-12-18_2018-05-16_4793_4921_953_1081_74_154_14_94_f0.12_c0.09_s0.76.nc" - need to make new minicube,
    "32TML": r"E:\DZ\shrub_dominated\ood-t_chopped\minicube_92_32TML_41.11_9.03_f0.29_c0.01_s0.65.nc",
    "34SFF": r"E:\DZ\shrub_dominated\ood-t_chopped\minicube_201_34SFF_36.66_22.89_f0.36_c0.01_s0.55.nc",
    "34TCL": r"E:\DZ\shrub_dominated\ood-t_chopped\minicube_203_34TCL_41.47_19.52_f0.04_c0.17_s0.54.nc"
}

sites = {"Crop": crop, "Forest": forest, "Shrub": shrub}
path = "E:/DZ/retraining"

if __name__ == "__main__":
    for key in sites:
        print("Processing land cover type:", key)
        for tile in sites[key]:
            print(tile)
            dir = path + f"/{key}/{tile}/ood-t_chopped/MJJ21" 
            os.makedirs(dir, exist_ok=True)

            file = sites[key][tile]
            print(f"Copying {file} to {dir}")
            shutil.copy(file, dir + "/")
            print("Copied")
    print("finished")