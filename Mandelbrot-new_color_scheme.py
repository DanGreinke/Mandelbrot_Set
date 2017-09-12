#! python3
# This program checks individual points and reports whether they are in the mandelbrot set.
#
# An input point must survive at least 1000 iterations without moving past a distance of 2 from
# the origin to be considered a part of the set.

# My Display is 1366 px by 768 px

import math, pprint, PIL, csv, os, time
from PIL import ImageColor, Image

# Output image resolution: x-axis
x_res = 1920
# Number of samples on x-axis. Must be higher than res to avoid dead pixels
x_sample = int(math.floor(x_res*1.2))
# Output image resolution: y-axis
y_res = 1080
# Number of samples on y-axis. Must be higher than res.
y_sample = int(math.floor(y_res*1.2))
# Number of times sampled point is iterated before cutoff. 
max_iteration = 1000.0
Re_range = []
Im_range = []
center = [0.0, 0.0] # center of ROI. [x, y]
half_width = 2.0 # defines distance from center to edge of frame in x-direction
x_min_value = center[0] - half_width
x_max_value = center[0] + half_width
y_min_value = center[1] - (half_width*y_sample)/x_sample
y_max_value = center[1] + (half_width*y_sample)/x_sample
x_current_value = x_min_value
y_current_value = y_min_value

#TODO attempt to open csv file that fits desired parameters
have_file = os.path.exists('C:\\Users\\dgrei\\OneDrive\\Documents\\Python_Scripts\\Mandelbrot\\Mandelbrot_Set\\' + 'Mandelbrot_Set_' + str(x_res) + '_by_' + str(y_res) + '_' + str(x_min_value) + "X_to_" + str(x_max_value) + "X_by_" + str(y_min_value) + "Y_to_" + str(y_max_value)+ 'Y.csv')
#if no suitable file found, calculate set and save to csv file.
while have_file == False:
    resultFile = open('Mandelbrot_Set_' + str(x_res) + '_by_' + str(y_res) + '_' + str(x_min_value) + "X_to_" + str(x_max_value) + "X_by_" + str(y_min_value) + "Y_to_" + str(y_max_value)+ 'Y.csv', 'w', newline='')
    print('Calculating...')
    outputWriter = csv.writer(resultFile)
    # X range
    for i in range(x_sample + 1):
        x_step = (float(i)*(x_max_value - x_min_value))/x_sample
        Re_range.append(x_current_value + x_step)
    # Y range
    for j in range(y_sample + 1):
        y_step = (float(j)*(y_max_value - y_min_value))/y_sample
        Im_range.append(y_current_value + y_step)
    # iterate through rows on grid (y-axis)
    for Im in Im_range:
        # iterate through columns in each row (x-axis)
        for Re in Re_range:
            x0 = Re
            y0 = Im
            x = 0.0
            y = 0.0
            iteration = 0
            # iterate each pixel until the output reaches a distance of 2 from origin, or reaches max_iteration cutoff.
            while x*x + y*y < 4 and iteration <= max_iteration:
                x_temp = x*x - y*y + x0
                y = 2*x*y + y0
                x = x_temp
                iteration += 1
                if iteration == max_iteration:
                    outputWriter.writerow([Re, Im, iteration])
                elif x*x + y*y >= 2*2:
                    outputWriter.writerow([Re, Im, iteration])

    resultFile.close()
    have_file = True 
# if csv file is found, or after file is created, may begin reading file and generating image. 
if have_file == True:
    #Initialize new image.
    print('Initializing pic.')
    im = Image.new('RGBA', (x_res + 1, y_res + 1))
    #Open output file, read file, create list from file data
    print('Opening File.')
    resultFile = open('Mandelbrot_Set_' + str(x_res) + '_by_' + str(y_res) + '_' + str(x_min_value) + "X_to_" + str(x_max_value) + "X_by_" + str(y_min_value) + "Y_to_" + str(y_max_value)+ 'Y.csv')
    Mandelbrot_reader = csv.reader(resultFile)
    Mandelbrot_data = list(Mandelbrot_reader)
    print('Generating Image...')
    # iterate through list of file data, convert to image coordinate system, assign pixel colors in image
    for row in Mandelbrot_data:
        x_val = float(row[0]) - center[0]
        x_px = int(math.floor(x_val*(float(x_res)/(x_max_value - x_min_value)) + (float(x_res)/(2.0))))
        #print(x_px)
        y_val = float(row[1]) - center[1]
        y_px = int(math.floor(y_val*(-float(y_res)/(y_max_value - y_min_value)) + (float(y_res)/(2.0))))
        #print(y_px)
        if float(row[2]) == max_iteration and x_px > 0.0 and y_px > 0:
            im.putpixel((x_px, y_px), (0, 0, 0))
        # Base pixel color on black body radiation color temp values. pixels close to mandelbrot set are blue hot, further away are red hot.
        elif float(row[2]) < max_iteration and x_px > 0.0 and y_px > 0:
            color_temp = (39.039*float(row[2]) + 960.961)/100 #assign color temp based on no. of iterations
            # Assign RGB values according to color temp. Credit to Tanner Helland for this algorithm
            # http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
            if color_temp <= 66:
                red = 255
            else:
                red = color_temp - 60.0
                red = int(round((329.698727446*(red**(-0.1332047592))), 0))
                if red < 0:
                    red = 0
                elif red > 255:
                    red = 255
                    
            if color_temp <= 66:
                green = color_temp
                green = int(round((99.4708025861*math.log(green) - 161.1195681661), 0))
                if green < 0:
                    green = 0
                elif green > 255:
                    green = 255
            else:
                green = color_temp - 60.0
                green = int(round((288.1221695283*(green**(-0.0755148492))), 0))
                if green < 0:
                    green = 0
                elif green > 255:
                    green = 255
                    
            if color_temp >= 66:
                blue = 255
            else:
                if color_temp <= 19.0:
                    blue = 0
                else:
                    blue = color_temp - 10
                    blue = int(round((138.5177312231*math.log(blue) - 305.0447927307), 0))
                    if blue < 0:
                        blue = 0
                    elif blue > 255:
                        blue = 255
            im.putpixel((x_px, y_px), (red, green, blue))
            #TODO implement new color scheme
    timestamp = time.strftime("%Y%m%d%H%M%S")
    im.save('Mandelbrot_Set_' + str(x_res) + 'x' + str(y_res) + '_' + str(timestamp) + '.png')
    resultFile.close()
print('Done.')            

        









            
 
