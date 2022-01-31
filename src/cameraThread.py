#! /usr/bin/python3
from helpers import *


import cv2

from threading import Thread, Event


class CameraThred(Thread):
    def __init__(self, color_image_widget, camera=0,image_dimensions=(640,480)):

        super(CameraThred, self).__init__()

        self.daemon = True

        self.color_image_widget = color_image_widget

        self.loop = True

        self.vid = cv2.VideoCapture(camera)
        
        self.image = None

        self.camera = camera

        self.image_dimensions=image_dimensions


    def getImagesFromVideo(self):
        ret, self.image = self.vid.read()
        self.image = cv2.resize(self.image, (int(1440/2),int(1080/2)), interpolation = cv2.INTER_AREA)
        self.image=cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def getQtImages(self):
        qt_image = convertImage(self.image,self.image_dimensions)
        self.color_image_widget.setPixmap(qt_image)

    def acquire(self):
        """ View acquired image in qt widget """
        self.getImagesFromVideo()        
        self.getQtImages()
    
    def saveImage(self, dest):
        cv2.imwrite(dest, self.image)

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
