This directory contains the code used on the HPC to perform retraining.

An environment for greenearthnet is created with venv instead anaconda, 
following the 'cuda (gpu enabled) install' instructions found in development\greenearthnet\setup.text,
replacing any conda install commands with pip install.
Note that installing pip-system-certs may raise some errors with later installs and may need to be installed 
after all other packages have been installed 

The greenearthnet data was transferred to the HPC environment by tarring it on a workstation, 
before using 'scp' to copy the compressed folder to the HPC

Similarly, retrained weights are copied from the HPC to the wokrstation using 'scp' 