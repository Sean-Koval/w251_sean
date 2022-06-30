# Homework 6


This homework requires a Jetson device.  If you do not have a device, please just sumbit the HW answering just questions 2 and 3 from Part 1.


This homework covers some use of GStreamer and model optimization.  It builds on the week 6 lab and completing the lab first is hightly recommended.   

This is an ungraded assignment

## Part 1: GStreamer

1. In the lab, you used the Ndida sink nv3dsink; Nvidia provides a another sink, nveglglessink.  Convert the following sink to use nveglglessink.
```
gst-launch-1.0 v4l2src device=/dev/video0 ! xvimagesink
```

2. What is the difference between a property and a capability?  How are they each expressed in a pipeline?

Properties describe a pad type (direction and availability). Differing forms of availability include Always, Sometimes, and on request. Properties control how an element acts. 

Capabilities are used used in both pads and pad templates. They provide information about the type of information that will be streamed over the pad. For a pad, they can be the form of a list of possible pads (not yet negotiated) or it lists the type of media that is already being streamed over the pad (negotiated). Capabilities are represented as either 1 or more within an array attached to the pad. These can be used to descibe metadata related to the media being streamed.  




3. Explain the following pipeline, that is explain each piece of the pipeline, desribing if it is an element (if so, what type), property, or capability.  What does this pipeline do?

```
gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw, framerate=30/1 ! videoconvert ! agingtv scratch-lines=10 ! videoconvert ! xvimagesink sync=false
```

- gst-launch-1.0: Runs the Gstreamer pipeline
- v412src: video source element(could be for a camera)
- device=/dev/video0: Property sets device location to /dev/video0
- video/x-raw: Capability sets video output to x-raw
- framerate=30/1: Capabilility sets frame rate to 30/1
- videoconvert: Filter element. Converts the video
- agingtv: Filter element
- scratch-lines=10 Component of filter element describing the lines of the age filter
- videoconvert: Filter element that converts video format
- xvimagesink: Sink element. This is the location of the video output
- sync=false: Property is going to prevent from syncing with the clock of the computer and will instead push the image to the display. 



4. GStreamer pipelines may also be used from Python and OpenCV.  For example:
```
import numpy as np
import cv2

# use gstreamer for video directly; set the fps
camSet='v4l2src device=/dev/video0 ! video/x-raw,framerate=30/1 ! videoconvert ! video/x-raw, format=BGR ! appsink'
cap= cv2.VideoCapture(camSet)

#cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
```
In the lab, you saw how to stream using Gstreamer.  Using the lab and the above example, write a Python application that listens for images streamed from a Gstreamer pipeline.  You'll want to make sure your image displays in color.

For part 1, you'll need to submit:
- Answer to question 1
- Answer to question 2
- Answer to question 3
- Source code and Gstreamer "server" pipeline used.


## Part 2: Model optimization and quantization

In lab, you saw to how use leverage TensorRT with TensorFlow.  For this homework, you'll look at another way to levarage TensorRT with Pytorch via the Jetson Inference library (https://github.com/dusty-nv/jetson-inference).

You'll want to train a custom image classification model, using either the fruit example or your own set of classes.

Like in the lab, you'll want to first baseline the your model, looking a the number of images per second it can process.  You may train the model using your Jetson device and the Jetson Inference scripts or train on a GPU eanabled server/virtual machine.  Once you have your baseline, follow the steps/examples outlined in the Jetson Inference to run your model with TensorRT (the defaults used are fine) and determine the number of images per second that are processed.

You may use either the container apporach or build the library from source.

For part 2, you'll need to submit:
- The base model you used
- A description of your data set
- How long you trained your model, how many epochs you specified, and the batch size.
- Native Pytorch baseline
- TensorRT performance numbers


### Setting up `jetson-inference` container 
- [Source](https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-docker.md)

```
$ git clone --recursive https://github.com/dusty-nv/jetson-inference
$ cd jetson-inference
$ docker/run.sh
```
**1. The base model used that was trained using Jetson device and Jetson Inference scripts:**

**Answer:**

`mobilenet-v1-ssd-mp-0_675.pth`

### Train on fruit example 
- [Source](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-ssd.md)

**2. A description of your dataset**

**Answer:**

`fruit` dataset was used with 8 classes of fruits.
- Apple
- Orange
- Banana
- Strawberry
- Grape
- Pear
- Pineapple
- Watermelon

There are 6360 total images. The commands and statistics distribution for the train/validation/test datasets are displayed below:

```
$ cd jetson-inference/python/training/detection/ssd
$ python3 open_images_downloader.py --stats-only --class-names "Apple,Orange,Banana,Strawberry,Grape,Pear,Pineapple,Watermelon" --data=data/fruit
```

### Download and train fruit dataset
```
# Download train dataset
$ python3 open_images_downloader.py --class-names "Apple,Orange,Banana,Strawberry,Grape,Pear,Pineapple,Watermelon" --data=data/fruit
```

```
# Begin training
python3 train_ssd.py --data=data/fruit --model-dir=models/fruit --batch-size=4 --epochs=30
```

**3. How long did it take to train the model, how many epochs were specified and batch size.**

**Answer:**

| Number of Epochs | Batch Size |
|------------------|------------|
| 30               | 4          |

These are examples of image outputs based on the model:

![image](jetson-inference/python/training/detection/ssd/fruit_310.jpg) 
![image](jetson-inference/python/training/detection/ssd/fruit_325.jpg)



**4. Native Pytorch baseline**

```
# batch size = 1
python3 valid_ssd.py --data=data/fruit --model-dir=models/fruit --resume=models/fruit/mb1-ssd-Epoch-28-Loss-3.7590008989424155.pth --batch-size=1 --epoch=1

# batch size = 4
python3 valid_ssd.py --data=data/fruit --model-dir=models/fruit --resume=models/fruit/mb1-ssd-Epoch-28-Loss-3.7590008989424155.pth --batch-size=4 --epoch=1

# 233it [01:05,  3.58it/s]
```



**Answer:**

`930it [01:17, 12.05it/s]`
- 12.05 images/sec after a run on 930 images


**5. TensorRT performance numbers**

### Converting the model to ONNX to be loaded with TensorRT
```
python3 onnx_export.py --model-dir=models/fruit
```
This will save a model called `ssd-mobilenet.onnx` under `jetson-inference/python/training/detection/ssd/models/fruit/`


### Processing Images with TensorRT
```
IMAGES=/jetson-inference/python/training/detection/ssd/data/fruit/test

# save images
# using /usr/local/bin/detectnet.py
detectnet.py --model=models/fruit/ssd-mobilenet.onnx --labels=models/fruit/labels.txt \
          --input-blob=input_0 --output-cvg=scores --output-bbox=boxes \
            "$IMAGES/*.jpg" $IMAGES/test/fruit_%i.jpg
            
# use this command for faster runtime
# does not save images
# using /jetson-inference/python/training/detection/ssd/detectnet.py
./detectnet.py --headless --model=models/fruit/ssd-mobilenet.onnx --labels=models/fruit/labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes "$IMAGES/*.jpg"
```

Pytorch model uses FP32 and TensorRT model uses FP16. Thus, the optimized model is quantized.

```
[TRT]    detected model format - ONNX  (extension '.onnx')
[TRT]    desired precision specified for GPU: FASTEST
[TRT]    requested fasted precision for device GPU without providing valid calibrator, disabling INT8
[TRT]    [MemUsageChange] Init CUDA: CPU +198, GPU +0, now: CPU 222, GPU 2282 (MiB)
[TRT]    native precisions detected for GPU:  FP32, FP16
[TRT]    selecting fastest native precision for GPU:  FP16
[TRT]    attempting to open engine cache file models/fruit/ssd-mobilenet.onnx.1.1.8001.GPU.FP16.engine
[TRT]    loading network plan from engine cache... models/fruit/ssd-mobilenet.onnx.1.1.8001.GPU.FP16.engine
[TRT]    device GPU, loaded models/fruit/ssd-mobilenet.onnx
```

**Answer:**

- Total Images: 930
- Total Time Taken: 161.00596046447754
- Images/sec: 5.776183672437297
