import cv2
import os
import glob
import time
import utils
import tkinter as tk
from PIL import ImageTk, Image

class HockeyVideo:
    def __init__(self, root, path, frameJump=1):
        self.root = root
        self.path = path
        self.frameJump = frameJump
        self.separateFrames()
        utils.tempClassifyFramesRand()
        self.frames = glob.glob('footage/*')
        self.frames.sort(key=utils.extractNum)

    def separateFrames(self):
        files = glob.glob('footage/*')
        for f in files:
            os.remove(f)

        vidObj = cv2.VideoCapture(self.path)
        vidFPS = vidObj.get(cv2.CAP_PROP_FPS)

        count = 0
        success = 1
        while success:
            try:
                success, image = vidObj.read()
                if count % self.frameJump == 0:
                    cv2.imwrite(f'footage/{count}-{round(vidFPS)}-predval.jpg', image)
                count += 1
            except:
                print('End of video?')

    def displayFrames(self):
        startTime = time.time()
        fps = utils.extractNum(self.frames[0], index=1)
        frameNum = 0
        for frameName in self.frames:
            self.displayImageInFrame(frameName, 250, 250, 1, 0)
            if (frameNum / fps) - (time.time() - startTime) > 0:
                time.sleep((frameNum / fps) - (time.time() - startTime))
            if utils.extractNum(frameName, 2) == 1:
                time.sleep(1)
            frameNum += self.frameJump

    def displayImageInFrame(self, frameName, width, height, row, column):
        gridFrame = tk.Frame(self.root, bg='green' if utils.extractNum(frameName, 2) == 0 else 'red')
        frameImg = Image.open(frameName)
        frameImg = frameImg.resize((width, height))
        frameImg = ImageTk.PhotoImage(frameImg)
        imgLabel = tk.Label(gridFrame, image=frameImg)
        imgLabel.image = frameImg
        imgLabel.grid(row=0, column=0, padx=5, pady=5)
        gridFrame.grid(row=row, column=column, columnspan=6)