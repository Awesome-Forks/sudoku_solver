import numpy as np
import cv2

def getFontScaleinRect(text, rect, font = cv2.FONT_HERSHEY_SIMPLEX, font_scale = 1,
  thickness = 2, percentage = 0.6):
  x,y,w,h = rect
  size = cv2.getTextSize(text, font, font_scale, thickness)[0]
  temp1 = percentage * w / size[0]
  temp2 = percentage * h / size[1]
  mintemp = min(temp2, temp1)
  return font_scale * mintemp

def centerPosInRect(text, rect, font = cv2.FONT_HERSHEY_SIMPLEX, font_scale = 1,
  thickness = 2):
  size = cv2.getTextSize(text, font, font_scale, thickness)[0]
  x,y,w,h = rect
  return (x + int((w - size[0])/2), y + int((h + size[1])/2))
