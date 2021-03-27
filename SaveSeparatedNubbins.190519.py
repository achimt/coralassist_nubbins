#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 09:50:21 2019

@author: achim
"""
# Import libraries. 
# cv2 crucial for the image handling
# tkinter for the GUI
# PIL image as this works well with tkinter
import pandas as pd
import cv2
import tkinter as tk
import PIL.Image, PIL.ImageTk
from os.path import join

# function to increase the width of the chopping comb. This (like the other 
# functions) is implemented with ugly global variables. But it works and the
# program is just about small enough to not loose the way. 
def increase_width(startRow=0, endRow=1599):
    global photo
    global smallImg
    global w
    global s
    w=int(w*1.03)
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(smallImg))
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    #print("width increased", w)
    for i in range(7):
        canvas.create_line(i*w + s, 
                           startRow, 
                           i*w + s, 
                           endRow, 
                           fill="yellow", 
                           width=10)
        
# this function decreases the width of the individual nubbin slices
def decrease_width(startRow=0, endRow=1599):
    global photo
    global smallImg
    global w
    global s
    w=int(w*.97)
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(smallImg))
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    #print("width decreased", w)
    for i in range(7):
        canvas.create_line(i*w + s, 
                           startRow, 
                           i*w + s, 
                           endRow, 
                           fill="yellow", 
                           width=10)

# this function is important as it shifts the start position of all the
# nubbin slices to the left. It should be called at the beginning of every 
# cycle through an image. 
def increase_shift(startRow=0, endRow=1599):
    global photo
    global smallImg
    global w
    global s
    s=int(s*1.03)
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(smallImg))
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    #print("shift increased", s)
    for i in range(7):
        canvas.create_line(i*w + s, 
                           startRow, 
                           i*w + s, 
                           endRow, 
                           fill="yellow", 
                           width=10)
        
# decrease_shift shifts the position of all nubbin slices to the right. 
def decrease_shift(startRow=0, endRow=1599):
    global photo
    global smallImg
    global w
    global s
    s=int(s*.97)
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(smallImg))
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    #print("shift decreased", s)
    for i in range(7):
        canvas.create_line(i*w + s, 
                           startRow, 
                           i*w + s, 
                           endRow, 
                           fill="yellow", 
                           width=10)
        
# This is the crucial function that generates a name for each nubbin slice
        # consisting of the nubbin name and the image acquisition date. Then
        # the function generates slices of the large image of the aquarium
        # that correspond to the vertical yellow lines in the GUI. It saves 
        # the nubbin slices and generates an entry into a logfile. 
def close_window(window, fileDir, fileName, logFileName, nubbin, nubbinDate):
    global photo
    global smallImg
    global w
    global s
    fileDir = "/home/achim/dataDrive/corals/acroporaImages/singleNubbinImg/"
    startRow, endRow = 0, 1599
    #print(fileName, w, s)
    for i in range(len(nubbin)):
        if not pd.isnull(nubbin[i]):
            nubbin[i]=str(int(nubbin[i]))
    for i in range(6):
        startCol, endCol = i*w+s, (i+1)*w+s
        croppedImg = smallImg[startRow:endRow, startCol:endCol]
        croppedImg = cv2.cvtColor(croppedImg, cv2.COLOR_BGR2RGB)
        #print(type(nubbin))
        if not pd.isnull(nubbin[i]):
            fn = join(fileDir, nubbin[i] + '_' + nubbinDate + '.jpg')
            #print(fn)
            cv2.imwrite(fn, croppedImg)
        logLine = [nubbin[i],nubbinDate, fileName, i, s, w]
        logLine = ",".join(str(x) for x in logLine)
        print(logLine)
        logLine = logLine + '\n'
        with open(logFileName, "a") as logfile:
            logfile.write(logLine)

    window.destroy()
        

def loadImage(fileDir, fileName, logFileName, nubbin, nubbinDate):
    window = tk.Tk()
    global smallImg
    global photo
    global canvas
    # OpenCV needs to convert the image from BGR to RGB, as 
    # Tkinter sees the color channes in a different order
    img = cv2.cvtColor(cv2.imread(join(fileDir, fileName)), cv2.COLOR_BGR2RGB)
    smallImg = cv2.resize(img,(1600,1200))

    # construct a canvas
    height, width, channels = smallImg.shape
    canvas = tk.Canvas(window, width=width, height=height)
    canvas.pack()
    
    # Add the photo to the canvas
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(smallImg))
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    
    # Add six lines to the canvas
    w=200
    s=120
    startRow=0
    endRow=1599
    for i in range(7):
        canvas.create_line(i*w + s, 
                           startRow, 
                           i*w + s, 
                           endRow, 
                           fill="yellow", 
                           width=10)
    
    # Add buttons
    btnWidthIncr = tk.Button(window,
                         text="Increase Width",
                         width=50,
                         command=lambda: increase_width())
    btnWidthIncr.pack(anchor=tk.S, expand=True)
    
    btnWidthDecr = tk.Button(window,
                         text="Decrease Width",
                         width=50,
                         command=lambda: decrease_width())
    btnWidthDecr.pack(anchor=tk.S, expand=True)
    
    btnShiftIncr = tk.Button(window,
                         text="Increase Shift",
                         width=50,
                         command=lambda: increase_shift())
    btnShiftIncr.pack(anchor=tk.S, expand=True)
    
    btnShiftDecr = tk.Button(window,
                         text="Decrease Shift",
                         width=50,
                         command=lambda: decrease_shift())
    btnShiftDecr.pack(anchor=tk.S, expand=True)
    
    btnClose = tk.Button(window, 
                         text="Save", 
                         width=12, 
                         command=lambda: close_window(window, 
                                                      fileDir, 
                                                      fileName, 
                                                      logFileName, 
                                                      nubbin, 
                                                      nubbinDate))
    btnClose.pack(anchor=tk.S, expand=True)
    
    window.mainloop()
    return(w, s)

fileDir = "/home/achim/dataDrive/corals/acroporaImages/"
fileDate = "190519"
fileName = fileDate + ".csv"
logName = fileDate + ".log"
file = fileName
fileName = join(fileDir, file)

w=200
s=120
startRow=0
endRow=1599


imageList = pd.read_csv(fileName, dtype=object)
fileDate = fileDate[2:4] + '.' + fileDate[4:] + '.' + fileDate[:2]
fileDir = "/home/achim/dataDrive/corals/acroporaImages/" + fileDate + "/"
logFileHeader = 'nubbin,nubbinDate,fileName,#,start,width\n'
logFileName = join(fileDir, logName)
with open("logFileName", "w") as logFile:
    logFile.write(logFileHeader)
    print(logFileHeader)
logFile.close()

for i in range(len(imageList)):
    fileName = imageList.iloc[i][1] + '.JPG'
    nubbinDate = imageList.iloc[i][0]
    nubbin = imageList.iloc[i][4:10]
    print(i, fileName, nubbinDate)
    for j in range(len(nubbin)):
        if not pd.isnull(nubbin[j]):
            nubbin[j]=str(int(nubbin[j]))
    #print(nubbin, nubbinDate)
    loadImage(fileDir, 
              fileName,
              logFileName, 
              nubbin, 
              nubbinDate)
    
    


