Benson, V. et al. Multi-modal learning for geospatial vegetation forecasting. In Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition 27788–27799 (IEEE, 2024).


Wang, W. et al. Pyramid Vision Transformer: A Versatile Backbone for Dense Prediction Without Convolutions. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 568–578, 2021. 2, 3
- developed a Transformer based model, well suited for high resolution tasks, as opposed to convolutional neural networks (CNN) commonly found in computer vision
- embeds patches of 4x4 pixels and feeds whole images as sequences of patches into a Transformer encoder, allowing for a global receptive field as opposed to local receptive fields generated through convolutions which require further network depth to grow larger
- generates 4 levels of feature maps by using the first one as input for the next level, allowing for multi-scale feature maps similar to CNNs
- improves the multi-head attention layer in the Transformer encoder with a spatial reduction layer to lower computation and memory costs


Wang, W. et al. PVT v2: Improved baselines with Pyramid Vision Transformer. Computational Visual Media, 8(3):415–424, 2022.
- improves the original PVT model by:
	1. improving the spatial reduction algorithm
	2. allowing for overlapping patches to better capture the local continuity of features through convolutions
	3. enhances the fixed position encoding when embedding patches with convolutions to allow for more flexibility with image sizes 


He, K. et al. Masked Autoencoders Are Scalable Vision Learners. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 16000–16009, 2022.