from packages.hog import HOG
from packages import dataset
import mahotas
import cv2
from packages import imutils
import pickle

class Recognize:
  # def __init__(self):
    # print("Open model")
    # self.model = open("train_data/svm.cpickle", "rb").read()
    # self.model = pickle.loads(self.model)
    # print(self.model)

    # self.hog = HOG(orientations = 18, pixelsPerCell = (10,10), cellsPerBlock=(1,1), transform_sqrt= True)

  def recognizing(self, image):
    cv2.imshow("sample", image)
    # if image.shape[1] < 41:
    #   image = imutils.resize(image, height=41)

    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (5,5), 0)
    # edged = cv2.Canny(blurred, 30, 150)
    # (_, cnts,_) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in cnts], key = lambda x: x[1])

    # for (c, _) in cnts:
    #   (x,y,w,h) = cv2.boundingRect(c)

    #   if w >= 7 and h >= 20:
    #     roi = gray[y:y+h, x: x+w]

    #     thresh = roi.copy()
    #     T = mahotas.thresholding.otsu(roi)
    #     thresh[thresh > T] = 255
    #     thresh = cv2.bitwise_not(thresh)

    #     thresh =  dataset.deskew(thresh, 20)
    #     thresh = dataset.center_extent(thresh, (20,20))

    #     hist = self.hog.describe(thresh)
    #     digit = self.model.predict([hist])
    #     return digit[0]
    return 0
