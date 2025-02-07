import cv2
import os
import glob
import time
import utils
import tkinter as tk

class HockeyVideo:
    def __init__(self, root, path, frameJump=1):
        self.root = root  # Tkinter window
        self.root.bind('<Escape>', self.endManualVAR)
        self.path = path  # Video path
        self.frame = tk.Frame(self.root, bg='green')  # Initialise the tkinter frame which holds the video
        self.mouseX = None
        self.mouseY = None
        self.frameJump = frameJump  # How many frames are displayed e.g: frameJump = 2, only frame 0, 2, 4, 6 will play
        self.fps = 30  # Video FPS, redefined when a video is submitted. 30 is standard?
        self.separateFrames()  # Turns the video into a sequence of frames
        utils.tempClassifyFramesRand()  # Randomly assigns values to the frames (no model working yet)
        self.frames = glob.glob('footage/*')  # Creates a list of frame paths
        self.frames.sort(key=utils.extractFrameNum)  # Sorts into order
        self.lastFrame = utils.extractFrameNum(self.frames[-1])  # path of the last frame
        self.frameNum = 0  # Current frame being displayed
        self.nextFrameDisplayTime = time.time()  # Time when the next frame should display
        self.speed = 1  # Playback speed
        self.isPaused = False
        self.videoEnded = False  # Ends video threading when True
        self.manualVARMode = False
        self.VARStage = 'start'
        self.ballStartPos = None
        self.ballCollisionPos = None
        self.ballEndPos = None

    def separateFrames(self):
        files = glob.glob('footage/*')
        for f in files:
            os.remove(f)  # Clears frame directory

        vidObj = cv2.VideoCapture(self.path)
        self.fps = vidObj.get(cv2.CAP_PROP_FPS)

        count = 0
        success = 1
        while success:
            try:
                success, image = vidObj.read()
                if count % self.frameJump == 0:
                    cv2.imwrite(f'footage/{count}-predval.jpg', image)  # Creates frame file, form orderSequence-modelConfidence
                count += 1
            except:
                print('End of video?')

    def displayFrames(self): # ONLY INVOKE AS THREAD
        comparisonFrameDifference = 10
        self.nextFrameDisplayTime = time.time()
        while True: # Thread: so while video exists, this always runs
            if self.videoEnded:
                return  # When returned, the thread ends
            if not self.manualVARMode:
                frameName = self.frames[self.frameNum//self.frameJump]
                self.displayImageInFrame(frameName, 250, 250, 1, 0)
                while self.speed == 0 or self.isPaused:
                    if self.videoEnded:
                        return  # When returned, the thread ends
                    frameName = self.frames[self.frameNum // self.frameJump]
                    self.displayImageInFrame(frameName, 250, 250, 1, 0)

                self.nextFrameDisplayTime += (self.frameJump/self.fps)/self.speed
                if self.nextFrameDisplayTime - time.time() > 0.01:  # Wait until time to show next frame
                    time.sleep((self.nextFrameDisplayTime - time.time()) - 0.01)
                if utils.extractConfidenceVal(frameName) == 1:  # Stutter frame when foot identified
                    time.sleep(1)
                    self.VARStage = 'start'
                    self.manualVARMode = True
                    self.frameNum -= round(comparisonFrameDifference/self.frameJump)*self.frameJump
                    frameName = self.frames[self.frameNum // self.frameJump]
                elif self.frameNum + self.frameJump <= self.lastFrame:
                    self.frameNum += self.frameJump
                else:  # End of video
                    self.dumpFrame()
                    self.displayImageInFrame(frameName, 250, 250, 1, 0)
                    self.isPaused = True
            if self.manualVARMode:
                self.displayImageInFrame(frameName, 250, 250, 1, 0)
                if self.VARStage == 'start':
                    self.VARInstructionLabel = tk.Label(self.root, text='Please select the centre of the ball.')
                    self.VARInstructionLabel.grid(row=0, column=1)
                    if self.mouseX != None and self.mouseY != None:
                        self.ballStartPos = (self.mouseX, self.mouseY)
                        self.mouseX = None
                        self.mouseY = None
                        self.frameNum += round(comparisonFrameDifference/self.frameJump)*self.frameJump
                        frameName = self.frames[self.frameNum // self.frameJump]
                        self.VARStage = 'collision'
                if self.VARStage == 'collision':
                    if self.mouseX != None and self.mouseY != None:
                        self.ballStartPos = (self.mouseX, self.mouseY)
                        self.mouseX = None
                        self.mouseY = None
                        self.frameNum += round(comparisonFrameDifference/self.frameJump)*self.frameJump
                        frameName = self.frames[self.frameNum // self.frameJump]
                        self.VARStage = 'end'
                if self.VARStage == 'end':
                    if self.mouseX != None and self.mouseY != None:
                        self.ballStartPos = (self.mouseX, self.mouseY)
                        self.mouseX = None
                        self.mouseY = None
                        self.VARStage = 'display'
                if self.VARStage == 'display':
                    self.manualVARMode = False
                    self.frameNum += round(comparisonFrameDifference/self.frameJump)*self.frameJump


    def displayImageInFrame(self, frameName, width, height, row, column):
        self.frame.configure(bg='green' if utils.extractConfidenceVal(frameName) == 0 else 'red')
        frameImg = utils.openImageResize(frameName, (width, height))
        imgLabel = tk.Label(self.frame, image=frameImg)
        imgLabel.image = frameImg
        imgLabel.grid(row=0, column=0, padx=5, pady=5)
        imgLabel.bind('<Button-1>', self.getMousePos)
        self.frame.grid(row=row, column=column, columnspan=6)

    def dumpFrame(self):
        self.frame.destroy()  # Removes pointless frames
        self.frame = tk.Frame(self.root)

    def getMousePos(self, event):
        if self.manualVARMode:
            self.mouseX = event.x
            self.mouseY = event.y
            print(event.x, event.y)

    def endManualVAR(self, event):
        self.manualVARMode = False