import numpy as np
from skimage import exposure
import cv2
import argparse
from packages import imutils

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image path")

args = vars(ap.parse_args())

image = cv2.imread(args["image"])
# reside the image
image = imutils.resize(image, width=300)

colorLower = np.array([0, 0, 0], dtype="uint8")
colorUpper = np.array([250, 250, 250], dtype="uint8")
gray = cv2.inRange(image, colorLower, colorUpper)
cv2.imshow("Mean in Range", gray)

# change image color to gray
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# blurred the gray image
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# # apply throshold to image
thresh = cv2.adaptiveThreshold(blurred, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 3)
# thresh = cv2.adaptiveThreshold(blurred,255,0,0,15,3)

#apply filter to image
# filter = cv2.bilateralFilter(blurred, 10, 17, 17)
# edged = cv2.Canny(filter, 30, 150, apertureSize = 3)

# edged detection
edged = cv2.Canny(thresh, 30, 150, apertureSize = 3)
#count tour
(_,cnts, _) = cv2.findContours(gray.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
sort_cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
screenCnt = None

boxH, boxW = image.shape[:2]
maxBoxH = (boxH / 9) + (boxH / 9 * 0.1)
minBoxH = (boxH / 9) - (boxH / 9 * 0.1)
maxBoxW = (boxW / 9) + (boxW / 9 * 0.1)
minBoxW = (boxW / 9) - (boxW / 9 * 0.1)
# maxBoxH = 9 * h => h = maxBoxH / 9
# maxBoxW = 9 * w => w = maxBoxW / 9
count = 0
blocks = []
# screenCnt = cv2.approxPolyDP(sort_cnts[0], 4, True)
print maxBoxW, maxBoxH
# loop over our contours
for c in cnts:
  # approximate the contour
  peri = cv2.arcLength(c, True)
  approx = cv2.approxPolyDP(c, 0.02 * peri, True)
  (x, y, w, h) = cv2.boundingRect(c)

  # if our approximated contour has four points,
  # and its width and height is in range
  # then we can assume that we have found sudoku block
  if (len(approx) == 4) and (w >= minBoxW and w <= maxBoxW) and (h >= minBoxH and h <= maxBoxH):
    blocks.append([x,y])
    count += 1
    # sudo = image[y:y + h, x:x + w]
    # name_crop = "crop" + str(count % 5)
    # cv2.imshow(name_crop, sudo)
    cv2.putText(image, str(count), (x + 5, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0), 2)
    # cv2.drawContours(image,[approx], 0, (0, 0, 255), 2)
print len(blocks)
print blocks
cv2.drawContours(image, [screenCnt], -1, (0,255,0),3)

# cv2.imshow("Mean Thresh", thresh)
# cv2.imshow("Gray", gray)
# cv2.imshow("edged detection", edged)
cv2.imshow("Sudoku", image)
cv2.waitKey(0)
