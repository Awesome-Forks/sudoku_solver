import numpy as np
import cv2
import argparse
from packages import imutils, textutils, board_reader
import recognize
import sudoku

def main():
  recognizer = recognize.Recognize()
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

  if result == True or True:
    for sudoku_block in sudoku_blocks.iteritems():
      key, value = sudoku_block
      block = value['block']
      x,y,w,h = block

      text = str(value['value'])
      center_pos = textutils.centerPosInRect(text, block, font = font, font_scale = font_scale,
        thickness = thickness)
      cv2.putText(image, text, center_pos, font, font_scale, (0,255,0), thickness)
  if result == False:
    text = 'Cannot solve'
    block = (0,0,image.shape[1], image.shape[0])
    center_pos = textutils.centerPosInRect(text, block, font = font, font_scale = font_scale,
        thickness = thickness)
    cv2.putText(image, text, center_pos, font, font_scale, (0,0, 255), thickness)

  cv2.imshow("Sudoku", image)
  cv2.waitKey(0)

main()