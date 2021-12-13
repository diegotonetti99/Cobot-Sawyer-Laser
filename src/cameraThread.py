#! /usr/bin/python3
from image_helpers import *

import cv2

from threading import Thread, Event


class CalibrationCameraThread(Thread):

    def __init__(self, color_image_widget, gray_image_widget, min_thr=0, max_thr=255, blur=3, camera=0,image_dimensions=(640,480)):

        super(CalibrationCameraThread, self).__init__()

        self.daemon = True

        self.color_image_widget = color_image_widget

        self.gray_image_widget = gray_image_widget

        self.loop = True

        self.vid = cv2.VideoCapture(camera)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.min_thr = min_thr

        self.max_thr = max_thr

        self.blur = blur

        self.image = None

        self.gray_image = None

        self.camera = camera

        self.image_dimensions=image_dimensions

        self.newcameramtx, self.roi, self.mtx, self.dist = None, None, None, None

    def getImagesFromVideo(self):
        ret, self.image = self.vid.read()

    def getQtImages(self):
        qt_image = convertImage(self.image,self.image_dimensions)
        self.color_image_widget.setPixmap(qt_image)
        qt_image = convertImage(self.gray_image,self.image_dimensions)
        self.gray_image_widget.setPixmap(qt_image)

    def acquire(self):
        """ View acquired image in tk widget """
        self.getImagesFromVideo()        
        self.gray_image = elaborateImage(self.image, self.min_thr,
                                    self.max_thr, self.blur, True)
        self.getQtImages()
        

    def run(self):

        while self.loop:
            try:
                self.acquire()
            except Exception as e:
                print(e)
                pass
        self.vid.release()
        return

    def stop(self):
        self.loop = False


class LaserAcquisitionThread(CalibrationCameraThread):

    def __init__(self, rgb_image_widget, gray_image_widget, mtx, dist, roi, newcameramtx, min_thr=0, max_thr=255, blur=3,camera=0,image_dimensions=(640,480)):

        super().__init__(rgb_image_widget, gray_image_widget, min_thr, max_thr, blur,camera=camera,image_dimensions=image_dimensions)

        self.circles = None

        self.mtx = mtx

        self.dist = dist

        self.newcameramtx = newcameramtx

        self.roi =roi

    def acquire(self):
        self.getImagesFromVideo()
        # apply calibration
        self.image = cv2.undistort(
            self.image, self.mtx, self.dist, None, self.newcameramtx)
        # crop image with roi
        x,y,w,h = self.roi
        self.image=self.image[y:y+h, x:x+w]
        # apply transformation to rgb image and get binary image
        self.gray_image = elaborateImage(self.image, self.min_thr,
                                         self.max_thr, self.blur, True)
        # find circles in image
        self.circles = getCircles(self.gray_image)
        # draw circles on color image
        self.image = drawCircles(self.image, self.circles)
        # draw images on widgets
        self.getQtImages()
