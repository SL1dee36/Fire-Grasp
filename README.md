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


###Principle of operation:


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




### Огнехват [RUS]
* **программа предназначена для обнаружения и отслеживания пожаров в реальном времени.**

### Функциональные возможности:

* **Обнаружение огня:** Программа анализирует видеопоток с экрана, используя алгоритм цветовой сегментации в цветовом пространстве HSV. Это позволяет выделять пиксели, соответствующие цвету пламени, и игнорировать другие элементы изображения.
* **Определение контуров:** После выделения пикселей огня, программа применяет морфологические операции (расширение и эрозия), чтобы объединить отдельные пиксели в один сегмент. Затем она ищет контуры на этом сегменте, чтобы определить области, которые наиболее вероятно являются огнем. Контуры представляют собой непрерывные линии, очерчивающие границы обнаруженных объектов.
* **Отслеживание движения:** Программа отслеживает движение огня, анализируя изменение положения центра масс каждого обнаруженного контура с течением времени. Это позволяет определить, в какую сторону движется огонь, и визуализировать это на экране.
* **Отображение результатов:** Программа визуализирует результаты своей работы, накладывая контуры огня на исходное изображение. Дополнительно, она отображает направление движения огня рядом с каждым контуром. Это позволяет пользователю легко увидеть, где находится огонь и как он движется.
* **Дополнительные функции:**
    * **Настройка параметров:** Программа позволяет вручную настроить диапазон цветов, который считается огнем, используя слайдеры. Это позволяет адаптировать программу к различным условиям освещения и типам огня.
    * **Режимы отображения:** Программа позволяет выбрать режим отображения контуров огня: обычный, квадраты или гексагоны. Это позволяет выбрать наиболее удобный способ визуализации результатов.
    * **Дебаг-меню:** Программа предоставляет меню для отладки, позволяющее изменять параметры и выводить текущие значения. Это помогает разработчикам тестировать и улучшать программу.

### Используемые технологии:

* **Обработка изображений OpenCV:** Библиотека OpenCV (Open Source Computer Vision Library) используется для обработки изображений, включая преобразование цветового пространства, морфологические операции, поиск контуров и отрисовку результатов. OpenCV предоставляет широкий набор функций для работы с изображениями и видео.
* **NumPy:** Библиотека NumPy используется для работы с массивами, позволяя эффективно обрабатывать пиксели изображений и выполнять математические операции. NumPy предоставляет удобные инструменты для работы с многомерными массивами, что делает ее незаменимой для обработки изображений.
* **PyAutoGUI:** Библиотека PyAutoGUI используется для захвата снимков экрана, которые затем обрабатываются программой. PyAutoGUI предоставляет простой способ взаимодействия с операционной системой для получения снимков экрана и управления мышью и клавиатурой.

### Термины:

* **Цветовая сегментация:** Метод выделения областей изображения на основе их цвета. В данном случае используется цветовое пространство HSV, которое лучше подходит для выделения цветов, чем RGB.
* **Морфологические операции:** Операции, которые применяются к бинарным изображениям (черно-белым) для изменения их формы. Расширение увеличивает области, заполняя соседние пиксели, а эрозия уменьшает области, удаляя крайние пиксели.
* **Контуры:** Непрерывные линии, которые очерчивают границы обнаруженных объектов. Контуры используются для определения формы и размера объектов.
* **Центр масс:** Точка, которая представляет центр тяжести объекта. В данном случае используется для отслеживания движения огня.

### Принцип работы:

1. **Захват изображения:** Программа с помощью PyAutoGUI получает снимок экрана.
2. **Преобразование цветового пространства:** Изображение преобразуется из RGB в HSV, чтобы использовать преимущества цветовой сегментации для выделения огня.
3. **Сегментация цветов:** Программа создает маску, которая выделяет пиксели в заданном диапазоне цветов, соответствующих огню.
4. **Морфологические операции:** Программа применяет морфологические операции для объединения пикселей огня в один сегмент.
5. **Поиск контуров:** Программа ищет контуры на сегменте, чтобы определить области, которые, вероятно, являются огнем.
6. **Отслеживание движения:** Программа отслеживает изменение положения центра масс каждого контура с течением времени, чтобы определить направление движения огня.
7. **Отображение результатов:** Программа накладывает контуры огня на исходное изображение и отображает направление движения огня рядом с каждым контуром.

### Ограничения:

* Программа чувствительна к изменениям освещения и качеству изображения.
* Программа может быть неэффективна при обнаружении огня в условиях с большим количеством других движущихся объектов.

### Потенциальные приложения:

* Системы раннего предупреждения пожаров.
* Мониторинг лесных пожаров.
* Системы безопасности, которые обнаруживают огонь и оповещают об опасности.
* Демонстрация:


https://github.com/SL1dee36/Fire-Grasp/assets/84046495/9a460821-9231-4888-a2d4-ff5e93390cf7



Данная программа демонстрирует возможности компьютерного зрения для решения задач анализа и обнаружения огня в реальном времени. Она может быть модифицирована и расширена для работы с различными сценариями и условиями, например, для работы с видеопотоками с камер или для обработки изображений с других источников.

Программа может быть неэффективна при обнаружении огня в условиях с большим количеством других объектов, имеющих похожие цвета.
Потенциальные приложения:
Системы раннего предупреждения пожаров.
Мониторинг лесных пожаров.
Системы безопасности, которые обнаруживают огонь и оповещают об опасности.
Данная программа демонстрирует возможности компьютерного зрения для решения задач анализа и обнаружения огня в реальном времени. Она может быть модифицирована и расширена для работы с различными сценариями и условиями, например, для работы с видеопотоками с камер или для обработки изображений с других источников.
