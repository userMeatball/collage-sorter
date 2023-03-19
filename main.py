import numpy as np
import cv2 as cv
import os
import sys

def process(src):
    print("**********\nIf saved images are not of desired result, play around with threshold and contour area\n**********")
    # declare threshold and contour area for easy manipulation
    threshold = 150 # mask intensity
    con_area = 1000000  # minimum size of contour

    for img in src:
        # load img
        try:
            img = cv.imread(img)
        except:
            print("\nERROR: File '", img, "' could not be read!")

        # greyscale img, blur greyscale and mask,mask_inv
        img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        img_blur = cv.GaussianBlur(img_gray, (5, 5), 0)
        ret, mask = cv.threshold(img_blur, threshold, 255, cv.THRESH_BINARY)
        mask_inv = cv.bitwise_not(mask) # set background to black, foreground white

        #  get all contours from img
        contours, heirarchy = cv.findContours(mask_inv, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

        # loop through contours
        for i,contour in enumerate(contours):
            if cv.contourArea(contour) > con_area:
                # get dimensions of contour
                x,y,w,h = rect = cv.boundingRect(contour)

                # crop img to contour dimensions
                cropped = img[y: y+h, x: x+w]

                # # define filename and save cropped img
                # try:
                #     filename = 'img/' + str(i) + '.' + imgsrc
                #     print("Saving img: " + filename)
                #     cv.imwrite(filename, cropped)
                # except:
                #     print("The file: '" + filename + "' could not be saved!")

                # debug
                cv.imshow('img', cropped)
                cv.waitKey(0)
                cv.destroyAllWindows

# get src file or directory
if len(sys.argv) <= 1:
    print("No arguments provided!")
    quit()
src_in = str(sys.argv[1])
if not os.path.exists(src_in):
    print("That file or directory could not be found!")
    quit()

# declare src array, add all src files to array
src = []
if os.path.isdir(src_in):
    for f in os.listdir(src_in):
        src.append(src_in + '/' + f)
    print(src)
else:
    src.append(src_in)
    print(src)


process(src)


