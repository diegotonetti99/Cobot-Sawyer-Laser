import tkinter as tk
from tkinter import ttk

from image_helpers import *

from threading import Thread

import cv2

import numpy as np


from PIL import Image, ImageTk

def convertImage(cv_image):
    """ Return a tk image from an opencv image """
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(cv_image)

    tk_image = ImageTk.PhotoImage(image=image)

    return tk_image

class CalibrationCameraThread(Thread):


    def __init__(self, rgb_image,gray_image, min_thr=0, max_thr=255):

        super(CalibrationCameraThread, self).__init__()

        self.rgb_image = rgb_image

        self.gray_image=gray_image

        self.loop = True

        self.vid = cv2.VideoCapture(0)

        self.min_thr=min_thr

        self.max_thr=max_thr


    def run(self):

        while self.loop:
            ret, image = self.vid.read()

            tk_image = convertImage(image)

            self.rgb_image.configure(image=tk_image)

            self.rgb_image.image = tk_image

            image = elaborateImage(image, self.min_thr, self.max_thr, 3, False)

            tk_image = convertImage(image)

            self.gray_image.configure(image=tk_image)

            self.gray_image.image = tk_image

        self.vid.release()


    def stop(self):

        self.loop = False

        self.vid.release()



class Application(ttk.Frame):


    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)

        self.grid()

        self.createWidget()

        self.thread=None


    def createWidget(self):

        self.quitButton = ttk.Button(self, text='Quit', command=self.quit)

        self.quitButton.grid(column=0, row=0)

        self.captureButton = ttk.Button(self, text='Capture', command=self.on_capture_click)

        self.captureButton.grid(column=1, row=0)

        self.stopButton = ttk.Button(self, text='Stop', command=self.on_stop_click)

        self.stopButton.grid(column=2,row=0)

        self.color_image = ttk.Label()

        self.color_image.grid(column=0,row=1)

        self.gray_image = ttk.Label()

        self.gray_image.grid(column=1,row=1)


        self.min_threshold_scale=ttk.Scale(self, orient=tk.HORIZONTAL,value=10,to=255,from_=0, command=self.on_min_threshold_changed)
        self.min_threshold_scale.grid(column=1,row=2)

        self.max_threshold_scale=ttk.Scale(self, orient=tk.HORIZONTAL,value=240,to=255,from_=0, command=self.on_max_threshold_changed)

        self.max_threshold_scale.grid(column=1,row=3)






    def on_capture_click(self):
        if self.thread is None:
            self.thread = CalibrationCameraThread(self.color_image,self.gray_image,self.min_threshold_scale.get(),self.max_threshold_scale.get())

            self.thread.start()


    def on_stop_click(self):
        if self.thread is not None:
            self.thread.stop()
            #self.thread.join()
            self.thread = None


    def on_min_threshold_changed(self, value):
        if self.thread is not None:
            self.thread.min_thr=int(float(value))



    def on_max_threshold_changed(self, value):
        if self.thread is not None:
            self.thread.max_thr=int(float(value))





if __name__ == '__main__':
    app = Application()
    app.master.title('Cobot sawyer laser')
    app.mainloop()

    # execute when window is closed
    if app.thread is not None:
        app.thread.stop()
        app.thread.join()

