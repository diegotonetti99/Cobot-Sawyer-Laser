import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

from image_helpers import *

from threading import Thread

import cv2

import numpy as np


class CalibrationCameraThread(Thread):

    def __init__(self, rgb_image_widget, gray_image_widget, min_thr=0, max_thr=255, blur=3):

        super(CalibrationCameraThread, self).__init__()

        self.rgb_image_widget = rgb_image_widget

        self.gray_image_widget = gray_image_widget

        self.loop = True

        self.vid = cv2.VideoCapture(0)

        self.min_thr = min_thr

        self.max_thr = max_thr

        self.blur = blur

        self.image = None

        self.newcameramtx, self.roi, self.mtx, self.dist = None, None, None, None

    def run(self):

        while self.loop:
            try:
                ret, self.image = self.vid.read()

                tk_image = convertImage(self.image)

                self.rgb_image_widget.configure(image=tk_image)

                self.rgb_image_widget.image = tk_image

                self.image = elaborateImage(self.image, self.min_thr,
                                            self.max_thr, self.blur, False)

                tk_image = convertImage(self.image)

                self.gray_image_widget.configure(image=tk_image)

                self.gray_image_widget.image = tk_image
            except:
                pass
        self.vid.release()

    def stop(self):

        self.loop = False

        self.vid.release()


class LaserAcquisitionThread(CalibrationCameraThread):

    def __init__(self, rgb_image_widget, gray_image_widget, mtx, dist, newcameramtx, min_thr=0, max_thr=255, blur=3):

        super().__init__(rgb_image_widget, gray_image_widget, min_thr, max_thr, blur)

        self.circles = None

        self.mtx = mtx
        self.dist = dist
        self.newcameramtx = newcameramtx

    def run(self):

        while self.loop:
            try:
                # get image
                ret, self.image = self.vid.read()
                # apply calibration
                self.image = cv2.undistort(
                    self.image, self.mtx, self.dist, None, self.newcameramtx)
                # apply transformation to rgb image and get binary image
                self.gray_image = elaborateImage(self.image, self.min_thr,
                                                 self.max_thr, self.blur, False)
                # convert image to gui framework
                tk_image = convertImage(self.gray_image)
                # configure image widget
                self.gray_image_widget.configure(image=tk_image)
                # set image of the widget
                self.gray_image_widget.image = tk_image
                # find circles in binary image
                self.circles = getCircles(self.gray_image)
                # draw circles in rgb image
                self.image = drawCircles(self.image, self.circles)
                # convert image to gui framework
                tk_image = convertImage(self.image)
                # configure image widget
                self.rgb_image_widget.configure(image=tk_image)
                # set imge
                self.rgb_image_widget.image = tk_image
            except:
                pass
        self.vid.release()

# create application class with frame parent


class Application(ttk.Frame):

    button_width = 30
    margins = 5

    def __init__(self, master=None):
        # initialize parent class
        ttk.Frame.__init__(self, master, padding=10)
        # initialize grid
        self.grid()
        # create all widgets
        self.widgets()
        # define thread variable
        self.thread = None
        # define calibration matrix
        self.calibration_matrix = (6, 7)
        # define calibration markers variable
        self.calibration_markers = None

    def widgets(self):
        """ Create all first page widgets """
        # create capture button
        self.captureButton = ttk.Button(
            self, text='Capture', command=self.on_capture_click, style='success.TButton', width=self.button_width)
        self.captureButton.grid(
            column=0, row=0, sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)

        # create stop button
        self.stopButton = ttk.Button(
            self, text='Stop', command=self.on_stop_click, style='danger.TButton', width=self.button_width)
        self.stopButton.grid(column=1, row=0, sticky=tk.E +
                             tk.W, padx=self.margins, pady=self.margins)

        # create calibrate button
        self.calibrateButton = ttk.Button(
            self, text='Calibrate', command=self.on_calibrate_click, style='primary.TButton', width=self.button_width)
        self.calibrateButton.grid(
            column=0, row=1, columnspan=2, sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)

        # create a vertical separator
        self.separator = ttk.Separator(self, orient=tk.VERTICAL)
        self.separator.grid(column=2, row=0, rowspan=8,
                            sticky=tk.N+tk.S, padx=self.margins, pady=self.margins)

        # create a horizontal separator
        self.h_seprarator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.h_seprarator.grid(column=0, row=6, columnspan=4,
                               sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)

        # create image widget
        self.color_image_w = ttk.Label(self, compound='image')
        self.color_image_w.grid(
            column=0, row=7, columnspan=2, sticky=tk.N+tk.E+tk.S+tk.W, padx=self.margins, pady=self.margins)

        # create gray image widget
        self.gray_image_w = ttk.Label(self, compound='image')
        self.gray_image_w.grid(
            column=3, row=7, columnspan=3, sticky=tk.N+tk.E+tk.S+tk.W, padx=self.margins, pady=self.margins)

        # create min label
        self.min_label = ttk.Label(self, text='Min')
        self.min_label.grid(column=3, row=0, sticky=tk.E,
                            padx=self.margins, pady=self.margins)

        # create min threshold slider
        self.min_threshold_scale = ttk.Scale(
            self, orient=tk.HORIZONTAL, value=50, to=255, from_=0, command=self.on_min_threshold_changed, style='primary.Horizontal.TScale')
        self.min_threshold_scale.grid(
            column=4, row=0, columnspan=1, sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)

        # create min theshold label
        self.min_thr_v = tk.StringVar()
        self.min_thr_v.set(self.scaleToInt(self.min_threshold_scale.get()))
        self.min_thr_label = ttk.Label(self, textvariable=self.min_thr_v)
        self.min_thr_label.grid(
            column=5, row=0, sticky=tk.W, padx=self.margins, pady=self.margins)

        # create max label
        self.min_label = ttk.Label(self, text='Max')
        self.min_label.grid(
            column=3, row=1, sticky=tk.E, padx=self.margins, pady=self.margins)

        # create max threshold slider
        self.max_threshold_scale = ttk.Scale(
            self, orient=tk.HORIZONTAL, value=150, to=255, from_=0, command=self.on_max_threshold_changed, style='primary.Horizontal.TScale')
        self.max_threshold_scale.grid(
            column=4, row=1, columnspan=1, sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)

        # create max theshold label
        self.max_thr_v = tk.StringVar()
        self.max_thr_v.set(self.scaleToInt(self.max_threshold_scale.get()))
        self.max_thr_label = ttk.Label(self, textvariable=self.max_thr_v)
        self.max_thr_label.grid(
            column=5, row=1, sticky=tk.W, padx=self.margins, pady=self.margins)

        # create blur label
        self.min_label = ttk.Label(self, text='Blur')
        self.min_label.grid(
            column=3, row=2, sticky=tk.E, padx=self.margins, pady=self.margins)

        # create blur slider
        self.blur_scale = ttk.Scale(
            self, orient=tk.HORIZONTAL, value=3, to=20, from_=1, command=self.on_blur_changed, style='primary.Horizontal.TScale')
        self.blur_scale.grid(column=4, row=2, columnspan=1,
                             sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)

        # create min theshold label
        self.blur_v = tk.StringVar()
        self.blur_v.set(self.scaleToInt(self.blur_scale.get()))
        self.blur_thr_label = ttk.Label(self, textvariable=self.blur_v)
        self.blur_thr_label.grid(
            column=5, row=2, sticky=tk.W, padx=self.margins, pady=self.margins)

    def on_capture_click(self):
        if self.thread is None:
            self.thread = CalibrationCameraThread(
                self.color_image_w, self.gray_image_w, self.min_threshold_scale.get(), self.max_threshold_scale.get(), self.blur_scale.get())

            self.thread.start()

    def on_capture_laser_click(self):
        if self.thread is None:
            # create new laser acquisition thread
            self.thread = LaserAcquisitionThread(self.color_image_w, self.gray_image_w, self.mtx, self.dist, self.newcameramtx, self.min_threshold_scale.get(
            ), self.max_threshold_scale.get(), self.blur_scale.get())
            # start thread
            self.thread.start()

    def on_stop_click(self):
        if self.thread is not None:
            self.thread.stop()

            self.thread = None

    def on_calibrate_click(self):
        if self.thread is not None:
            # get calbration markers from image
            self.calibration_markers = getCalibrationMarkers(
                self.thread.image, calibration_matrix=self.calibration_matrix)
            # get calibration params
            self.newcameramtx, self.roi, self.mtx, self.dist = calibrateImage(
                self.thread.image, self.calibration_markers)
            print(self.newcameramtx)

            # stop thread
            self.thread.stop()
            # join thread
            # self.thread.join()
            # set thread to none
            self.thread = None
            # remove calibrate button
            self.calibrateButton.grid_remove()
            # create get position button
            self.positionButton = ttk.Button(
                self, text='Get position', command=self.on_get_position_clicked, style='primary.TButton', width=self.button_width)
            # add button to grid
            self.positionButton.grid(
                column=0, row=1, columnspan=2, sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)
            # remove capure button
            self.captureButton.grid_remove()
            # create capture laser button
            self.captureLaserButton = ttk.Button(
                self, text='Capture', command=self.on_capture_laser_click, style='success.TButton', width=self.button_width)
            # add button to grid
            self.captureLaserButton.grid(
                column=0, row=0, sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)

    def on_get_position_clicked(self):
        if self.thread is not None:
            circles = self.thread.circles
            print(circles[0, 0])
            print(pointDistance(circles[0, 0][:2],
                  self.calibration_markers[0, 0]))

    def on_min_threshold_changed(self, value):
        self.min_thr_v.set(self.scaleToInt(value))
        if self.thread is not None:
            self.thread.min_thr = self.scaleToInt(value)

    def on_max_threshold_changed(self, value):
        self.max_thr_v.set(self.scaleToInt(value))
        if self.thread is not None:
            self.thread.max_thr = self.scaleToInt(value)

    def on_blur_changed(self, value):
        self.blur_v.set(self.scaleToInt(value))
        if self.thread is not None:
            self.thread.blur = self.scaleToInt(value)

    def scaleToInt(self, value):
        return int(float(value))


if __name__ == '__main__':
    style = Style(theme='darkly')
    app = Application()
    app.master.title('Cobot sawyer laser')
    app.mainloop()

    # execute when window is closed
    if app.thread is not None:
        app.thread.stop()
        app.thread.join()
