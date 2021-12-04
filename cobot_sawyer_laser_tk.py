import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

from image_helpers import *

from cameraThread import *

import json

# create application class with frame parent


class Application(ttk.Frame):

    button_width = 30
    margins = 5

    def __init__(self, master=None):
        # initialize parent class
        ttk.Frame.__init__(self, master, padding=10)
        #self.event_add(tk.EventType.Destroy, self.on_closing)
        self.winfo_toplevel().protocol("WM_DELETE_WINDOW", self.on_closing)
        # initialize grid
        self.grid()
        # load user params
        self.getParams()
        # create all widgets
        self.widgets()
        # define thread variable
        self.thread = None
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
        self.stopButton.grid(column=1, row=0, columnspan=2, sticky=tk.E +
                             tk.W, padx=self.margins, pady=self.margins)

        # create calibrate button
        self.calibrateButton = ttk.Button(
            self, text='Calibrate', command=self.on_calibrate_click, style='primary.TButton', width=self.button_width)
        self.calibrateButton.grid(
            column=0, row=1, sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)

        # camera label
        self.camera_label = ttk.Label(self, text='Camera index')
        self.camera_label.grid(column=1, row=1, sticky=tk.E,
                               padx=self.margins, pady=self.margins)

        # camera text
        self.camera_entry = ttk.Entry(self, textvariable=self.camera_v)
        self.camera_entry.grid(
            column=2, row=1, padx=self.margins, pady=self.margins)

        # calibration matrix label
        self.calibration_matrix_label = ttk.Label(
            self, text='Calibration matrix (r, c)')
        self.calibration_matrix_label.grid(
            column=0, row=2, padx=self.margins, pady=self.margins)

        # calibration row value
        self.row_entry = ttk.Entry(self, textvariable=self.row_v)
        self.row_entry.grid(
            column=1, row=2, padx=self.margins, pady=self.margins)

        # calibration column value
        self.column_entry = ttk.Entry(self, textvariable=self.column_v)
        self.column_entry.grid(
            column=2, row=2, padx=self.margins, pady=self.margins)

        # create a vertical separator
        self.separator = ttk.Separator(self, orient=tk.VERTICAL)
        self.separator.grid(column=3, row=0, rowspan=8,
                            sticky=tk.N+tk.S, padx=self.margins, pady=self.margins)

        # create a horizontal separator
        self.h_seprarator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.h_seprarator.grid(column=0, row=6, columnspan=7,
                               sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)

        # create image widget
        self.color_image_w = ttk.Label(self, compound='image')
        self.color_image_w.grid(
            column=0, row=7, columnspan=3, sticky=tk.N+tk.E+tk.S+tk.W, padx=self.margins, pady=self.margins)

        # create gray image widget
        self.gray_image_w = ttk.Label(self, compound='image')
        self.gray_image_w.grid(
            column=4, row=7, columnspan=3, sticky=tk.N+tk.E+tk.S+tk.W, padx=self.margins, pady=self.margins)

        # create min label
        self.min_label = ttk.Label(self, text='Min')
        self.min_label.grid(column=4, row=0, sticky=tk.E,
                            padx=self.margins, pady=self.margins)

        # create min threshold slider
        self.min_threshold_scale = ttk.Scale(
            self, orient=tk.HORIZONTAL, value=int(self.min_thr_v.get()), to=255, from_=0, command=self.on_min_threshold_changed, style='primary.Horizontal.TScale')
        self.min_threshold_scale.grid(
            column=5, row=0, columnspan=1, sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)

        # create min theshold label
        self.min_thr_label = ttk.Label(self, textvariable=self.min_thr_v)
        self.min_thr_label.grid(
            column=6, row=0, sticky=tk.W, padx=self.margins, pady=self.margins)

        # create max label
        self.min_label = ttk.Label(self, text='Max')
        self.min_label.grid(
            column=4, row=1, sticky=tk.E, padx=self.margins, pady=self.margins)

        # create max threshold slider
        self.max_threshold_scale = ttk.Scale(
            self, orient=tk.HORIZONTAL, value=int(self.max_thr_v.get()), to=255, from_=0, command=self.on_max_threshold_changed, style='primary.Horizontal.TScale')
        self.max_threshold_scale.grid(
            column=5, row=1, columnspan=1, sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)

        # create max theshold label
        self.max_thr_label = ttk.Label(self, textvariable=self.max_thr_v)
        self.max_thr_label.grid(
            column=6, row=1, sticky=tk.W, padx=self.margins, pady=self.margins)

        # create blur label
        self.min_label = ttk.Label(self, text='Blur')
        self.min_label.grid(
            column=4, row=2, sticky=tk.E, padx=self.margins, pady=self.margins)

        # create blur slider
        self.blur_scale = ttk.Scale(
            self, orient=tk.HORIZONTAL, value=int(self.blur_v.get()), to=20, from_=1, command=self.on_blur_changed, style='primary.Horizontal.TScale')
        self.blur_scale.grid(column=5, row=2, columnspan=1,
                             sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)

        # create min theshold label 
        self.blur_thr_label = ttk.Label(self, textvariable=self.blur_v)
        self.blur_thr_label.grid(
            column=6, row=2, sticky=tk.W, padx=self.margins, pady=self.margins)

    def on_capture_click(self):
        if self.thread is None:
            # create camera thread to execute acquisitin in parallel
            self.thread = CalibrationCameraThread(
                self.color_image_w, self.gray_image_w, self.min_threshold_scale.get(), self.max_threshold_scale.get(), self.blur_scale.get(), int(self.camera_v.get()))
            # start camera acquisition loop
            self.thread.start()

    def on_capture_laser_click(self):
        if self.thread is None:
            # create new laser acquisition thread
            self.thread = LaserAcquisitionThread(self.color_image_w, self.gray_image_w, self.mtx, self.dist, self.newcameramtx, self.min_threshold_scale.get(
            ), self.max_threshold_scale.get(), self.blur_scale.get(), int(self.camera_v.get()))
            # start thread
            self.thread.start()

    def on_stop_click(self):
        if self.thread is not None:
            self.thread.stop()
            self.thread = None

    def on_calibrate_click(self):
        if self.thread is not None:
            self.calibration_matrix=(int(self.row_v.get()), int(self.column_v.get()))
            # get calbration markers from image
            self.calibration_markers = getCalibrationMarkers(
                self.thread.image, calibration_matrix=self.calibration_matrix)
            print(self.calibration_markers)
            if self.calibration_markers is not None:
                # get calibration params
                self.newcameramtx, self.roi, self.mtx, self.dist = calibrateImage(
                    self.thread.image, self.calibration_markers, self.calibration_matrix)
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
                    column=0, row=1, sticky=tk.E+tk.W, padx=self.margins, pady=self.margins)
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

    def saveParams(self):
        """ Save user params to data.json """
        # create data struct
        data = {
            "camera": int(self.camera_v.get()),
            "rows": int(self.row_v.get()),
            "columns": int(self.column_v.get()),
            "min_thr": int(self.min_thr_v.get()),
            "max_thr": int(self.max_thr_v.get()),
            "blur": int(self.blur_v.get())
        }
        # open data.json in write mode
        with open('data.json', 'w') as file:
            # write data to file
            json.dump(data, file)

    def getParams(self):
        """ get user params """
        self.camera_v = tk.StringVar(value=0)
        self.min_thr_v = tk.IntVar(value=50)
        self.max_thr_v=tk.IntVar(value=150)
        self.row_v=tk.IntVar(value=6)
        self.column_v=tk.IntVar(value=7)
        self.blur_v=tk.IntVar(value=3)
        # try to open data.json
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
            self.camera_v.set(data['camera'])
            self.row_v.set(data['rows'])
            self.column_v.set(data['columns'])
            self.min_thr_v.set(data['min_thr'])
            self.max_thr_v.set(data['max_thr'])
            self.blur_v.set(data['blur'])
        except:
            pass

    def on_closing(self):
        if self.thread is not None:
            self.saveParams()
            self.thread.stop()

        self.quit()


if __name__ == '__main__':
    print('Starting program')
    style = Style(theme='darkly')
    app = Application()
    app.master.title('Cobot sawyer laser')
    app.mainloop()
    print('Execution terminated')
