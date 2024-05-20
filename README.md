# Fire-Grasp: Detecting Fires in Real-Time

Fire-Grasp is an application designed to detect fires in real-time. It uses screenshots from your computer and image processing algorithms to determine the presence of fire.

### Libraries Used
* cv2: OpenCV library for image processing and video operations.
* numpy: Library for handling arrays of data.
* pyautogui: Library for automating GUI interactions.

## Installation
To install the application and the necessary libraries, follow these steps:

* Clone the repository:
  ```  git clone https://github.com/SL1dee36/Fire-Grasp.git  ```

* Navigate to the project directory:
  ```  cd Fire-Grasp  ```
  
* Install the necessary libraries:
  ```  pip install -r requirements.txt  ```

## Documentation
The application consists of several main modules, each performing its function. Here are some key features:

#### Debug Menu
The debug menu is a feature that allows you to adjust the parameters of the fire detection algorithm in real-time. This includes the lower and upper thresholds for the color range used to detect fire, as well as the display mode.

#### Display Modes
There are three display modes available:

  * Mode 0: This mode draws contours around the detected fire.
  * Mode 1: This mode draws a rectangle around the detected fire.
  * Mode 2: This mode draws a hexagon around the detected fire.

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


Changing Segment Size
```Python
from main import FireDetection

fd = FireDetection()
fd.segment_size = 4
fd.run()
```
In this example, we change the segment size before running the fire detection. This can be useful for adapting to different lighting conditions or image quality.


Please note that these examples are meant to illustrate the capabilities of the application. Depending on your needs, you can customize them to fit your specific goals.
