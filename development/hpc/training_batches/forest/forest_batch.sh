#!/bin/bash -l
#SBATCH --export=USER,LOGNAME,HOME,MAIL,PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
#SBATCH --job-name=Forest_Max_Minicubes_4_gpu_GEN_train      
#SBATCH --output=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/forest/hpc_logs/%x-%j.out
#SBATCH --error=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/forest/hpc_logs/%x-%j.err
#SBATCH --mail-type=START,END,FAIL
#SBATCH --mail-user=dong.zhang@nrcan-rncan.gc.ca
#SBATCH --account=nrcan_geobase__gpu_a100
#SBATCH --partition=gpu_a100
#SBATCH --time=8:00:00
#SBATCH --qos=low
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-gpu=32
#SBATCH --mem-per-cpu=3G
#SBATCH --gpus-per-task=4
#SBATCH --comment="image=registry.maze.science.gc.ca/ssc-hpcs/generic-job:ubuntu22.04"

nvidia-smi

# load the CUDA toolkit
. ssmuse-sh -d hpco/exp/cuda-12.2.2
export PATH="/fs/ssm/hpco/exp/cuda-12.2.2/cuda_12.2.2_amd64-64/nvvm/bin:$PATH"
export http_proxy=http://webproxy.science.gc.ca:8888/
export https_proxy=http://webproxy.science.gc.ca:8888/

# activate environment
source /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/.venv/bin/activate 

cd /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/forest

echo "29SND starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_sites/29SND
echo "29SND finished"

echo "29TNE starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_sites/29TNE
echo "29TNE finished"

echo "30TTK starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_sites/30TTK
echo "30TTK finished"

echo "31TBF starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_sites/31TBF
echo "31TBF finished"

echo "31UFP starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_sites/31UFP
echo "31UFP finished"

echo "33UWT starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_sites/33UWT
echo "33UWT finished"

echo "33VVG starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_sites/33VVG
echo "33VVG finished"

echo "33VUF starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_sites/33VUF
echo "33VUF finished"

echo "33VUG starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_sites/33VUG
echo "33VUG finished"

echo "34SFF starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_sites/34SFF
echo "34SFF finished"

echo "34SEJ starting"
python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/forest_sites/34SEJ
echo "34SEJ finished"
