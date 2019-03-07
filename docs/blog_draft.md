

Pneumonia Lungfish
==============================================


### MASK RCNN

In this post we’ll use Mask R-CNN to build a model that takes chest X-Ray images as input and outputs a bounding box and a mask that segments lung opacities in the image.

We’ll use the train and dev datasets provided by the Kaggle RSNA Challenge competition as well as the great Mask R-CNN implementation library by [Matterport](Link to code in github: https://github.com/gabrielgarza/Mask_RCNN).


One of the most exciting applications of deep learning is the ability for machines to understand images. Fei-Fei Li has referred to this as giving machines the “ability to see”.
### What are Covered?
* Problems in medical imaging detection
* Model
* Transfer learning
* Inference results
* How will Ocean Protocol impact medical imaging detection?
* Dash (optional)

## I. Problems in medical imaging detection
* Domain specific

* Gap in knowledge and service

* Data sharing

* Machine learning




## II. Model
### What is MASK R-CNN?
Mask R-CNN is an instance segmentation model that allows us to identify pixel wise location for our class. “Instance segmentation” means segmenting individual objects within a scene, regardless of whether they are of the same type — i.e, identifying individual cars, persons, etc. Check out the below GIF of a Mask-RCNN model trained on the COCO dataset. As you can see, we can identify [pixel locations for cars, persons, fruits, etc].(https://www.analyticsvidhya.com/blog/2018/07/building-mask-r-cnn-model-detecting-damage-cars-python/)
)

#### How is  MASK R-CNN implemented?
Python 3, Keras, and TensorFlow.
#### What does MASK R-CNN do?
The model generates **bounding boxes** and **segmentation masks** for each instance of an object in the image. It's based on Feature Pyramid Network (FPN) and a ResNet101 backbone.


#### What is the model Architecture of MASK R-CNN?
* Backbone model: a standard convolutional neural network that serves as a feature extractor. For example, it will turn a1024x1024x3 image into a 32x32x2048 feature map that serves as input for the next layers.
  * I used RESNET 50
* Region Proposal Network (RPN): Using regions defined with as many as 200K anchor boxes, the RPN scans each region and predicts whether or not an object is present. One of the great advantages of the RPN is that does not scan the actual image, the network scans the feature map, making it much faster.
* Region of Interest Classification and Bounding Box: In this step the algorithm takes the regions of interest proposed by the RPN as inputs and outputs a classification (softmax) and a bounding box (regressor).
* Segmentation Masks: In the final step, the algorithm the positive ROI regions are taken in as inputs and 28x28 pixel masks with float values are generated as outputs for the objects. During inference, these masks are scaled up.

## III. Transfer learning

Instead of replicating the entire algorithm based on the research paper, we’ll use the awesome Mask R-CNN library that Matterport built.

* generate our train and dev sets


* Load data the into the library,
  * I added a DetectorDataset.py in src/data


* Setup our training environment in AWS for training


  The first thing we did is create a Deep Learning AMI configured for AWS Batch that uses nvidia-docker following this AWS Guide.



* Use transfer learning to start training from the coco pre-trained weights
  * here I need to write a train.sh
  * Initial run using coco weights  
  ```  
  python3 ./pneumonia.py train --dataset=./datasets --weights=coco
```
  * Continue training  
```  
python3 ./pneumonia.py train --dataset=./datasets --weights=last
```

  * Explain:   train.sh -> loads latest weights, runs the train command python3 ./pneumonia.py train --dataset=./datasets --weights=last


* Tune our model to get good results.
  * Here I add a file, need to add more codes

    ```
  DetectorConfig.py in src/config
  ```
  * **Parameters to turn**

    * RPN_ANCHOR_SCALES = (64, 96, 128, 256, 512)  
    * Turn weight decay (This affect L2 strength and is a good way of preventing overfitting. Please try 0.01, 0.005 and 0.001 first, then try more precisely.)

    * Freeze some layers and train part of layers in Resnet like resnet4+.

  * Settings of the network
    * RPN only



## IV. Inference
* *Here I need to write a predict.sh*  
  ```
  bash predict.sh
  ```
* the predict.sh will use a file
```
  src/config/InferenceConfig.py
```

*  need to complete the codes
* format of my result File

* The inference time in MASK R-CNN is ?s?? per image.

* Qualitative Results

## V. How will Ocean Protocol impact medical imaging detection?


## VI. Interactive dash (optional)
---

#### Images to use

Mask R-CNN framework for instance segmentation. Source: https://arxiv.org/abs/1703.06870  

[Semantic Segmentation vs Instance Segmentation](https://towardsdatascience.com/review-deepmask-instance-segmentation-30327a072339)

#### References
[Mask R-CNN](https://arxiv.org/pdf/1703.06870.pdf)
(https://github.com/facebookresearch/Detectron)

[Coco dataset](http://mscoco.org/home/)

[Understand difference b/w instance segmentation and semantic segmentation](https://stackoverflow.com/questions/33947823/what-is-semantic-segmentation-compared-to-segmentation-and-scene-labeling)

[Good tutorial of MASK R-CNN](https://www.youtube.com/watch?v=UdZnhZrM2vQ&t=111s)

#### Terms
 * Image Classification: Classify the main object category within an image.

 * Object Detection: Identify the object category and locate the position using a bounding box for every known object within an image.

 * Semantic Segmentation: Identify the object category of each pixel for every known object within an image. Labels are class-aware.

 * Instance Segmentation: Identify each object instance of each pixel for every known object within an image. Labels are instance-aware.
 Reference


  * Faster R-CNN: a model predicts bounding boxes

  * Mask R-CNN: a model predicts bounding boxes and object masks in parallel.
