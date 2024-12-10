import tkinter as tk
import utils
import videoClass
from tkinter import filedialog as fd
import threading

class hockeyTkinterWindow:
    def __init__(self):
        self.video = None
        self.createWindow()

    def createWindow(self):
        self.root = tk.Tk()
        self.root.minsize(150, 100)

        submitVideoButton = tk.Button(self.root, text='Submit File', command=self.submitVideo,
                                      activebackground='blue', activeforeground='white')
        submitVideoButton.grid(row=0, column=0, pady=2)

        buttonFrame = tk.Frame(self.root, bg='grey')
        buttonFrame.grid(row=3, column=0, columnspan=6, sticky='nsew')

        reverseImage = utils.openImageResize('buttonImages/back.png', (20, 20))
        reverseButton = tk.Button(buttonFrame, image=reverseImage, command=self.tempClick, activebackground='blue',
                                  activeforeground='white')
        reverseButton.grid(row=0, column=0, padx=5, pady=2)

        playImage = utils.openImageResize('buttonImages/play.png', (20, 20))
        playButton = tk.Button(buttonFrame, image=playImage, command=self.tempClick, activebackground='blue',
                               activeforeground='white')
        playButton.grid(row=0, column=1, padx=5, pady=2)

        pauseImage = utils.openImageResize('buttonImages/pause.png', (20, 20))
        pauseButton = tk.Button(buttonFrame, image=pauseImage, command=self.tempClick, activebackground='blue',
                                activeforeground='white')
        pauseButton.grid(row=0, column=2, padx=5, pady=2)

        forwardImage = utils.openImageResize('buttonImages/forward.png', (20, 20))
        forwardButton = tk.Button(buttonFrame, image=forwardImage, command=self.tempClick, activebackground='blue',
                                  activeforeground='white')
        forwardButton.grid(row=0, column=3, padx=5, pady=2)

        slowImage = utils.openImageResize('buttonImages/halfspeed.png', (20, 20))
        slowButton = tk.Button(buttonFrame, image=slowImage, command=self.tempClick, activebackground='blue',
                               activeforeground='white')
        slowButton.grid(row=0, column=4, padx=5, pady=2)

        normalImage = utils.openImageResize('buttonImages/normalspeed.png', (20, 20))
        normalButton = tk.Button(buttonFrame, image=normalImage, command=self.tempClick, activebackground='blue',
                                 activeforeground='white')
        normalButton.grid(row=0, column=5, padx=5, pady=2)

        challengeImage = utils.openImageResize('buttonImages/challenge.png', (20, 20))
        challengeButton = tk.Button(buttonFrame, image=challengeImage, command=self.tempClick, activebackground='blue',
                                    activeforeground='white')
        challengeButton.grid(row=0, column=6, padx=5, pady=2)

        self.root.mainloop()

    def submitVideo(self):
        frameJump = 1
        filename = fd.askopenfilename()
        self.video = videoClass.HockeyVideo(self.root, filename, frameJump=frameJump)
        # classifyFrames() # todo: test when model not corrupted
        t = threading.Thread(target=self.video.displayFrames)
        t.start()

    def tempClick(self):
        self.video.speed = 0.5 # todo: fix (speed doesn't change)