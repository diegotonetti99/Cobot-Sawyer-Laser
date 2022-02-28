# Cobot-Sawyer-Laser

This repo contains all scripts and programs used to evalutate repeteability of a Sawyer Cobot using a laser pointer mounted on cobot's tip. 
Python scripts are tested with ROS noetic and intera SDK, which are essential to control the cobot. Image acquisition and data extraction is obtained using OpenCV. 
In order to create an easier experience Qt5 has been used to implement GUI for the programs.

Cobot calibration is obtained with a 10 points manual calibration over a predefined pattern. All markers are placed on a 4 rows by 5 columns grid, each marker is spaced by 120 mm and with 
a radious of 20 mm.
