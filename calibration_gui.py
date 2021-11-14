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


def imageConvert(image, image_viewer, is_binary=False):
    """ Set opencv image to GTK image widget """
    h, w = image.shape[:2]
    if is_binary:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
    # convert image from BGR to RGB (needed to display image correctly)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # convert 3D image array to 1D image array
    image = np.array(image).ravel()
    # create a pixel buffer from image
    pixbuf = GdkPixbuf.Pixbuf.new_from_data(
        image, GdkPixbuf.Colorspace.RGB, False, 8, w, h, 3*w)
    # set image viewer image to pixel buffer
    image_viewer.set_from_pixbuf(pixbuf)


class CameraThread(Thread):
    def __init__(self, camera_index, image_viewer, bin_image_viewer=None, min_threshold=0, max_threshold=255,find_circles=False):
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
        self.image=None
        self.bin_image=None
        self.find_circles=find_circles

    def run(self):
        """ Start camera acquisition """
        # while loop variable is true acquire image
        while(self.loop):
            # get BGR image from video source
            ret, self.image = self.vid.read()
            # if image is not empty
            if self.image is not None:
                if self.find_circles is not True:
                    imageConvert(self.image,self.image_viewer, False)

                if self.bin_image_viewer is not None:
                    # get binary image
                    self.bin_image = elaborateImage(
                        self.image, min_threshold=self.min_threshold, max_threshold=self.max_threshold, blur_value=3)
                    imageConvert(self.bin_image, self.bin_image_viewer, True)
                    if self.find_circles is True:
                        self.circles=getCircles(self.bin_image)
                        image=drawCircles(self.image, self.circles)
                        imageConvert(image, self.image_viewer)

    def stop(self):
        """ Stop camera acquisition and release all video resources """
        # set loop variable to false to stop image acquisition
        self.loop = False
        # release video resources
        self.vid.release()


class CalibrationGUI():
    def __init__(self):
        self.calibration_matrix=(6,7)
        # set camera thread to none
        self.camera_Thread = None
        # create a new gtk window
        self.win = Gtk.Window()
        # add on close function to window when close window button in clicked
        self.win.connect('destroy', self.on_close)
        # create calibration page
        self.calibration_window()
        


    def calibration_window(self):
        # create a grid
        self.grid = Gtk.Grid()
        # create start button
        self.start_btn = Gtk.Button(label='Start capturing')
        # add on start button clicked function when start button is clicked
        self.start_btn.connect('clicked', self.on_start_btn_clicked)
        # add start button to grid at column 0 and row 0 and set it's width to 1 column and it's height to 1 row
        self.grid.attach(self.start_btn, 0, 0, 1, 1)
        # create a stop button
        self.calibrate_btn = Gtk.Button(label='Calibrate')
        # add on stop button clicked function to stop button
        self.calibrate_btn.connect('clicked', self.on_calibrate_btn_cliked)
        # add stop button to grid at column 1, row 0, width=1 column and height=1 row
        self.grid.attach(self.calibrate_btn, 1, 0, 1, 1)
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

    def laser_window(self):
        self.grid.remove_column(1)
        self.grid.remove_column(0)
        # create start button
        self.capture_btn = Gtk.Button(label='Capture laser')
        # add on start button clicked function when start button is clicked
        self.capture_btn.connect('clicked', self.on_capture_btn_clicked)
        # add start button to grid at column 0 and row 0 and set it's width to 1 column and it's height to 1 row
        self.grid.attach(self.capture_btn, 0, 0, 1, 1)
        # create a stop button
        self.get_pos_btn = Gtk.Button(label='Get position')
        # add on stop button clicked function to stop button
        self.get_pos_btn.connect('clicked', self.on_get_pos_btn_cliked)
        # add stop button to grid at column 1, row 0, width=1 column and height=1 row
        self.grid.attach(self.get_pos_btn, 1, 0, 1, 1)
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
        # show window and all it's childs
        self.win.show_all()
        

    def on_start_btn_clicked(self, widget):
        """ Method called when start button is clicked. It create a new camera acquisition thread and start image acquisition """
        # create a new camera acquisition thread
        self.camera_Thread = CameraThread(
            camera_index=0, image_viewer=self.image_viewer, bin_image_viewer=self.bin_image_viewer, min_threshold=int(self.min_thr_slider.get_value()), max_threshold=int(self.max_thr_slider.get_value()))
        # start acquisition
        self.camera_Thread.start()

    def on_calibrate_btn_cliked(self, widget):
        """ Method called when stop button is clicked. It terminate camera acquisition thread """
        if self.camera_Thread is not None:
            # call stop thread function
            self.camera_Thread.stop()
            # wait thread completition
            self.camera_Thread.join()
            # if binary image is not none use it to calibrate
        if self.camera_Thread.bin_image is not None:
            # get calibration markers
            self.calibration_markers=getCalibrationMarkers(self.camera_Thread.bin_image,self.calibration_matrix)
            # if has found calibration markers
            if self.calibration_markers is not None:
                # get image calibration parameters
                self.newcameramtx, self.roi, self.mtx, self.dist = calibrateImage(
                    self.camera_Thread.bin_image, self.calibration_markers, calibration_matrix=self.calibration_matrix)
                print(self.newcameramtx)
                self.laser_window()

    def on_get_pos_btn_cliked(self, widget):
        print(self.camera_Thread.circles)

    def on_capture_btn_clicked(self,widget):
        self.camera_Thread = CameraThread(camera_index=0, image_viewer=self.image_viewer, bin_image_viewer=self.bin_image_viewer, min_threshold=int(self.min_thr_slider.get_value()),max_threshold=int(self.max_thr_slider.get_value()),find_circles=True)
        self.camera_Thread.start()

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
    gui = CalibrationGUI()
    # start main loop
    gui.main()
