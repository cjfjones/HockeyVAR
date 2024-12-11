import cv2
import os
import glob
import time
import utils
import tkinter as tk

class HockeyVideo:
    def __init__(self, root, path, frameJump=1):
        self.root = root
        self.path = path
        self.frame = tk.Frame(self.root, bg='green')
        self.frameJump = frameJump
        self.fps = 30 # Standard?
        self.separateFrames()
        utils.tempClassifyFramesRand()
        self.frames = glob.glob('footage/*')
        self.frames.sort(key=utils.extractFrameNum)
        self.lastFrame = utils.extractFrameNum(self.frames[-1])
        self.frameNum = 0
        self.nextFrameDisplayTime = time.time()
        self.speed = 1

    def separateFrames(self):
        files = glob.glob('footage/*')
        for f in files:
            os.remove(f)

        vidObj = cv2.VideoCapture(self.path)
        self.fps = vidObj.get(cv2.CAP_PROP_FPS)

        count = 0
        success = 1
        while success:
            try:
                success, image = vidObj.read()
                if count % self.frameJump == 0:
                    cv2.imwrite(f'footage/{count}-predval.jpg', image)
                count += 1
            except:
                print('End of video?')

    def displayFrames(self): # ONLY INVOKE AS THREAD
        self.nextFrameDisplayTime = time.time()
        while True: # Thread: so while video exists, this always runs
            frameName = self.frames[self.frameNum//self.frameJump]
            self.displayImageInFrame(frameName, 250, 250, 1, 0)
            while self.speed == 0:
                frameName = self.frames[self.frameNum // self.frameJump]
                self.displayImageInFrame(frameName, 250, 250, 1, 0)
            self.nextFrameDisplayTime += (self.frameJump/self.fps)/self.speed
            if self.nextFrameDisplayTime - time.time() > 0.01:
                time.sleep((self.nextFrameDisplayTime - time.time()) - 0.01)
            if utils.extractConfidenceVal(frameName) == 1:
                time.sleep(1)
            if self.frameNum + self.frameJump <= self.lastFrame:
                self.frameNum += self.frameJump
            else:
                self.dumpFrame()
                self.displayImageInFrame(frameName, 250, 250, 1, 0)
                self.speed = 0

    def displayImageInFrame(self, frameName, width, height, row, column):
        self.frame.configure(bg='green' if utils.extractConfidenceVal(frameName) == 0 else 'red')
        frameImg = utils.openImageResize(frameName, (width, height))
        imgLabel = tk.Label(self.frame, image=frameImg)
        imgLabel.image = frameImg
        imgLabel.grid(row=0, column=0, padx=5, pady=5)
        self.frame.grid(row=row, column=column, columnspan=6)

    def dumpFrame(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.root)