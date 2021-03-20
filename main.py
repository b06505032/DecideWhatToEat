from view import * 
from tkinter import * 
from PIL import ImageTk, Image


WIDTH, HEIGTH = 372, 662 # 414, 736 

def center_window(root, width, height): 
    screenwidth = root.winfo_screenwidth() 
    screenheight = root.winfo_screenheight() 
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2) 
    root.geometry(size) 

root = Tk() 
center_window(root, WIDTH, HEIGTH)
root.resizable(width=False, height=False) 
root.title('Decide What to Eat!')
root.width = WIDTH
root.height = HEIGTH

ExamPage(root) 
root.mainloop()

