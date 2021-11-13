# library needed to acquire camera images in background
from threading import Thread

from image_helpers import *

import cv2

import numpy as np

import sys

# import gobjects library
import gi
# set gtk version
gi.require_version('Gtk', '3.0')
# import gtk library used to create gui
from gi.repository import Gtk, GdkPixbuf
# create a camera thread used to acquire images while doing other operations


class CameraThread(Thread):
    def __init__(self, camera_index, image_viewer, bin_image_viewer=None, min_threshold=0, max_threshold=255):
        """ Initialize camera acquisition thread """
        Thread.__init__(self)
        self.camera_index = camera_index
        self.image_viewer = image_viewer
        self.bin_image_viewer = bin_image_viewer
        self.vid = cv2.VideoCapture(self.camera_index)
        # set loop variable to true
        self.loop = True
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

    def run(self):
        """ Start camera acquisition """
        # while loop variable is true acquire image
        while(self.loop):
            # get BGR image from video source
            ret, img = self.vid.read()
            # if image is not empty
            if img is not None:
                # get height and width of the image
                h, w = img.shape[:2]
                # convert image from BGR to RGB (needed to display image correctly)
                image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # convert 3D image array to 1D image array
                image = np.array(image).ravel()
                # create a pixel buffer from image
                pixbuf = GdkPixbuf.Pixbuf.new_from_data(
                    image, GdkPixbuf.Colorspace.RGB, False, 8, w, h, 3*w)
                # set image viewer image to pixel buffer
                self.image_viewer.set_from_pixbuf(pixbuf)

                if self.bin_image_viewer is not None:
                    # get binary image
                    bin_img = elaborateImage(
                        img, min_threshold=self.min_threshold, max_threshold=self.max_threshold, blur_value=3)
                    # convert binary image from gray channel to rgb channel
                    bin_img = cv2.cvtColor(bin_img, cv2.COLOR_GRAY2RGB)
                    # convert 3D image array to 1D image array
                    bin_img = np.array(bin_img).ravel()
                    # create image buffer
                    pixbuf = GdkPixbuf.Pixbuf.new_from_data(
                        bin_img, GdkPixbuf.Colorspace.RGB, False, 8, w, h, 3*w)
                    # set binary image viewer to buffer image
                    self.bin_image_viewer.set_from_pixbuf(pixbuf)

    def stop(self):
        """ Stop camera acquisition and release all video resources """
        # set loop variable to false to stop image acquisition
        self.loop = False
        # release video resources
        self.vid.release()


class MainWindow():
    def __init__(self):
        # create a new gtk window
        self.win = Gtk.Window()
        # add on close function to window when close window button in clicked
        self.win.connect('destroy', self.on_close)
        # set camera thread to none
        self.camera_Thread = None
        # create a grid
        self.grid = Gtk.Grid()
        # create start button
        self.start_btn = Gtk.Button(label='Start capturing')
        # add on start button clicked function when start button is clicked
        self.start_btn.connect('clicked', self.on_start_btn_clicked)
        # add start button to grid at column 0 and row 0 and set it's width to 1 column and it's height to 1 row
        self.grid.attach(self.start_btn, 0, 0, 1, 1)
        # create a stop button
        self.stop_btn = Gtk.Button(label='Stop capturing')
        # add on stop button clicked function to stop button
        self.stop_btn.connect('clicked', self.on_stop_btn_clicked)
        # add stop button to grid at column 1, row 0, width=1 column and height=1 row
        self.grid.attach(self.stop_btn, 1, 0, 1, 1)
        # create an image viewer
        self.image_viewer = Gtk.Image.new()
        # add image viewer to grid at column 0 and row 1
        self.grid.attach(self.image_viewer, 0, 1, 1, 1)
        # create binary image viewer
        self.bin_image_viewer = Gtk.Image.new()
        # add it to the grid
        self.grid.attach(self.bin_image_viewer, 1, 1, 1, 1)

        # create minimum threshold slider
        self.min_thr_slider = Gtk.Scale.new_with_range(
            orientation=Gtk.Orientation.HORIZONTAL, min=0, max=255, step=1)
        # set slider value
        self.min_thr_slider.set_value(50)
        # add on value changed function
        self.min_thr_slider.connect(
            'value-changed', self.on_min_thr_slider_value_changed)
        # add slider to grid
        self.grid.attach(self.min_thr_slider, 1, 2, 1, 1)
        # create maximum threshold slider
        self.max_thr_slider = Gtk.Scale.new_with_range(
            orientation=Gtk.Orientation.HORIZONTAL, min=0, max=255, step=1)
        # set slider value
        self.max_thr_slider.set_value(150)
        # add on value changed function
        self.max_thr_slider.connect(
            'value-changed', self.on_max_thr_slider_value_changed)
        # add slider to grid
        self.grid.attach(self.max_thr_slider, 1, 3, 1, 1)

        # add the grid to the window
        self.win.add(self.grid)
        # show window and all it's childs
        self.win.show_all()

    def on_start_btn_clicked(self, widget):
        """ Method called when start button is clicked. It create a new camera acquisition thread and start image acquisition """
        # create a new camera acquisition thread
        self.camera_Thread = CameraThread(
            camera_index=0, image_viewer=self.image_viewer, bin_image_viewer=self.bin_image_viewer, min_threshold=int(self.min_thr_slider.get_value()), max_threshold=int(self.max_thr_slider.get_value()))
        # start acquisition
        self.camera_Thread.start()

    def on_stop_btn_clicked(self, widget):
        """ Method called when stop button is clicked. It terminate camera acquisition thread """
        if self.camera_Thread is not None:
            # call stop thread function
            self.camera_Thread.stop()
            # wait thread completition
            self.camera_Thread.join()

    def on_min_thr_slider_value_changed(self, widget):
        """ Method called when minimum threshold slider value changes """ 
        if self.camera_Thread is not None:
            self.camera_Thread.min_threshold = int(widget.get_value())

    def on_max_thr_slider_value_changed(self, widget):
        """ Method called when maximum threshold slider value changes """
        if self.camera_Thread is not None:
            self.camera_Thread.max_threshold = int(widget.get_value())

    def on_close(self, widget):
        if self.camera_Thread is not None:
            # call stop thread function
            self.camera_Thread.stop()
            # wait thread completition
            self.camera_Thread.join()
        # close gtk main loop
        Gtk.main_quit()

    def main(self):
        # start gtk main, used to make all gui working
        Gtk.main()


if __name__ == '__main__':
    # create a new mainWindow obj
    mainWindow = MainWindow()
    # start main loop
    mainWindow.main()
