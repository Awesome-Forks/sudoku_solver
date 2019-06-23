import numpy as np
import cv2
import argparse
from packages import imutils, textutils, board_reader
import sudoku

def main():
  ap = argparse.ArgumentParser()
  ap.add_argument('-i', '--image', required=True, help="Image path")

  args = vars(ap.parse_args())

  image = cv2.imread(args["image"])
  # reside the image
  image = imutils.resize(image, width=300)

  # get sudoku block
  blocks = board_reader.getSudoKublocks(image)

  colorLower = np.array([0, 0, 0], dtype="uint8")
  colorUpper = np.array([250, 250, 250], dtype="uint8")
  gray = cv2.inRange(image, colorLower, colorUpper)
  cv2.imshow('my gray', gray)

  # exit application if cannot blocks
  if blocks == False:
    print('Cannot read sudoku')
    return

  sudokuer = sudoku.Sudoku(blocks, image)
  sudoku_blocks = sudokuer.blocks
  test_str = sudokuer.toString()
  print(test_str)

  result = sudokuer.result()

  font = cv2.FONT_HERSHEY_SIMPLEX
  font_scale = 1
  thickness = 2
  font_scale = textutils.getFontScaleinRect(str(9), blocks[0], font = font,
    font_scale= font_scale, thickness= thickness)

  count = 1
  if result == True or True:
    for sudoku_block in sudoku_blocks.items():
      key, value = sudoku_block
      block = value['block']
      x,y,w,h = block
      crop_img = image[y+5:y+h-5, x+5:x+w-5]
      cv2.imwrite("images/saved/crop-2-" + str(count) + ".png", crop_img)
      count += 1

      text = str(value['value'])
      if value['is_show']:
      # if True:
        center_pos = textutils.centerPosInRect(text, block, font = font, font_scale = font_scale,
          thickness = thickness)
        cv2.putText(image, text, center_pos, font, font_scale, (0,255,0), thickness)
  if result == False:
    text = 'Cannot solve'
    block = (0,0,image.shape[1], image.shape[0])
    center_pos = textutils.centerPosInRect(text, block, font = font, font_scale = font_scale,
        thickness = thickness)
    cv2.putText(image, text, center_pos, font, font_scale, (0,0,255), thickness)

  cv2.imshow("Sudoku", image)
  cv2.waitKey(0)

main()
