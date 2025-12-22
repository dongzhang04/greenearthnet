This directory contains changes made to earthnet_models_pytorch in order to train Contextformer properly

in data/__init__.py, the 'greenearthnet' entry in METRIC_CHECKPOINT_INFO must be changed from veg-score to RMSE_Veg with mode min instead of max
in task/workflow.py, between lines 80-85, under the function 'add_task_specific_args', the line 
            parser.add_argument("--metric", type=str, default="NNSE") must be changed to 
            parser.add_argument("--metric", type=str, default="RMSE")