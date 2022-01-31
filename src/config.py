import datetime

markers_distance = 120  # mm

laser_offset=-110 # mm

camera_index=2

calibration_matrix=[4,5] # rows, columns

workFolder = '/home/gianmarcococcoli/Desktop/PROVE/' + \
            datetime.today().isoformat() + '/'

average_len=10 # number of elements used to calcualte average values of circles positions

cobot_calibration_markers = [[0, 0, 0], [0, 2, 0], [0, 4, 0],
                             [1, 1, 0], [1, 3, 0],
                             [2, 1, 0], [2, 3, 0],
                             [3, 0, 0], [3, 2, 0], [3, 4, 0]]
