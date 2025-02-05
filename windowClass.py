import tkinter as tk
import utils
import videoClass
from tkinter import filedialog as fd
import threading
import time

class loginPage:
    def __init__(self, conn, cursor):
        self.root = tk.Tk()
        self.root.minsize(250, 300)
        self.conn = conn
        self.cursor = cursor
        self.club = tk.StringVar()
        self.fName = tk.StringVar()
        self.lName = tk.StringVar()
        self.password = tk.StringVar()
        self.createWindow()

    def createWindow(self):
        self.loginLabel = tk.Label(self.root, text='Sign Up')
        self.loginLabel.grid(row=0, column=0, columnspan=2, pady=2, sticky='nsew')

        self.cursor.execute('''SELECT * FROM Clubs;''')
        clubs = self.cursor.fetchall()

        self.clubDropDown = tk.OptionMenu(self.root, self.club, *clubs)
        self.clubDropDown.grid(row=1, column=1, columnspan=2, pady=2, sticky='nsew')

        self.fNameEntry = tk.Entry(self.root, textvariable=self.fName)
        self.fNameEntry.grid(row=2, column=1, columnspan=2, pady=2, sticky='nsew')

        self.lNameEntry = tk.Entry(self.root, textvariable=self.lName)
        self.lNameEntry.grid(row=3, column=1, columnspan=2, pady=2, sticky='nsew')

        self.passwordEntry = tk.Entry(self.root, textvariable=self.password, show='*')
        self.passwordEntry.grid(row=4, column=1, columnspan=2, pady=2, sticky='nsew')

        self.hockeyWindowButton = tk.Button(self.root, text='login', command=self.submitLogin)
        self.hockeyWindowButton.grid(row=5, column=1, columnspan=2, pady=2, sticky='nsew')

        self.root.mainloop()

    def submitLogin(self):
        self.clearLoginWindow()
        self.openHockeyWindow()

    def openHockeyWindow(self):
        hockeyTkinterWindow(root=self.root)

    def clearLoginWindow(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class hockeyTkinterWindow:
    def __init__(self, root=None):
        self.frameControlFlag = 0  # -1 for rewinding, 1 for forwarding, 0 for all else
        self.video = None
        if root != None:
            self.createWindow(root=root)
        else:
            self.createWindow()

    def createWindow(self, root=None):
        if root == None:
            self.root = tk.Tk()
        else:
            self.root = root
        self.root.minsize(250, 300)

        self.submitVideoButton = tk.Button(self.root, text='Submit File', command=self.submitVideo,
                                           activebackground='blue', activeforeground='white')
        self.submitVideoButton.grid(row=0, column=0, pady=2)

        self.root.after(500, self.frameControlLoop)

    def createButtonsWidget(self):
        self.buttonFrame = tk.Frame(self.root, bg='grey')
        self.buttonFrame.grid(row=3, column=0, columnspan=6, sticky='nsew')

        self.reverseImage = utils.openImageResize('buttonImages/back.png', (20, 20))
        self.reverseButton = tk.Button(self.buttonFrame, image=self.reverseImage, activebackground='blue',
                                       activeforeground='white')
        self.reverseButton.bind('<ButtonPress-1>', self.reverseFrame)
        self.reverseButton.bind('<ButtonRelease-1>', self.stopFrameControl)
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
        self.forwardButton = tk.Button(self.buttonFrame, image=self.forwardImage, activebackground='blue',
                                       activeforeground='white')
        self.forwardButton.bind('<ButtonPress-1>', self.forwardFrame)
        self.forwardButton.bind('<ButtonRelease-1>', self.stopFrameControl)
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

    def frameControlLoop(self):
        if self.frameControlFlag != 0:
            if self.frameControlFlag == 1 and self.video.frameNum + self.video.frameJump <= self.video.lastFrame:
                self.video.frameNum += self.video.frameJump

            if self.frameControlFlag == -1 and self.video.frameNum - self.video.frameJump >= 0:
                self.video.frameNum -= self.video.frameJump

            self.video.nextFrameDisplayTime = time.time()

        try:
            self.root.after(self.video.frameJump*200, self.frameControlLoop)
        except:
            self.root.after(200, self.frameControlLoop)

    def submitVideo(self):
        try:
            self.video.videoEnded = True
        except:
            print('no video')
        submitVideoThread = threading.Thread(target=self.processVideo)
        submitVideoThread.start()

    def processVideo(self):
        frameJump = 3
        filename = fd.askopenfilename()
        self.video = videoClass.HockeyVideo(self.root, filename, frameJump=frameJump)
        # classifyFrames() # todo: test when model not corrupted
        displayThread = threading.Thread(target=self.video.displayFrames)
        displayThread.start()
        self.createButtonsWidget()

    def normalSpeed(self):
        self.video.speed = 1
        self.video.nextFrameDisplayTime = time.time()

    def halfSpeed(self):
        self.video.speed = 0.3
        self.video.nextFrameDisplayTime = time.time()

    def pauseVideo(self):
        self.video.isPaused = True

    def playVideo(self):
        self.video.isPaused = False
        self.video.nextFrameDisplayTime = time.time()

    def reverseFrame(self, event):
        self.pauseVideo()
        self.frameControlFlag = -1
        if self.video.frameNum - self.video.frameJump >= 0:
            self.video.frameNum -= self.video.frameJump

    def forwardFrame(self, event):
        self.pauseVideo()
        self.frameControlFlag = 1
        if self.video.frameNum + self.video.frameJump <= self.video.lastFrame:
            self.video.frameNum += self.video.frameJump

    def stopFrameControl(self, event):
        self.frameControlFlag = 0

    def challenge(self):
        pass
