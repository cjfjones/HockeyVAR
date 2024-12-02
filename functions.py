import os
import glob
import cv2
import tkinter as tk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
import time
import threading

def frameSeparation(path):
    files = glob.glob('footage/*')
    for f in files:
        os.remove(f)

    vidObj = cv2.VideoCapture(path)

    count = 0
    success = 1
    while success:
        try:
            success, image = vidObj.read()
            if count%3 == 0:
                cv2.imwrite(f'footage/{count}.jpg', image)
            count += 1
        except:
            print('End of video?')

def displayFrames(root):
    for frameName in glob.glob('footage/*'):
        frameObj = ImageTk.PhotoImage(Image.open(frameName))
        displayFrame = tk.Label(root, image=frameObj)
        displayFrame.grid(row=1, column=0)
        time.sleep(1)

def submitVideo(root):
    filename = fd.askopenfilename()
    frameSeparation(filename)
    displayFrames(root)
    t = threading.Thread(target=displayFrames, args=[root])
    t.run()
