import numpy as np
import cv2 as cv

print("**********\nIf saved images are not of desired result, play around with threshold and contour area\n**********")

# declare threshold and contour area for easy manipulation
threshold = 150 # mask intensity
con_area = 1000000  # minimum size of contour

# declare img src
imgsrc = "./img/photo3.jpg"

# load img
img = cv.imread(imgsrc)
assert img is not None, "file could not be read!"

# greyscale img, blur greyscale and mask,mask_inv
img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
img_blur = cv.GaussianBlur(img_gray, (5, 5), 0)
ret, mask = cv.threshold(img_blur, threshold, 255, cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask) # set background to black, foreground white

#  get all contours from img
contours, heirarchy = cv.findContours(mask_inv, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

# debug
cv.imshow('src', mask_inv)
cv.waitKey(0)
cv.destroyAllWindows()

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
        cv.imshow('approx', cropped)
        cv.waitKey(0)
        cv.destroyAllWindows()
