#! /usr/bin/python3 
import cv2

import numpy as np

from PyQt5 import QtGui

from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import Qt

from math import sqrt, pow

from config import *

def elaborateImage(image, min_threshold=0, max_threshold=255, blur_value=3, BGR=False):
    """ Return a binary image where pixels with intensity between minimum and maximum threshold are set to 1, pixels with intensity out of that range are set to zero, applying BGR to gray scale and blur  """
    image = image.copy()
    # if BGR is true return BGR binary image

    if BGR:
        e_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        e_img = cv2.blur(e_img, (blur_value, blur_value))
        e_img = cv2.inRange(e_img, min_threshold, max_threshold)
        return e_img
        # return cv2.cvtColor(e_img, cv2.COLOR_GRAY2RGB)

    else:
        # convert image to grayscale

        # blur image

        e_img = cv2.blur(image, (blur_value, blur_value))

        # apply threshold and return image

        e_img = cv2.inRange(e_img, min_threshold, max_threshold)
        return e_img


def getCircles(image, min_radius=0, max_radius=0):
    """ return a list of found circles given a binary image and minimum and maximum radius """
    # get circles
    circles = cv2.HoughCircles(image,cv2.HOUGH_GRADIENT, 1.2, 100,param1=30,param2=5,minRadius=1,maxRadius=30)
    #circles = cv2.HoughCircles(image, method=cv2.HOUGH_GRADIENT_ALT, dp=1.5,
    #                          minDist=10, param1=20, param2=0.5, minRadius=min_radius, maxRadius=max_radius)
    return circles


def getCalibrationMarkers(image, calibration_matrix=(6, 7)):
    """ Returns calibration markers found in a binary image"""
    params = cv2.SimpleBlobDetector_Params()
    params.maxArea = image.size
    params.minArea=1000
    detector = cv2.SimpleBlobDetector_create(params)
    # detect circles
    ret, detected_circles = cv2.findCirclesGrid(image, calibration_matrix,flags=cv2.CALIB_CB_SYMMETRIC_GRID)#, blobDetector=detector)
    #print(ret, detected_circles)
    return detected_circles


def drawCircles(image, circles ):
    """ Returns an image on which are drawn the given circles. Return image"""

    # if has found circles draw them to image
    image = image.copy()
    if circles is not None:
        # convert float to int16

        circles_int = np.uint16(np.around(circles))

        # iterate each circle

        for circle in circles_int[0,:]:

            # get circle center coordinates and radious
            x, y, r = circle[0], circle[1], circle[2]


            # draw circumference on image at coordinates (x,y) with radious r, color green and thikness 2

            cv2.circle(image, (x, y), r, (0, 255, 0), 2)

            # draw cicle center on image at coordinates (x,y) with radious 2, color red and thikness 3

            cv2.circle(image, (x, y), 2, (0, 0, 255), 3)
    return image

def drawGridCircles(image, circles ):
    """ Returns an image on which are drawn the given grid circles. Returns image"""

    # if has found circles draw them to image

    if circles is not None:
        # convert float to int16

        circles_int = np.uint16(np.around(circles))

        # iterate each circle

        for circle in circles_int[:, 0]:

            # get circle center coordinates and radious
            x,y,r=circle[0], circle[1], 10

            # draw circumference on image at coordinates (x,y) with radious r, color green and thikness 2

            cv2.circle(image, (x, y), r, (0, 255, 0), 2)

            # draw cicle center on image at coordinates (x,y) with radious 2, color red and thikness 3

            cv2.circle(image, (x, y), 2, (0, 0, 255), 3)
    return image



def pointDistance(a, b):
    """ Returns the distance between 2 points """

    return sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2))


def calibrateImage(image, calibration_markers, calibration_matrix=(6, 7)):
    """ Return calibration parameters from a given binary image and calibration matrix size.
    return newcameramtx, roi, mtx, dist"""

    # create a float32 biimensional array of zeros

    real_points = np.zeros(

        (calibration_matrix[0]*calibration_matrix[1], 3), np.float32)

    # reshape the array and fill each point with it's coordinates

    real_points[:, :2] = np.mgrid[0:calibration_matrix[1],
                                  0:calibration_matrix[0]].T.reshape(-1, 2)
    
    # set coordinates distance of x millimeters
    real_points=np.multiply(real_points,markers_distance)

    # if no calibration marker was found return None

    if calibration_matrix is None:

        return None, None

    # define real points vector (required from calibrateCamera function)

    real_points_v = []

    # add real points to real points vector

    real_points_v.append(real_points)

    # define image points vector (required)

    img_points = []

    # get image dimension

    img_dim = image.shape[:2]

    # add obtained calibration markers to image point vector

    img_points.append(calibration_markers)

    # get image calibration parameters

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        real_points_v, img_points, image.shape[::-1], None, None)

    # get optimal calibration parameters

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
        mtx, dist, img_dim, 1, img_dim)

    return newcameramtx, roi, mtx, dist



#def convertImage(cv_image):
#    """ Return a tk image from an opencv image """
#    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

#    image = Image.fromarray(cv_image)

#    tk_image = ImageTk.PhotoImage(image=image, )

#    return tk_image


def arrangeCircles(circles, rows, columns):
    ''' Arrange circles over a grid pattern of given rows and columns. Returns the arranged matrix. '''
    # arranged matrix
    A=[[0,0,0] for i in range(rows*columns)]
    # max and min x value
    max_x=circles[0,0][0]
    min_x=circles[0,0][0]
    # max and min y value
    max_y=circles[0,0][1]
    min_y=circles[0,0][1]
    for c in circles[0,:]:
        x,y,r=c[0],c[1],c[2]
        if x<min_x:
            min_x=x
        if x>max_x:
            max_x=x
        if y<min_y:
            min_y=y
        if y>max_y:
            max_y=y
    # calculate delta x and delta y
    delta_x=max_x-min_x
    delta_y=max_y-min_y
    # calculate x and y interval dimension
    dx=delta_x/(columns-1)
    dy=delta_y/(rows-1)
    # calculate A matrix index of circles
    for c in circles[0,:]:
        x,y=c[0],c[1]
        # row index
        i=int(round(y/dy))
        # column index
        j=int(round(x/dx))
        A[j+columns*i]=c
    return A
def convertImage(cv_image,image_dimensions=(640,480)):
    """Convert from an opencv image to QPixmap. Return QPixmap"""
    rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(image_dimensions[0], image_dimensions[1], Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)
