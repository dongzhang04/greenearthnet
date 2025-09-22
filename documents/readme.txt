This directory contains survey papers that may provide context to the project. 
Summaries of the papers can be found below:


Benson, V. et al. Multi-modal learning for geospatial vegetation forecasting. In Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition 27788–27799 (IEEE, 2024).
- Contextformer architecture:
1. uses PVT v2 as the vision backbone for encoding spatial context with Sentinel 2 satellite imagery and elevation data, with elevation included as an additional channel to Sentinel 2's image channels
2. applies a cloud mask, a temporal positional encoding to indicate the timestep of a given token, and a weather embedding from the meteo encoder
3. processes the patch embedding with a temporal transformer, specifically Presto's transformer encoder
4. decodes the resulting embeddings with delta decoders which predict the change in NDVI from the last cloud free timestep, before computing the final NDVI value for each timestep by adding the respective delta with the last cloud free measure
5. the above process is done in parallel for all timesteps rather than iteratively, with step 4 applying only to timesteps 11-30 (or 1-20 if -9 is taken to be the oldest time step)

- during training, a MLM/MAE learning technique is employed, with two types of masks applied at an equal probability:
1. a random dropout mask which drops 70% of the patches from each of the timesteps in the range 3-30
2. an inference mask which drops all patches from timesteps 10 to 30, equivalent to the actual task

- the model's test sets are comprised of:
1. Train, a training set from the years 2017-2020
2. OOD-t test, the main test set containing locations near Train in the years 2021-2022, meant for temporal extrapolation
3. Val, a set containing the same locations as ODD-t test in the year 2020, allowing for early stopping 
4. OOD-s test, further locations outside training regions in the years 2017-2019, meant for spatial extrapolation
5. OOD-st test, the same locations as OOD-s in the years 2021-2022, meant for spatio-temporal extrapolation



Wang, W. et al. Pyramid Vision Transformer: A Versatile Backbone for Dense Prediction Without Convolutions. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 568–578, 2021. 2, 3
- developed a Transformer based model as opposed to convolutional neural networks (CNN) commonly found in computer vision
- well suited for high resolution downstream tasks, specifically image classification, object detection, and semantic segmentation
- embeds patches of 4x4 pixels and feeds whole images as sequences of patches into a Transformer encoder, allowing for a global receptive field as opposed to local receptive fields generated through convolutions which require further network depth to grow larger
- generates 4 levels of feature maps by using the first one as input for the next level, allowing for multi-scale feature maps similar to CNNs
- improves the multi-head attention layer in the Transformer encoder with a spatial reduction layer to lower computation and memory costs


Wang, W. et al. PVT v2: Improved baselines with Pyramid Vision Transformer. Computational Visual Media, 8(3):415–424, 2022.
- improves the original PVT model by:
1. improving the spatial reduction algorithm
2. allowing the overlapping of patches though the use of convolutions in order to better capture the local continuity of features
3. replaces the fixed-size position encoding when embedding patches with convolutions to allow for variable length position encodings, providing flexibility with different image resolutions/sizes 


He, K. et al. Masked Autoencoders Are Scalable Vision Learners. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 16000–16009, 2022.
- developed an effective self-supervised learning method (MAE) in which a model reconstructs images that had their patches randomly masked, similar to masked language modeling (MLM) in NLP


Tseng, G. et al. Lightweight, Pre-trained Transformers for Remote Sensing Timeseries. arxiv, 2304.14065, 2024.
- previous self-supervised models for remote sensing data commonly ignore the temporal dimension and treat data as single-timestep images, and often only consider a single satellite product as opposed to a multimodal approach
- the model developed in this paper (Presto) addresses these issues, resulting in a flexible model that can accommodate diverse input formats such as differences in input shapes and data, and perform effectively with missing inputs












