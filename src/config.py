from datetime import datetime

import os

markers_distance = 120  # mm

laser_offset=110 # mm

camera_index=2 # 0

home_position=[-0.16, 0.45, 0.42] # m

calibration_matrix=[4,5] # rows, columns

#workFolder = '~/Desktop/PROVE/' + \
#            datetime.today().isoformat() + '/'
workFolder = os.path.join(os.path.expanduser('~/Desktop/PROVE'), datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
average_len=10 # number of elements used to calcualte average values of circles positions

cobot_calibration_markers = [[0, 0, 0], [0, 2, 0], [0, 4, 0],
                             [1, 1, 0], [1, 3, 0],
                             [2, 1, 0], [2, 3, 0],
                             [3, 0, 0], [3, 2, 0], [3, 4, 0]]
