# AI Information and Research Background
<html>
<head>
    <title>AniML Filtering Empty Images</title>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="../static/css/styles.css">
    <link rel="stylesheet" href="../static/css/mystyle.css">
    <link rel="stylesheet" href="../static/css/style3.css">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z"
        crossorigin="anonymous">
<h2> AniML - Model Background </h2>
</head>
</html>

<html>
<h3 align="left"> Model Decision and Background: </h3>

The network architecture of 
<font style="font-family: 'Poppins', sans-serif; color: blue; font-size: 1.1em; font-weight: 300; line-height: 1.7em">
[Yolov5](https://pytorch.org/hub/ultralytics_yolov5/#:~:text=YOLOv5%20%F0%9F%9A%80%20is%20a%20family,to%20ONNX%2C%20CoreML%20and%20TFLite.)
</font>, the algorithm used for the AniML AI model engine, consists of three parts:

<font style="font-family: 'Poppins', sans-serif; color: #999; font-size: 1.1em; font-weight: 300; line-height: 1.7em">

1. Backbone: CSPNet or CSPDarknet
2. Neck: PANet, and 
3. Head: Yolo Layer. 

</font>

The data are first input to CSPDarknet for feature extraction, and then fed to PANet for feature fusion. Finally, Yolov5 Layer outputs detection results, including the predicted class, confidence score for that class prediction, the bounding box location and size which encompassing the object of interest.

The scheme of the YOLOv5 Architecture as Convolutional Neural Network (CNN), in which the key parts are the BackBone, Neck and Head. 

<font style="font-family: 'Poppins', sans-serif; color: #999; font-size: 1.1em; font-weight: 300; line-height: 1.7em">

* BackBone CSPNet is used in order to extract features from the images which are used as input images. 
* Neck is used for the creation of pyramid feature. It helps the module on scaling factor of detected objects which are of the same nature but different scales. The technique which is used for creation of pyramid features is PANet. 
* Head is to apply anchor of different sizes on those features which are generated in the previous layers with value of probability as well as bounding box with score. 

</font>

Mask R-CNN is a state of the art model for instance segmentation, developed on top of Faster R-CNN. Faster R-CNN is a region-based convolutional neural networks [2], that returns bounding boxes for each object and its class label with a confidence score.

The default YoloV5 model was trained Common Object in Context 
<font style="font-family: 'Poppins', sans-serif; color: blue; font-size: 1.1em; font-weight: 300; line-height: 1.7em">
[(COCO)](https://cocodataset.org)
</font> dataset, which contains 80 different classes. AniML seeks to retrain the final layers of YoloV5 with some additional layers that are customized to an end users specific use case.

<center>
<h4>Convolutional Neural Network</h4>
<h5>Decision Layers for Computer Vision Object Detection</h5>
</center>
<img 
    style="display: block; 
           margin-left: auto;
           margin-right: auto;
           width: 100%;"
    src="../static/website_images/cnn_flow.png"
    alt="Our logo">
</img>

<h3>Further Background Reading</h3>
<h5>CNN Background:</h5>
    
CNN is a kind of Network architecture for deep-learning algorithms for identifying and recognizing objects (pixel data process). CNN leverages principles from linear algebra, such as matrix multiplication to identify patterns within an image and is highly suitable for image classification and CV applications with highly accurate results, especially when a lot of data is involved. i.e.  self-driving cars and facial recognition.

<h5>CNN Layers:</h5>   
The CNN learns the object's features in successive iterations as the object data moves through the CNN's many layers. This direct (and deep) learning eliminates the need for manual feature extraction (feature engineering).

A CNN can have multiple layers, each of layer learns to detect the different features of an input image. 
A filter or kernel is applied to each image to produce an output that gets progressively better and more detailed after each layer. As each filter activates certain features from the image, it does its work and passes on its output to the filter in the next layer.

Each layer learns to identify different features and the operations end up being repeated for dozens, hundreds or even thousands of layers. 

Finally, all the image data progressing through the CNN's multiple layers allow the CNN to identify the entire object.

<h5>CNN Applications:</h5>   
CNNs can be retrained for new recognition tasks and built on pre-existing networks and can be used for real-world applications without increasing computational complexities or costs.

<h5>Other CV Modeling Techniques:</h5>   

One type of an Artificial neural networks (ANNs) is a recurrent neural network (RNN) that uses sequential or time series data as input. It is suitable for applications involving NLP, language translation, speech recognition and image captioning.

</html>
