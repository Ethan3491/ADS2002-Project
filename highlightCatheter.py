from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import ast
from scipy.interpolate import CubicSpline

#Function to create a circular area of white pixels centrered on an x,y cordinate. Warning, this is an INPLACE function
def small_dot(image_array,x,y,radius):

    h, w = image_array.shape[:2] 

    #Bounding box clipping to stay within image bounds
    y1 = max(0, y - radius)
    y2 = min(h, y + radius + 1)
    x1 = max(0, x - radius)
    x2 = min(w, x + radius + 1)

    yy, xx = np.ogrid[y1 - y:y2 - y, x1 - x:x2 - x]
    mask = xx**2 + yy**2 <= radius**2

    image_array[y1:y2, x1:x2][mask] = 255

#Function to generate an array of interpolated coordinates from existing ones. Expects list[list[x,y]]. Code assisted by ChatGPT
#Input (coordinate_array -> list[list[x,y]])
#Output (coordinate_array -> list[list[x,y]])
def parametric_spline(coordinate_array, n=50):
    points = np.array(coordinate_array)
    t = np.arange(len(points)) #Assigning a parameter, t, to each point 
    
    # Build cubic splines for x(t) and y(t)
    cs_x = CubicSpline(t, points[:, 0])
    cs_y = CubicSpline(t, points[:, 1])
    
    # Evaluate on fine grid
    tt = np.linspace(0, len(points)-1, n)
    xx = cs_x(tt)
    yy = cs_y(tt)

    result= []
    for i in range(n):
        result.append([xx[i], yy[i]])
    return result

#Input (image -> Image, coordinate_array -> list[list[x,y]], n -> int) 
#Output (image -> Image)
#Draws the caterther onto an image given a caterther path and the image to be drawn on. N controls how many dots are drawn, increase if lines appear 
def highlightCatheter(image, coordinate_array, n = 500):
    img = image
    img_array = np.array(img, dtype=np.float32)
    coords= coordinate_array 
    inter_coords = parametric_spline(coords,n)
    
    img_array = np.array(img, dtype=np.float32)
    for cord in inter_coords:
        small_dot(img_array, int(cord[0]), int(cord[1]), 10)
    image_result = Image.fromarray(img_array.astype("uint8"))
    return image_result

#Recommended input

#filepath = rf"?"
#imageIloc = 0
#image = Image.open(rf"{filepath}\{annotatedDataframe.iloc[imageIloc][0]}.jpg")
#coordinate_array = ast.literal_eval(annotatedDataframe.iloc[imageIloc][2])
#highlightCatheter(image, coordinate_array)
