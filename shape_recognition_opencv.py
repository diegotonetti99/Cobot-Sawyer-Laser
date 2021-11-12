import cv2

from setup import *

from image_helpers import *

from math import sqrt, pow

import numpy as np


def main():
    # define a video capture object, index represent camera source
    vid = cv2.VideoCapture(camera_index)

    print('Press [c] when camera is ready to take calibration image')

    while True:
        # get image from video
        ret, img = vid.read()

        # get image dimensions
        img_dim = img.shape[:2]

        # show image in a window
        cv2.imshow('Image preview', img)

        # get binary image
        bin_img = elaborateImage(
            img, min_threshold=min_markers_threhsold, max_threshold=max_marker_threshold, blur_value=blur_marker)

        # show binary image
        cv2.imshow('Binary image', bin_img)

        # if c key is pressed exit while loop and continue execution
        if cv2.waitKey(1) & 0xff == ord('c'):
            break

    # get image width and height in pixels
    img_dim = img.shape[:2]

    # get calibration marker points from binary image
    calibration_markers = getCalibrationMarkers(
        bin_img, calibration_matrix=calibration_matrix)

    # if no calibration marker was found terminate execution
    if calibration_markers is None:
        print('No calibration marker was found, exiting ...')
        exit()

    # get image calibration parameters
    newcameramtx, roi, mtx, dist = calibrateImage(
        bin_img, calibration_markers, calibration_matrix=calibration_matrix)

    # exit program if no calibration marker is found

    if newcameramtx is None:

        # print why program is terminated
        print('Camera calibration failed, exiting ...')

        # close all opencv windows
        cv2.destroyAllWindows()

        # release all camera resources
        vid.release()

        # terminate execution
        exit()

    # print key needed to exit program
    print('Press [q] to exit')

    # infinite loop
    while True:

        # Capture the video frame by frame and put the frame in img in BGR format
        ret, img = vid.read()

        # undistort acquired image
        img = cv2.undistort(img, mtx, dist, None, newcameramtx)

        # get binary image
        bin_img = elaborateImage(
            img, min_threshold=min_laser_threshold, max_threshold=max_laser_threshold, blur_value=blur_laser)

        # show binary image
        cv2.imshow('bin', bin_img)

        # get circles
        detected_circles = getCircles(
            bin_img, min_radius=1, max_radius=max(img_dim))

        # print circles on image
        drawCircles(img, detected_circles)

        # display acquired image in a window
        cv2.imshow("Detected Circle", img)

        # when q button is pressed exit while loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()

    # Destroy all the windows
    cv2.destroyAllWindows()


# start program from main

if __name__ == '__main__':

    try:
        # try to execute main
        main()

    except:
        # if throw an exception during main execution print a message
        print("Can't execute the program")
