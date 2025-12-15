#!/bin/bash
source /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/.venv/bin/activate 
cd /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches

echo "29TQF starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_sites/29TQF
echo "29TQF finished"

echo "30TWK starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_sites/30TWK
echo "30TWK finished"

echo "30UYU starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_sites/30UYU
echo "30UYU finished"

echo "31TBF starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_sites/31TBF
echo "31TBF finished"

echo "31UFP starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_sites/31UFP
echo "31UFP finished"

echo "32UNC starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_sites/32UNC
echo "32UNC finished"

echo "33UWT starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_sites/33UWT
echo "33UWT finished"

echo "33UXP starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_sites/33UXP
echo "33UXP finished"

echo "34SEJ starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_sites/34SEJ
echo "34SEJ finished"

echo "34TFL starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_sites/34TFL
echo "34TFL finished"
