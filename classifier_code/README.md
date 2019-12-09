# Classifier Code

We used two approaches for classifying distracted driving videos: 
1. Image classifiers
2. Video classifiers

## Image classifiers

### Installation

We utilize the [fastai](https://www.fast.ai/) version 0.7 codebase for training our image classifiers. In order to install the same, look at the tutorial given [here](https://forums.fast.ai/t/fastai-v0-7-install-issues-thread/24652).

### Approach / Code

We use transfer learning to perform image classification on the individual frames of a video. We try different types of frame splitting approaches such as 

1. random splitting
2. One Frame per sec of video
3. All frames of the video.

The folders rf, 1f & af represent the above frame splitting strategies respectively. 

We also experiment with 3 different types of classifiers namely:

1. ResNet34
2. ResNeXt50
3. WideResNet50

The `frame_split.py` file within each of the three folders rf, 1f and af is used for splitting the videos in a given directory into frames. To, use this code, just replace the directory names/path within the code.

The files `resnet34-classifier.py`, `resnext-classifier.py` and `wrn-classifier.py` classifier consists of code for the three classifiers respectively. 

### INFER Pipeline
The `infer_pipeline` directory consists of a set of scripts that perform the whole pipeline of image classification as follows:

1. Download the videos from google drive and 
2. Extract the tar files
3. Perform image classification

## Video classification

The video classification was done using the 3D Resnet code provided [here](https://github.com/kenshohara/3D-ResNets-PyTorch). We used the ResNet-34 and the ResNeXt-101 models trained on the Kinetics dataset for our classification task. We again leverage transfer learning to improve the prediction accuracy for our task. 

If you are using this code or the pre-trained models, please cite this paper:

```tex
@inproceedings{hara3dcnns,
  author={Kensho Hara and Hirokatsu Kataoka and Yutaka Satoh},
  title={Can Spatiotemporal 3D CNNs Retrace the History of 2D CNNs and ImageNet?},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  pages={6546--6555},
  year={2018},
}
```

To train the network, please follow the instructions given in the original [repository](https://github.com/kenshohara/3D-ResNets-PyTorch). 

## Dataset

The train/test and holdout testset splits are given in the folder `train_test_split`. The file `train.csv` contains the training data, `test.csv` contains the testing data and `test-gt.csv` contains the fround truth for the test set.

The whole training and holdout test dataset itself is uploaded at this [link](https://rebrand.ly/distracted-driving-dataset).