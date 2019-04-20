from sklearn.svm import LinearSVC
from packages.hog import HOG
from packages import dataset
import argparse
import pickle
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True, help="path to the dataset file")
ap.add_argument("-m", "--model", required=True, help="path tro where the model will be stored")
args = vars(ap.parse_args())

(digits, target) = dataset.load_data(args["dataset"])
# print digits
print (digits.shape)
print (len(digits))
print ("------------------------------------------------------------------------")
print (target)
data = []

hog = HOG(orientations = 18, pixelsPerCell =(10, 10), cellsPerBlock = (1,1), transform_sqrt = True)

for image in digits:
    image = dataset.deskew(image, 20)
    image = dataset.center_extent(image, (20, 20))

    hist = hog.describe(image)
    data.append(hist)
print ("------------------------------------------------------------------------")
print (len(data))
model = LinearSVC(random_state= 42)
model.fit(data, target)
print ("------------------------------------------------------------------------")
print (model)
f = open(args["model"], "wb")
f.write(pickle.dumps(model))
f.close()
