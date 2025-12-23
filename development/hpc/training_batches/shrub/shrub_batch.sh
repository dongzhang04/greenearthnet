#!/bin/bash -l
#SBATCH --export=USER,LOGNAME,HOME,MAIL,PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
#SBATCH --job-name=Shrub_Max_Minicubes_4_gpu_GEN_train      
#SBATCH --output=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/shrub/hpc_logs/%x-%j.out
#SBATCH --error=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/shrub/hpc_logs/%x-%j.err
#SBATCH --mail-type=START,END,FAIL
#SBATCH --mail-user=dong.zhang@nrcan-rncan.gc.ca
#SBATCH --account=nrcan_geobase__gpu_a100
#SBATCH --partition=gpu_a100
#SBATCH --time=2:00:00
#SBATCH --qos=low
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-gpu=32
#SBATCH --mem-per-cpu=3G
#SBATCH --gpus-per-task=4
#SBATCH --comment="image=registry.maze.science.gc.ca/ssc-hpcs/generic-job:ubuntu22.04"
#SBATCH --exclude=ib14gpu-002


nvidia-smi

# load the CUDA toolkit
. ssmuse-sh -d hpco/exp/cuda-12.2.2
export PATH="/fs/ssm/hpco/exp/cuda-12.2.2/cuda_12.2.2_amd64-64/nvvm/bin:$PATH"
export http_proxy=http://webproxy.science.gc.ca:8888/
export https_proxy=http://webproxy.science.gc.ca:8888/

# activate environment
source /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/.venv/bin/activate 

cd /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/shrub



# echo "29SND starting"
# python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/29SND
# echo "29SND finished"

# echo "29SPC starting"
# python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/29SPC
# echo "29SPC finished"

# echo "29SQB starting"
# python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/29SQB
# echo "29SQB finished"

# echo "29TPE starting"
# python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/29TPE
# echo "29TPE finished"

# echo "29TQF starting"
# python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/29TQF
# echo "29TQF finished"

# echo "30STJ starting"
# python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/30STJ
# echo "30STJ finished"

# echo "30TTK starting"
# python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/30TTK
# echo "30TTK finished"

# echo "30UYV starting"
# python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/30UYV
# echo "30UYV finished"

# echo "31TBF starting"
# python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/31TBF
# echo "31TBF finished"

# echo "32TML starting"
# python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/32TML
# echo "32TML finished"

# srun -N1 -n1 hostname

srun --nodes=1 --ntasks=1 --output=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/shrub/hpc_logs/%x-%j-31TBF.out --error=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/shrub/hpc_logs/%x-%j-31TBF.err bash -c 'echo "Running site 31TBF on $(hostname)"; python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/31TBF' &

srun --nodes=1 --ntasks=1 --output=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/shrub/hpc_logs/%x-%j-32TML.out --error=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/shrub/hpc_logs/%x-%j-32TML.err bash -c 'echo "Running site 32TML on $(hostname)"; python ./train.py /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/config/4_gpu/seed=42.yaml --data_dir /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/greenearthnet_data/shrub_sites/32TML' &

wait