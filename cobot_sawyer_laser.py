import tkinter as tk

from image_helpers import *

from threading import Thread

import cv2

import numpy as np

from PIL import Image, ImageTk

def convertImage(cv_image):

    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(cv_image)

    tk_image = ImageTk.PhotoImage(image=image)

    return tk_image


class CalibrationCameraThread(Thread):

    def __init__(self, label, min_thr=0, max_thr=255):
        super(CalibrationCameraThread, self).__init__()

        self.label = label

        self.loop = True

        self.vid = cv2.VideoCapture(0)

        self.min_thr=min_thr

        self.max_thr=max_thr

    def run(self):

        while self.loop:

            ret, image = self.vid.read()
            image = elaborateImage(image, self.min_thr, self.max_thr, 3, False)
            tk_image = convertImage(image)
            self.label.configure(image=tk_image)
            self.label.image = tk_image

        self.vid.release()

    def stop(self):

        self.loop = False

        self.vid.release()


class Application(tk.Frame):

    def __init__(self, master=None):

        tk.Frame.__init__(self, master)
        self.grid()

        self.createWidget()

        self.thread=None

    def createWidget(self):

        self.quitButton = tk.Button(self, text='Quit', command=self.quit)

        self.quitButton.grid()

        self.captureButton = tk.Button(
            self, text='Capture', command=self.on_capture_click)

        self.captureButton.grid()

        self.stopButton = tk.Button(
            self, text='Stop', command=self.on_stop_click)

        self.stopButton.grid()

        self.label = tk.Label()

        self.label.grid()

        self.min_threshold_scale=tk.Scale(self, label='Min theshold', orient=tk.HORIZONTAL,resolution=1,to=255,from_=0, command=self.on_min_threshold_changed)
        self.min_threshold_scale.grid()

        self.max_threshold_scale=tk.Scale(self, label='Max theshold', orient=tk.HORIZONTAL,resolution=1,to=255,from_=0, command=self.on_max_threshold_changed)
        self.max_threshold_scale.grid()





    def on_capture_click(self):

        self.thread = CalibrationCameraThread(self.label,self.min_threshold_scale.get(),self.max_threshold_scale.get())

        self.thread.start()

    def on_stop_click(self):

        self.thread.stop()

    def on_min_threshold_changed(self, value):
        if self.thread is not None:
            self.thread.min_thr=int(value)


    def on_max_threshold_changed(self, value):
        if self.thread is not None:
            self.thread.max_thr=int(value)




if __name__ == '__main__':

    app = Application()

    app.master.title('Cobot sawyer laser')
    app.mainloop()
