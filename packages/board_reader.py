import numpy as np
import cv2

def getSudoKublocks(image):
  # init the color range(between the color set to white else to black)
  colorLower = np.array([0, 0, 0], dtype="uint8")
  colorUpper = np.array([250, 250, 250], dtype="uint8")
  gray = cv2.inRange(image, colorLower, colorUpper)

  #count tour
  (_,cnts, _) = cv2.findContours(gray.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  sort_cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
  sudoBlock = None

  index = 0
  blocks = []

  while True:
    blocks = []

    if index == 0:
      boxH, boxW = image.shape[:2]
    else:
      _,_,boxW, boxH = cv2.boundingRect(sort_cnts[index])

    # calculate max/min of each sudoku blocks
    maxBoxH = (boxH / 9) + (boxH / 9 * 0.2)
    minBoxH = (boxH / 9) - (boxH / 9 * 0.2)
    maxBoxW = (boxW / 9) + (boxW / 9 * 0.2)
    minBoxW = (boxW / 9) - (boxW / 9 * 0.2)

    count = 0
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
        blocks.append([x, y, w, h])

    index += 1

    # exit loop
    if index >= 5 or len(blocks) == 81:
      break

  #order the block by its position
  blocks = sorted(blocks, reverse = False)

  if len(blocks) != 81:
    return False
  else:
    return blocks