##### SETUP FILE #####


##### IMAGE CALIBRATION SECTION #####
# set camera index, default 0
camera_index = 0
# set number of colums and row of calibration markers matrix
calibration_matrix = (5, 7)
# set minimum light threshold for markers image processing, pixel with values less than threshold are set to 0. Range of values between 0 and 255
min_markers_threhsold = 80
# set maximum light threshold for markers image processing, pixel with values above threshold are set to 0. Range of values between 0 and 255
max_marker_threshold = 120
# set blur value for marker image processing, higher values make image less sharper. It can be usefull to remove small details or approximate shapes with rounded equivalets
blur_marker = 5


##### LASER SECTION #####
# set minimum light threshold for laser image processing
min_laser_threshold = 200
# set maximum light threshold for laser image processing
max_laser_threshold = 255
# set blur value for laser image processing
blur_laser = 5
# set minimum laser diameter, circles with diameter less than value are ignored
min_laser_diameter = 1
# set maximum laser diameter, circles with diameter above value are ignored
max_lasser_diameter = 100
