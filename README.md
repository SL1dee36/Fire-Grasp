### Fire-Grasp [ENG]
* **the program is designed to detect and track fires in real time.**


### Functionality:


* **Fire detection:** The program analyzes the video stream from the screen using a color segmentation algorithm in the HSV color space. This allows to select pixels corresponding to the color of the flame and ignore other elements of the image.
* **Contour detection:** After selecting fire pixels, the program applies morphological operations (dilation and erosion) to combine the individual pixels into a single segment. It then looks for contours on that segment to identify areas that are most likely to be fire. Contours are continuous lines that delineate the boundaries of detected objects.
* **Motion Tracking:** The program tracks the movement of the fire by analyzing the change in the position of the center of mass of each detected contour over time. This allows you to determine which way the fire is moving and visualize it on the screen.
* **Displaying the results:** The program visualizes the results of its work by superimposing fire contours on the original image. Additionally, it displays the direction of fire movement next to each outline. This allows the user to easily see where the fire is and how it is moving.
* **Additional features:**
* **Parameter settings:** The program allows you to manually adjust the range of colors that count as fire using sliders. This allows you to adapt the program to different lighting conditions and fire types.
* **Display modes:** The program allows you to select the mode of displaying fire contours: normal, squares or hexagons. This allows you to choose the most convenient way to visualize the results.
* **Debug Menu:** The program provides a debug menu that allows you to change parameters and display current values. This helps developers to test and improve the program.


### Technologies used:


* **OpenCV Image Processing:** The OpenCV (Open Source Computer Vision Library) library is used for image processing, including color space conversion, morphological operations, contour search, and rendering results. OpenCV provides a wide range of functions for working with images and video.
* **NumPy:** The NumPy library is used to work with arrays, allowing you to efficiently process image pixels and perform mathematical operations. NumPy provides convenient tools for working with multidimensional arrays, making it indispensable for image processing.
* **PyAutoGUI:** The PyAutoGUI library is used to capture screen shots that are then processed by a program. PyAutoGUI provides a simple way to interact with the operating system to capture screen shots and control the mouse and keyboard.

### Terms:


* **Color segmentation:** A method of selecting areas of an image based on their color. In this case, the HSV color space is used, which is better suited for color extraction than RGB.
* **Morphological operations:** Operations that are applied to binary images (black and white) to change their shape. Expansion enlarges areas by filling in neighboring pixels, and erosion reduces areas by removing outermost pixels.
* **Contours:** Continuous lines that delineate the boundaries of detected objects. Contours are used to define the shape and size of objects.
* **Center of mass:** A point that represents the center of gravity of an object. In this case, it is used to track the movement of the fire.


### Principle of operation:


1. **Capture an image:** The program takes a screenshot using PyAutoGUI.
2. **Color Space Conversion:** The image is converted from RGB to HSV to take advantage of color segmentation to highlight fire.
3. **Color segmentation:** The program creates a mask that selects pixels in a given range of colors that correspond to fire.
4. **Morphological operations:** The program applies morphological operations to combine fire pixels into a single segment.
5. **Search for contours:** The program searches for contours on the segment to identify areas that are likely to be fire.
6. **Motion Tracking:** The program tracks the changing position of each loop's center of mass over time to determine the direction of fire.
7. **Display results:** The program overlays fire outlines on the original image and displays the direction of fire movement next to each outline.


### Restrictions:


* The program is sensitive to changes in lighting and image quality.
* The program may not be effective in detecting fire in environments with many other moving objects.


### Potential applications:


* Fire early warning systems.
* Monitoring wildfires.
* Safety systems that detect fire and alert you to danger.
* Demonstration:


https://github.com/SL1dee36/Fire-Grasp/assets/84046495/9a460821-9231-4888-a2d4-ff5e93390cf7



This program demonstrates the capabilities of computer vision to solve real-time fire analysis and detection problems. It can be modified and extended to deal with different scenarios and conditions, for example, to deal with video streams from cameras or to process images from other sources.


The program may be ineffective at detecting fire in environments with many other objects with similar colors.
Potential applications:
Fire early warning systems.
Wildfire Monitoring.
Safety systems that detect fire and alert you to danger.
This program demonstrates the capabilities of computer vision to solve real-time fire analysis and detection problems. It can be modified and extended to deal with different scenarios and conditions, for example, to deal with video streams from cameras or to process images from other sources.
