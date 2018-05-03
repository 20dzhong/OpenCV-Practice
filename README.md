### bunch of files together for the sake for computer vision practice
# TODO List
> Look into canny edge detections and how it works

> detecting 3D shapes?

> Have a better understanding of NumPy, HSV and color manipulations

# Notes 
The most used color spacings in OpenCV are HSV and Grayscale

* Grayscale images are simply easier to work with, color increase the complexity of the model.
* RGB to HSV is used because HSV separates image intensity from color information (*luma* and *chroma*)
* HSV is easier to work with compared with RGB especially when it comes to working with shadows, the hue for HSV stays the same while RGB has different values

Edges are detected when there is a drop off between the values of the pixels
