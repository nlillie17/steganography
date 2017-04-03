# ## Problem 3:  green-screening!
# 
# This question asks you to write one function that takes in two images:
#  + orig_image  (the green-screened image)
#  + new_bg_image (the new background image)
#  
# It also takes in a 2-tuple (corner = (0,0)) to indicate where to place the upper-left
#   corner of orig_image relative to new_bg_image
#
# The challenge is to overlay the images -- but only the non-green pixels of
#   orig_image...
#

#
# Again, you'll want to borrow from hw7pr1 for
#  + opening the files
#  + reading the pixels
#  + create some helper functions
#    + defining whether a pixel is green is the key helper function to write!
#  + then, creating an output image (start with a copy of new_bg_image!)
#
# Happy green-screening, everyone! Include at least TWO examples of a background!
#





# Here is a signature for the green-screening...
# remember - you will want helper functions!

import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image 


def resize_image(orig_image, new_bg_image):
    """ this should resize the images to be the same size"""
    new_image = orig_image.copy()
    new_image2 = new_bg_image.copy()
    num_rows, num_cols, num_chans = new_image.shape
    new_image2 = cv2.resize(new_image2, (num_cols,num_rows))
    return new_image2


def green_screen( orig_image, new_bg_image, corner=(0,0) ):
    """ replaces all of the green in the original image with a background """
    new_image = orig_image.copy()
    new_image2 = new_bg_image.copy()
    new_image = resize_image(new_image2,new_image)
    num_rows, num_cols, num_chans = new_image2.shape
    for row in range(num_rows):
        for col in range(num_cols):
            r1,g1,b1 = new_image[row,col] 
            r2,g2,b2 = new_image2[row,col]
            if isGreen(r1,g1,b1) == False:
                new_image2[row,col] = [r1,g1,b1]
            else:
                new_image[row,col] = [r2,g2,b2]

    plt.imshow(new_image)
    plt.show()
    cv2.imwrite("green_screen1poll.jpg",new_image)
    return new_image		


# def two_image_filter( image1, image2 ): #Kept just for easy checking of converting pixels
#     '''transform r,g,b values by multiplying by random scalar if under 255
#     '''
#     new_image1 = image1.copy()
#     new_image2 = image2.copy()
    
#     len1 = len(new_image1)
#     len2 = len(new_image2)

#     image_used = image1
#     if len2 < len1:
#         image_used = image2
    
#     new_image = image_used
    
#     num_rows, num_cols, num_chans = image_used.shape
#     for row in range(num_rows):
#         for col in range(num_cols):
#             r1, g1, b1 = new_image1[row,col]
#             r2, g2, b2 = new_image2[row,col]
#             new_image[row,col] = [trans_r2(r1,r2), trans_g2(g1,g2), trans_b2(b1,b2)]  # [0,0,b]
#     plt.imshow(new_image)
#     plt.show() 
#     return new_image 

def isGreen(r,g,b):
    """ determines whether a pixel is green """
    #65,255,65 - 0,199,0 is the range of lime green
    if g-r>40 and g-b>50:
        return True 
    elif g<100 and r<70 and b<70:
        if g-b<20 or g-r<20:
            return False
        return True
    return False

""" so to implement our green_screen function, we first re-sized the images to be the same size.
Next, we checked through each pixel in each picture. If the pixel was determined to be green based on our
isGreen(r,g,b) function, then we took the pixel from the background pic. If the pixel was determined
to be not green, then we took the pixel from the original image. We have attached two images: the first
is of me (Austin) on Dodger Stadium (this was saved directly from plt.imshow()). The second was taken 
from the file that was written by our code. It created a pollution background for some odd reason, and
we thought it looked cool so we kept it."""
