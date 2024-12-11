import tkinter as tk
import utils
import videoClass
from tkinter import filedialog as fd
import threading
import time

class hockeyTkinterWindow:
    def __init__(self):
        self.video = None
        self.createWindow()

    def createWindow(self):
        self.root = tk.Tk()
        self.root.minsize(150, 100)

        self.submitVideoButton = tk.Button(self.root, text='Submit File', command=self.submitVideo,
                                      activebackground='blue', activeforeground='white')
        self.submitVideoButton.grid(row=0, column=0, pady=2)

        self.root.mainloop()

    def createButtonsWidget(self):
        self.buttonFrame = tk.Frame(self.root, bg='grey')
        self.buttonFrame.grid(row=3, column=0, columnspan=6, sticky='nsew')

        self.reverseImage = utils.openImageResize('buttonImages/back.png', (20, 20))
        self.reverseButton = tk.Button(self.buttonFrame, image=self.reverseImage, command=self.reverseFrame, activebackground='blue',
                                  activeforeground='white')
        self.reverseButton.grid(row=0, column=0, padx=5, pady=2)

        self.playImage = utils.openImageResize('buttonImages/play.png', (20, 20))
        self.playButton = tk.Button(self.buttonFrame, image=self.playImage, command=self.playVideo, activebackground='blue',
                               activeforeground='white')
        self.playButton.grid(row=0, column=1, padx=5, pady=2)

        self.pauseImage = utils.openImageResize('buttonImages/pause.png', (20, 20))
        self.pauseButton = tk.Button(self.buttonFrame, image=self.pauseImage, command=self.pauseVideo, activebackground='blue',
                                activeforeground='white')
        self.pauseButton.grid(row=0, column=2, padx=5, pady=2)

        self.forwardImage = utils.openImageResize('buttonImages/forward.png', (20, 20))
        self.forwardButton = tk.Button(self.buttonFrame, image=self.forwardImage, command=self.forwardFrame, activebackground='blue',
                                  activeforeground='white')
        self.forwardButton.grid(row=0, column=3, padx=5, pady=2)

        self.slowImage = utils.openImageResize('buttonImages/halfspeed.png', (20, 20))
        self.slowButton = tk.Button(self.buttonFrame, image=self.slowImage, command=self.halfSpeed, activebackground='blue',
                               activeforeground='white')
        self.slowButton.grid(row=0, column=4, padx=5, pady=2)

        self.normalImage = utils.openImageResize('buttonImages/normalspeed.png', (20, 20))
        self.normalButton = tk.Button(self.buttonFrame, image=self.normalImage, command=self.normalSpeed, activebackground='blue',
                                 activeforeground='white')
        self.normalButton.grid(row=0, column=5, padx=5, pady=2)

        self.challengeImage = utils.openImageResize('buttonImages/challenge.png', (20, 20))
        self.challengeButton = tk.Button(self.buttonFrame, image=self.challengeImage, command=self.challenge, activebackground='blue',
                                    activeforeground='white')
        self.challengeButton.grid(row=0, column=6, padx=5, pady=2)

    def submitVideo(self):
        frameJump = 3
        filename = fd.askopenfilename()
        self.video = videoClass.HockeyVideo(self.root, filename, frameJump=frameJump)
        # classifyFrames() # todo: test when model not corrupted
        t = threading.Thread(target=self.video.displayFrames)
        t.start()
        self.createButtonsWidget()

    def normalSpeed(self):
        self.video.speed = 1
        self.video.nextFrameDisplayTime = time.time()

    def halfSpeed(self):
        self.video.speed = 0.3
        self.video.nextFrameDisplayTime = time.time()

    def pauseVideo(self):
        self.video.speed = 0

    def playVideo(self):
        self.video.speed = 1
        self.video.nextFrameDisplayTime = time.time()

    def reverseFrame(self):
        if self.video.frameNum - self.video.frameJump >= 0:
            self.video.frameNum -= self.video.frameJump
        print(self.video.frameNum)
        self.video.nextFrameDisplayTime = time.time()

    def forwardFrame(self):
        if self.video.frameNum + self.video.frameJump <= self.video.lastFrame:
            self.video.frameNum += self.video.frameJump
        print(self.video.frameNum)
        self.video.nextFrameDisplayTime = time.time()

    def challenge(self):
        pass