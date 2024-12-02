import tkinter as tk
import functions

root = tk.Tk()
root.minsize(150, 100)

submitVideoButton = tk.Button(root, text='Submit File', command=lambda: functions.submitVideo(root), activebackground='blue', activeforeground='white')

submitVideoButton.grid(row=0, column=0)

root.mainloop()