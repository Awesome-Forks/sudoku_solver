import numpy as np
import cv2
import argparse
from packages import imutils, textutils, board_reader

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument('-i', '--image', required=True, help="Image path")

  args = vars(ap.parse_args())

  image = cv2.imread(args["image"])
  # reside the image
  image = imutils.resize(image, width=300)

  # get sudoku block
  blocks = board_reader.getSudoKublocks(image)

  # exit application if cannot blocks
  if blocks == False:
    print 'Cannot read sudoku'
    return

  rows = 'ABCDEFGHI'
  cols = '123456789'
  index = 0
  temp = {}
  for c in cols:
    for r in rows:
      temp[r+c] = {}
      temp[r+c]['block'] = blocks[index]
      index += 1
  print blocks
  print '----------------------A1:', temp['B1']
  # Ex:  
  # 'A1': {block:[...], number: '1'}

  font = cv2.FONT_HERSHEY_SIMPLEX
  font_scale = 1
  thickness = 2
  font_scale = textutils.getFontScaleinRect(str(9), blocks[0], font = font,
    font_scale= font_scale, thickness= thickness)

  for index, block in enumerate(blocks):
    x,y,w,h = block

    sudo = image[y:y + h, x:x + w]
    name_crop = "crop" + str(index % 10)
    cv2.imshow(name_crop, sudo)
    text = str(index)
    center_pos = textutils.centerPosInRect(text, block, font = font, font_scale = font_scale,
      thickness = thickness)
    cv2.putText(image, text, center_pos, font, font_scale, (0,255,0), thickness)

  cv2.imshow("Sudoku", image)
  cv2.waitKey(0)

main()