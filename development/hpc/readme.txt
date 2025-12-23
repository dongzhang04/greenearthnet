This directory contains the code used on the HPC to perform retraining.

An environment for greenearthnet is created with venv instead anaconda, 
following the 'cuda (gpu enabled) install' instructions found in development\greenearthnet\setup.text,
replacing any conda install commands with pip install.
Note that installing pip-system-certs may raise some errors with later package installations and may need to be installed 
after all other packages have been installed 

The venv can be created as follows: 
first ensure you are connected to the slurm job scheduler by entering the command: ssh inter-nrcan-ubuntu2204.science.gc.ca
    this is because the python version may be different from the HPC account and will not be able to access the venv's packages properly
navigate to the desired directory: cd /gpfs/fs5/nrcan/nrcan_geobase/work/doz000/projects
in the terminal run the following commands:
    python3 -m venv .venv
    source .venv/bin/activate
    pip install ...
    ...
    deactivate 



The greenearthnet data was transferred to the HPC environment by tarring it on a workstation, 
before using 'scp' to copy the compressed folder to the HPC
classify_landcover was then run to sort the uncompressed greenearthnet folder's training data into the 3 landcover types


To run a training batch, first open training_batch/data.sh and enter the landcover type and tiles for which you wish to train on
Running training_batch/data.sh will then create and populate the proper folders to do individual training on. 
Modify training_batch/crop_training.sh, training_batch/forest_training.sh, and training_batch/shrub_training.sh to specify which tiles to train only
Running training_batch/batch_train.sh will queue each of the three landcover training shell scripts
the number of nodes is set to 3 in order to train all 3 landcover types in parallel, however job queue times may be long
each landcover training script will output logs to training_batchs/hpc_logs where the name of the retrained weights files are output 
the retrained weights will be output to the folder experiments/greenearthnet/contextformer/4_gpu/config_seed=42/checkpoints in the dierctory where sbatch was used to queue batch_train.sh
it is recommended to cd into training_batches before queueing a job

the crop, forest, and shrub folders found within training_batches contain code for training on a single site as opposed to batches of single sites
this training is done the same way as explained above

The retrained weights are then transferred to the workstation manually using scp