import numpy as np
import cv2 as cv
import os
import sys


# process images give in src[]
def process(src):
    print("**********\nIf saved images are not of desired result, play around with threshold and contour area\n**********")
    # declare threshold and contour area for easy manipulation
    threshold = 150 # mask intensity
    con_area = 1000000  # minimum size of contour

    for img_path in src:
        # load img
        try:
            img = cv.imread(img_path)
        except:
            print("\nERROR: File '", img, "' could not be read!")

        # greyscale img, blur greyscale and mask,mask_inv
        img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        img_blur = cv.GaussianBlur(img_gray, (5, 5), 0)
        ret, mask = cv.threshold(img_blur, threshold, 255, cv.THRESH_BINARY)
        mask_inv = cv.bitwise_not(mask) # set background to black, foreground white

        #  get all contours from img
        contours, heirarchy = cv.findContours(mask_inv, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

        # list of all cropped images
        processed_img = {}
        # loop through contours
        for i,contour in enumerate(contours):
            if cv.contourArea(contour) > con_area:
                # get dimensions of contour
                x,y,w,h = rect = cv.boundingRect(contour)

                # crop img to contour dimensions
                img_cropped = img[y: y+h, x: x+w]

                # declare filename for the cropped img
                filename = str(i) + '.jpg'

                processed_img[filename] = img_cropped

        return processed_img


# save files in directory arg, take in cropped: ndarray[] returned by process
# file structure: root_dir, processed_dir, src_img & processed_imgs
# root_dir being dir specified by user
# processed_dir being dir_name of src_img - ext
# processed_imags being file_name of {path}/i.src_img
def save(processed_img, save_dir):
    if not os.path.exists(save_dir):
        print("ERROR: The directory '" + save_dir + "' could not be found!")
        quit()
    
    for key in processed_img:
        filename = save_dir + key
        img = processed_img[key]
        if not os.path.exists(filename):
            print("Writing file: " + filename)
            cv.imwrite(filename, img)
        else:
            print("ERROR: The file '" + filename + "' already exists!")


if __name__ == "__main__":
    # get src file or directory
    if len(sys.argv) < 3:
        print("Two arguments needed!")
        print("eg. python main.py ./input/ ./output/")
        # help
        quit()
    src_in = str(sys.argv[1])   # set input source given in arg
    save_dir = str(sys.argv[2]) # set output directory given in arg
    if not os.path.exists(src_in):
        print("The file or directory '" + src_in + "' could not be found!")
        quit()
    if not os.path.exists(save_dir):    # create output dir if doesn't exist
        print("Creating output dir: " + save_dir)
        os.mkdir(save_dir)

    # declare src array
    src = []
    # if src_in is path to directory, loop through files and append to src
    if os.path.isdir(src_in):   
        for f in os.listdir(src_in):
            src.append(src_in + '/' + f)
    else:
        src.append(src_in)

    # save cropped images from src_img
    save(process(src), save_dir)


