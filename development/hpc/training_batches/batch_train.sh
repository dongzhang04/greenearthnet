#!/bin/bash -l
#SBATCH --export=USER,LOGNAME,HOME,MAIL,PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
#SBATCH --job-name=3_node_4_gpu_30_sites_GEN_train     
#SBATCH --output=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/hpc_logs/%x-%j.out
#SBATCH --error=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/hpc_logs/%x-%j.err
#SBATCH --mail-type=START,END,FAIL
#SBATCH --mail-user=dong.zhang@nrcan-rncan.gc.ca
#SBATCH --account=nrcan_geobase__gpu_a100
#SBATCH --partition=gpu_a100
#SBATCH --time=1-00:00:00
#SBATCH --qos=low
#SBATCH --nodes=3
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

cd /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches

chmod +x crop_training.sh forest_training.sh shrub_training.sh

srun --exclusive --nodes=1 --ntasks=1 --output=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/hpc_logs/%x-%j-crop.out --error=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/hpc_logs/%x-%j-crop.err bash -c 'echo "Running crop training on $(hostname)"; ./crop_training.sh' &
srun --exclusive --nodes=1 --ntasks=1 --output=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/hpc_logs/%x-%j-forest.out --error=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/hpc_logs/%x-%j-forest.err bash -c 'echo "Running forest training on $(hostname)"; ./forest_training.sh' &
srun --exclusive --nodes=1 --ntasks=1 --output=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/hpc_logs/%x-%j-shrub.out --error=/gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects/fork/development/hpc/training_batches/hpc_logs/%x-%j-shrub.err bash -c 'echo "Running shrub/grassland training on $(hostname)"; ./shrub_training.sh' &

wait


