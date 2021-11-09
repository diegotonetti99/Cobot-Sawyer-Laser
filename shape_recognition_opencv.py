import cv2


from math import sqrt, pow


import numpy as np


def elaborateImage(image, min_threshold=0, max_threshold=255, blur_value=3):
    """ Return a binary image where pixels with intensity between minimum and maximum threshold are set to 1, pixels with intensity out of that range are set to zero, applying BGR to gray scale and blur  """

    # convert image to grayscale

    e_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur image

    e_img = cv2.blur(e_img, (blur_value, blur_value))

    # apply threshold and return image

    return cv2.inRange(e_img, min_threshold, max_threshold)


def getCalibrationMarkers(image, calibration_matrix=(6, 7)):
    """ Returns calibration markers found in a binary image"""

    # detect circles

    ret, detected_circles = cv2.findCirclesGrid(image, calibration_matrix)

    return detected_circles


def drawCircles(image, circles, radious=10):
    """ Returns an image on which are drawn the given circles with given radious """

    # if has found circles draw them to image

    if circles is not None:

        # convert float to int16

        circles_int = np.uint16(np.around(circles))

        # iterate each circle

        for circle in circles_int[:, 0]:

            # get circle center coordinates and radious

            x, y = circle[0], circle[1]

            # draw circumference on image at coordinates (x,y) with radious r, color green and thikness 2

            cv2.circle(image, (x, y), radious, (0, 255, 0), 2)

            # draw cicle center on image at coordinates (x,y) with radious 2, color red and thikness 3

            cv2.circle(image, (x, y), 2, (0, 0, 255), 3)
    return image


def pointDistance(a, b):
    """ Returns the distance between 2 points """

    return sqrt(pow(a[0]-b[0])+pow(a[1]-b[1]))


def calibrateImage(image, calibration_matrix=(6, 7)):
    """ Return calibration parameters from a given binary image and calibration matrix size """

    # create a float32 biimensional array of zeros

    real_points = np.zeros(

        (calibration_matrix[0]*calibration_matrix[1], 3), np.float32)

    # reshape the array and fill each point with it's coordinates

    real_points[:, :2] = np.mgrid[0:calibration_matrix[1],
                                  0:calibration_matrix[0]].T.reshape(-1, 2)

    # get calibration marker points from image

    calibration_markers = getCalibrationMarkers(
        image, calibration_matrix=calibration_matrix)

    # if no calibration marker was found return None

    if calibration_matrix is None:

        return None, None

    # define real points vector (required from calibrateCamera function)

    real_points_v = []

    # add real points to real points vector

    real_points_v.append(real_points)

    # define image points vector (required)

    img_points = []

    # add obtained calibration markers to image point vector

    img_points.append(calibration_markers)

    # get image calibration parameters

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        real_points_v, img_points, img_dim, None, None)

    # get optimal calibration parameters

    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
        mtx, dist, img_dim, 1, img_dim)

    return newcameramtx, roi


def main():

    # define calibration matrix dimensions
    calibration_matrix = (6, 7)

    # define a video capture object, index represent camera source

    vid = cv2.VideoCapture(1)

    # default threshold range

    thr = [100, 200]

    # default blur value

    blur = 3

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
            img, min_threshold=thr[0], max_threshold=thr[1])

        # show binary image

        cv2.imshow('Binary image', bin_img)

        # if c key is pressed exit while loop and continue execution

        if cv2.waitKey(1) & 0xff == ord('c'):
            break

    bin_image = elaborateImage(img, min_threshold=100, max_threshold=200)

    newcameramtx, roi = calibrateImage(
        bin_image, calibration_matrix=calibration_matrix)

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

        # display acquired image in a window

        cv2.imshow("Detected Circle", img)

        # undistort acquired image

        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

        # when q button is pressed exit while loop

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break

    # After the loop release the cap object

    vid.release()

    # Destroy all the windows

    cv2.destroyAllWindows()


if __name__ == '__main__':

    # try:
    main()

    # except:

    print("Can't execute the program")
