# Fire-Grasp: Detecting Fires in Real-Time

Fire-Grasp is an application designed to detect fires in real-time. It uses screenshots from your computer and image processing algorithms to determine the presence of fire.

### Libraries Used
- **cv2:** OpenCV library for image processing and video operations.
- **numpy:** Library for handling arrays of data.
- **pyautogui:** Library for automating GUI interactions.

## Installation
To install the application and the necessary libraries, follow these steps:

- Clone the repository:
  ```Console
  git clone https://github.com/SL1dee36/Fire-Grasp.git 

- Navigate to the project directory:
  ```Console
  cd Fire-Grasp 
  
- Install the necessary libraries:
  ```Console
  pip install -r requirements.txt 

## [Documentation](https://sl1dee36.github.io/page2.html#header01-1z)
The application consists of several main modules, each performing its function. Here are some key features:

  #### Debug Menu
  The debug menu is a feature that allows you to adjust the parameters of the fire detection algorithm in real-time. This includes the lower and upper thresholds for the color range used to detect fire, as well as the display mode.

  #### Display Modes
  There are three display modes available:

  - Mode 0: This mode draws contours around the detected fire.
  - Mode 1: This mode draws a rectangle around the detected fire.
  - Mode 2: This mode draws a hexagon around the detected fire.
  
  You can add more display and/or output options as well

  #### Parameters of processing of the received data 
  - **KERNEL_SIZE:** This is the size of the kernel used for dilatation and erosion operations. A kernel is simply a matrix of a certain size that OpenCV uses to perform these operations. In your case, KERNEL_SIZE = (1, 1), which means that the kernel is a 1x1 matrix.
  
  - **DILATE_ITERATIONS:** This is the number of dilate iterations OpenCV will perform on the image. Dilation is the process of increasing the size of objects in an image. In your case, DILATE_ITERATIONS = 10, which means that OpenCV will perform 10 dilatation iterations on the image.
  
  - **ERODE_ITERATIONS:** This is the number of erosion iterations that OpenCV will perform on the image. Erosion is the process of reducing the size of objects in an image. In your case, ERODE_ITERATIONS = 50, which means that OpenCV will perform 50 iterations of erosion on the image.

You can use these parameters to customize the fire detection algorithm. Changing `KERNEL_SIZE` can affect the size of objects that the algorithm can detect. Increasing `DILATE_ITERATIONS` can help the algorithm detect larger objects, while increasing `ERODE_ITERATIONS` can help the algorithm detect smaller objects. However, care should be taken as too large values can lead to excessive dilatation or erosion, which can skew the results. Experimenting with these parameters can help you find the optimal settings for your particular application.
  

## Video Demonstration

https://github.com/SL1dee36/Fire-Grasp/assets/84046495/adc824c6-3195-4cdd-be09-4cef6ea8217a


## Usage Examples
Here are some examples of how to use the application:

Fire Detection
```Python
from main import FireDetection

fd = FireDetection()
fd.run()
```
In this example, we create an instance of the FireDetection class and run it. This will start the fire detection process.


Changing Segment and Kernel sizes
```Python
from main import FireDetection

fd = FireDetection()
fd.SEGMENT_SIZE = 4
fd.KERNEL_SIZE = (1,1)
fd.run()
```
In this example, we change the segment & Kernel size before running the fire detection. This can be useful for adapting to different lighting conditions or image quality.


Please note that these examples are meant to illustrate the capabilities of the application. Depending on your needs, you can customize them to fit your specific goals.
