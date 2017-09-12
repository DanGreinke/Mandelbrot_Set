# Mandelbrot_Set
Computes mandelbrot set, saves file containing coordinates and number of iterations for 
sampled points, reads file and generates image of Mandelbrot Set. Pixels assumed to be
part of the Mandelbrot set are colored black. All other pixels are assigned black body
color temperatures according to the number of iterations associated with that point.
Pixels with fewer iterations are more reddish, and pixels with larger numbers of 
iterations are bluish.

Credit to Tanner Helland for the algorithm used to assign the RGB values associated
with the color temperatures of a black body.
http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/

1) This script uses python 3.6.2, which can be downloaded here: 
https://www.python.org/downloads/

2) You will need to install PIP to download Pillow, a requisite module for this script.
https://pip.pypa.io/en/stable/installing/

3) Download Pillow. Type the following into the command prompt (windows users):
py -m pip install Pillow

4) Finally, you will need to adjust the file path in the source code for your computer.
Other parameters, such as x_res, y_res, center, and half_width may be adjusted to 
control the image resolution, center of your ROI, and the distance from the center to
the outer edge of the ROI in either direction on the x-axis.
