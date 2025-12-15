#!/bin/bash -l
#SBATCH --export=USER,LOGNAME,HOME,MAIL,PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
#SBATCH --job-name=C_4_gpu_GEN_train      
#SBATCH --output=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/%x-%j.out
#SBATCH --error=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/%x-%j.err
#SBATCH --mail-type=START,END,FAIL
#SBATCH --mail-user=dong.zhang@nrcan-rncan.gc.ca
#SBATCH --account=nrcan_geobase__gpu_a100
#SBATCH --partition=gpu_a100
#SBATCH --time=1-00:00:00
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

cd /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc

python ./train.py config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/crop_dominated
