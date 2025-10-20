scripts and config used when running with the gpu on w-bsc-a157818
the only change to the scripts consist of deleting the 'strategy' field in the 'trainer' section of the config files
when testing, lightning would not accept 'auto' as a valid strategy so this was an alternative way to set the strategy to 'auto' 

the environment is set up with the gpu option outlined in 'development/greenearthnet/setup.txt'