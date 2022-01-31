#! /usr/bin/python3
from helpers import *


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
        

        self.min_thr = min_thr

        self.max_thr = max_thr

        self.blur = blur

        self.image = None

        self.gray_image = None

        self.camera = camera

        self.image_dimensions=image_dimensions

        self.newcameramtx, self.roi, self.mtx, self.dist = None, None, None, None

        self.cir_hist=[]

    def getImagesFromVideo(self):
        ret, self.image = self.vid.read()
        self.image = cv2.resize(self.image, (int(1440/2),int(1080/2)), interpolation = cv2.INTER_AREA)
        self.image=cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)


    def getQtImages(self):
        qt_image = convertImage(self.image,self.image_dimensions)
        self.color_image_widget.setPixmap(qt_image)
        qt_image = convertImage(self.gray_image,self.image_dimensions)
        self.gray_image_widget.setPixmap(qt_image)

    def acquire(self):
        """ View acquired image in qt widget """
        self.getImagesFromVideo()        
        self.gray_image = elaborateImage(self.image, self.min_thr,
                                    self.max_thr, self.blur, False)
        # convert gray image to RGB (3 gray channel) to draw color markers
        self.image=cv2.merge([self.image,self.image,self.image])
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

    def __init__(self, rgb_image_widget, gray_image_widget, mtx, dist, roi, newcameramtx, min_thr=0, max_thr=255, blur=3,camera=0,image_dimensions=(640,480),calibration_matrix=[4,5],average_len=10):

        super().__init__(rgb_image_widget, gray_image_widget, min_thr, max_thr, blur,camera=camera,image_dimensions=image_dimensions)

        self.circles = None

        self.mtx = mtx

        self.dist = dist

        self.newcameramtx = newcameramtx

        self.roi =roi

        self.calibration_matrix=calibration_matrix

        #self.image = cv2.resize(self.image, (680,400))

        self.circles_array=[]

        self.average_len=average_len
    
    def acquire(self):
        self.getImagesFromVideo()
        # apply calibration
        self.image = cv2.undistort(self.image, self.mtx, self.dist, None, self.newcameramtx)
        # crop image with roi
        x,y,w,h = self.roi
        #self.image=self.image[y:y+h, x:x+w]
        # apply transformation to rgb image and get binary image
        self.gray_image = elaborateImage(self.image, self.min_thr,
                                         self.max_thr, self.blur, False)
        # find circles in image
        self.circles = getCircles(self.gray_image)
        # order circles if number correspond to number of elements in calibration matrix
        if len(self.circles[0, :]) == self.calibration_matrix[0]*self.calibration_matrix[1]:
                self.circles = arrangeCircles(
                    self.circles, self.calibration_matrix[0], self.calibration_matrix[1])
        if len(self.circles[0,:])==self.calibration_matrix[0]*self.calibration_matrix[1] or len(self.circles[0,:])==1:
            # calc circles average
            self.circles_array.append(self.circles)
            self.circles_array=self.circles_array[-self.average_len:]
            circles_average=[[0,0,0] for i in range(self.circles[0,:])]
            for circles in self.circles_array:
                for r in range(0, len(circles[0,:])):
                    circles_average[r][0]+=circles[0,r][0]/self.average_len
                    circles_average[r][1]+=circles[0,r][1]/self.average_len
                    circles_average[r][2]+=circles[0,r][2]/self.average_len
            circles_average=[circles_average]
        
        # convert image from gray to rgb to apply color circles
        self.image=cv2.merge([self.image,self.image,self.image])
        self.image = drawCircles(self.image, self.circles)
        # draw images on widgets
        self.getQtImages()
