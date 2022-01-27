from helpers import *

import cv2

from threading import Thread, Event


class CalibrationCameraThread(Thread):

    def __init__(self, rgb_image_widget, gray_image_widget, min_thr=0, max_thr=255, blur=3, camera=0):

        super(CalibrationCameraThread, self).__init__()

        self.daemon = True

        self.rgb_image_widget = rgb_image_widget

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

        self.newcameramtx, self.roi, self.mtx, self.dist = None, None, None, None

    def acquire(self):
        """ View acquired image in tk widget """
        ret, self.image = self.vid.read()
        # resize image
        #self.image = cv2.resize(self.image, (640,400))

        self.gray_image = self.image
        tk_image = convertImage(self.image)

        self.rgb_image_widget.configure(image=tk_image)

        self.rgb_image_widget.image = tk_image

        self.image = elaborateImage(self.image, self.min_thr,
                                    self.max_thr, self.blur, True)

        tk_image = convertImage(self.image)

        self.gray_image_widget.configure(image=tk_image)

        self.gray_image_widget.image = tk_image

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

    def __init__(self, rgb_image_widget, gray_image_widget, mtx, dist, newcameramtx, min_thr=0, max_thr=255, blur=3,camera_index=0):

        super().__init__(rgb_image_widget, gray_image_widget, min_thr, max_thr, blur,camera=camera_index)

        self.circles = None

        self.mtx = mtx

        self.dist = dist

        self.newcameramtx = newcameramtx

    def acquire(self):
        # get image
        ret, self.image = self.vid.read()

        #self.image = cv2.resize(self.image, (680,400))
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
