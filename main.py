import numpy as np
import cv2 as cv
import os
import argparse
import random as rng

def thresh_callback(val):
    threshold = val

    canny_output = cv.Canny(src_blur, threshold, threshold * 2)

    contours, _ = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contours_poly = [None]*len(contours)
    # boundRect = [None]*len(contours)
    poly_accuracy = 50
    for i, c in enumerate(contours):
        contours_poly[i] = cv.approxPolyDP(c, poly_accuracy, True)
        # boundRect[i] = cv.boundingRect(contours_poly[i])

    
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    
    for i in range(len(contours)):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv.drawContours(drawing, contours_poly, i, color)
        # cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
        # (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
    
    
    cv.imshow('Contours', drawing)


def process(src_arr):
    # loop through source images
    for src in src_arr:
        src = cv.imread(cv.samples.findFile(args.i))
        if src is None:
            print("Couldn't open file. Check path.")
            break
            
        # gray source img
        src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        # blur grayed img
        global src_blur     # used in thresh callback function
        src_blur = cv.blur(src_gray, (3,3))

        # create window and show source
        source_window = "Source"
        cv.namedWindow(source_window)
        cv.imshow(source_window, src)

        max_thresh = 255
        thresh = 60 # initial threshold
        cv.createTrackbar('Canny thresh:', source_window, thresh, max_thresh, thresh_callback)
        thresh_callback(thresh)

        cv.waitKey()


# get src file or directory
parser = argparse.ArgumentParser(description='Lorem.')
parser.add_argument('-i', help='Path to input image.', default='ogimg.jpg')
args = parser.parse_args()

# append file or files if input is directory
src = []
if os.path.isdir(args.i):
    for f in os.listdir(args.i):
        src.append(args.i + '/' + f)
else:
    src.append(args.i)

# process an image or list of imgs
process(src)


