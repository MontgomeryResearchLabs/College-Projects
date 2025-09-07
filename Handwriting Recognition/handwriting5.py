# Imports
import numpy as np
from skimage import img_as_ubyte #convert float to uint8
from skimage.color import rgb2gray
import cv2
import imutils
import time
from time import sleep
from imutils.video import VideoStream
import tensorflow as tf
from tensorflow import keras
from sense_hat import SenseHat
from picamera import PiCamera


    
def read_image(file_path):
  img = cv2.imread(file_path, cv2.IMREAD_COLOR)
  return cv2.resize(img, (28, 28),interpolation=cv2.INTER_CUBIC)



camera = PiCamera()


# SenseHat Settings 
sense = SenseHat()
sense.set_rotation(180)
sense.low_light = True

# Load the model 
model= keras.models.load_model("/home/pi/Desktop/keras_convnet_adam")
print('Model loaded succesfully')







# Infinite loop
while True:
    
    sense.clear()
    
    camera.start_preview()
    sleep(2)
    
    camera.stop_preview()
    camera.capture('/home/pi/project/image.jpg')   
    
    img = read_image('/home/pi/project/image.jpg')
    
    
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_img = cv2.resize(gray_img, (28, 28))
    gray_img = cv2.bitwise_not(gray_img)

    X_img = gray_img.reshape(1, 28, 28, 1)/255
    mpred = model.predict(X_img)
    smpl_pred = np.argmax(mpred, axis=-1)
    temp = mpred[0, int(smpl_pred)]*100
    conf = str(int(temp))
    conf = conf + '%'

    num = str(smpl_pred)
    sense.show_message(num, text_colour=(0,0,255))
    sleep(2)
    sense.show_message(conf, text_colour=(0,0,255))
    sense.clear()
    
    print(num)
    print(conf, '%')

    input("next")
