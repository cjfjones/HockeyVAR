import os
import glob
import re
import pickle
# import tensorflow as tf # todo: uncomment when uncorrupted model
import numpy as np
import random
from PIL import ImageTk, Image

def roundToNearest(num, base):
    return round(num/base)*base

def openImage(path):
    image = Image.open(path)
    image = ImageTk.PhotoImage(image)
    return image

def openImageResize(path, size):
    image = Image.open(path)
    image.resize(size)
    image = ImageTk.PhotoImage(image)
    return image

def extractFrameNum(e):
    return int(re.findall('\d+', e)[0])  # Used for finding the frame number from a path

def extractConfidenceVal(e):
    return int(re.findall('\d+', e)[1])  # Used for finding the frame confidence from a path

def classifyFrames():
    model = loadModel()
    imageBatch = []
    #for imagePath in glob.glob('footage/*'):
        #image = tf.keras.preprocessing.image.load_img(imagePath, target_size=(160, 160))
        #imageArray = tf.keras.preprocessing.image.img_to_array(image)
        #imageBatch.append(imageArray)

    imageBatch = np.array(imageBatch)
    #imageBatch = tf.keras.applications.mobilenet_v2.preprocess_input(imageBatch)
    predictionBatch = model.predict(imageBatch)
    predictionLabels = (predictionBatch > 0.5).astype(int)

def loadModel():
    with open('model/model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

def tempClassifyFramesRand():
    for imagePath in glob.glob('footage/*'):
        if '75' in imagePath:
            os.rename(imagePath, imagePath.replace('predval', '1'))
        else:
            os.rename(imagePath, imagePath.replace('predval', '0'))