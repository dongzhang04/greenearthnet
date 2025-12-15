#!/bin/bash
source /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/.venv/bin/activate 
cd /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches

echo "29SND starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/29SND
echo "29SND finished"

echo "29SPC starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/29SPC
echo "29SPC finished"

echo "29SQB starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/29SQB
echo "29SQB finished"

echo "29TPE starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/29TPE
echo "29TPE finished"

echo "29TQF starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/29TQF
echo "29TQF finished"

echo "30STJ starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/30STJ
echo "30STJ finished"

echo "30TTK starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/30TTK
echo "30TTK finished"

echo "30UYV starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/30UYV
echo "30UYV finished"

echo "31TBF starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/31TBF
echo "31TBF finished"

echo "32TML starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/32TML
echo "32TML finished"