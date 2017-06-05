import numpy as np
import cv2
import argparse
from packages import imutils

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image path")

args = vars(ap.parse_args())

image = cv2.imread(args["image"])
# reside the image
image = imutils.resize(image, width=300)
# change image color to gray
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# blurred the gray image
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# # apply throshold to image
# thresh = cv2.adaptiveThreshold(blurred, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 3)
thresh = cv2.adaptiveThreshold(blurred,255,1,1,11,2)

# edged detection
edged = cv2.Canny(thresh, 30, 200)
# edged = cv2.Canny(thresh,100,200)

#count tour
(_,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None

# loop over our contours
for c in cnts:
  # approximate the contour
  peri = cv2.arcLength(c, True)
  approx = cv2.approxPolyDP(c, 0.02 * peri, True)

  # if our approximated contour has four points, then
  # we can assume that we have found our screen
  if len(approx) == 4:
    screenCnt = approx
    # check if in side this block has 8 horizontal line, 8 vertical line
    # if yes, draw it
    # get blocks 9*9 = (81)
    # get value in the each blocks
    # then breack
    break
cv2.drawContours(image, [screenCnt], -1, (0,255,0),3)

cv2.imshow("Mean Thresh", thresh)
cv2.imshow("Blurred", blurred)
cv2.imshow("edged detection", edged)
cv2.imshow("Sudoku", image)
cv2.waitKey(0)
