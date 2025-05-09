# Sobel Edge Detector

## Description
This project contains a script to execute and visualize 
the steps of a Sobel Edge Detector (SED). A SED estimates
the gradient of each pixel in an image in order to
create an 'outline' of an image. 

![myplot](https://github.com/user-attachments/assets/f4fc18a6-3fa1-4f93-9bdf-1e2dcdf46b5d)

## Installation & Use
1. Clone the repository by copying the HTTPS link into 
the IDE of your choice.
2. Add images to the '/images' folder (optional)
3. Change the address ```'images/YOUR_IMAGE.png'```
on line 5 in the file 'filter.py' to your image's location
4. Run the 'filter.py' file

## Edge Detection
Imagine you had an image where each pixel's intensity was 
defined by the function F(x). In order to find where the color
of that image was changing, all you would need to do is find 
where the change in F(x) was largest. Those places would be 
the outline of that image.

Unfortunately, images don't come with their own functions, 
so we have to estimate the gradient by assessing the change 
in both the X and Y directions over a 3x3 area of pixels. 
Doing this across the entire image forms an array representing
the estimated amount of change for each pixel.

The values of this array are then normalized from (0-255) and
turned back into an image.

## Otsu's Method
With the base method of edge detection, images often are muted.
In order to reduce noise and make the edge more vivid, this script
employs Otsu's Method. Otsu's Method calculates the threshold 
value (somewhere between 0-255) that maximizes between
class variation. This threshold can then be used to create
a binary array, where locations of low change are black (0),
and locations of high change are white (1), while avoiding
the noise caused by SED alone.
