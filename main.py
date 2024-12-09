import tkinter as tk
import utils
import videoClass
from tkinter import filedialog as fd
import threading

def submitVideo(root):
    frameJump = 2
    filename = fd.askopenfilename()
    video = videoClass.HockeyVideo(root, filename, frameJump=frameJump)
    # classifyFrames() # todo: test when model not corrupted
    t = threading.Thread(target=video.displayFrames)
    t.start()

def tempClick():
    print('click')

root = tk.Tk()
root.minsize(150, 100)

submitVideoButton = tk.Button(root, text='Submit File', command=lambda: submitVideo(root), activebackground='blue', activeforeground='white')
submitVideoButton.grid(row=0, column=0)

reverseButton = tk.Button(root, text='r', command=tempClick, activebackground='blue', activeforeground='white')
reverseButton.grid(row=3, column=0)
playButton = tk.Button(root, text='p', command=tempClick, activebackground='blue', activeforeground='white')
playButton.grid(row=3, column=1)
forwardButton = tk.Button(root, text='f', command=tempClick, activebackground='blue', activeforeground='white')
forwardButton.grid(row=3, column=2)
slowButton = tk.Button(root, text='s', command=tempClick, activebackground='blue', activeforeground='white')
slowButton.grid(row=3, column=3)
normalButton = tk.Button(root, text='n', command=tempClick, activebackground='blue', activeforeground='white')
normalButton.grid(row=3, column=4)
challengeButton = tk.Button(root, text='c', command=tempClick, activebackground='blue', activeforeground='white')
challengeButton.grid(row=3, column=5)

root.mainloop()