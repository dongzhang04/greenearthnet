folders no longer in use:
leaf 
predictions
qgis
replicated_minicubes
training

To run metrics and treatment (blocking and hallucination) predictions go to the 'tools' folder.
Predicitions can also be ran in the greenearthnet environment like so:
predictions - python test.py E:\DZ\model_configs\contextformer\contextformer16M\seed=42.yaml E:\DZ\model_weights\contextformer\contextformer16M\seed=42.ckpt --track ood-t_chopped --pred_dir E:\DZ\predictions --data_dir E:\DZ\greenearthnet

notebook.ipynb can be used for any miscellaneous tasks like viewing minicubes/predictions and working with the data.