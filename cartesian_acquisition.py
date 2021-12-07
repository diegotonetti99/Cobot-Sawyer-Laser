#! /usr/bin/env python
# Copyright (c) 2013-2018, Rethink Robotics Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Intera SDK Joint Position Waypoints Example
"""
import argparse
import sys

import rospy

import csv

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import intera_interface

from threading import Thread

from intera_motion_interface import (
    MotionTrajectory,
    MotionWaypoint,
    MotionWaypointOptions
)

class Waypoints(object):
    def __init__(self, speed, accuracy, limb="right"):
        # Create intera_interface limb instance
        self._arm = limb
        self._limb = intera_interface.Limb(self._arm)
        

        # Parameters which will describe joint position moves
        self._speed = speed
        self._accuracy = accuracy

        # Recorded waypoints
        self._waypoints = list()

        # Recording state
        self._is_recording = False

        # Verify robot is enabled
        print("Getting robot state... ")
        self._rs = intera_interface.RobotEnable()
        self._init_state = self._rs.state().enabled
        print("Enabling robot... ")
        self._rs.enable()

        # Create Navigator I/O
        self._navigator = intera_interface.Navigator()

    def _record_waypoint(self, value):
        """
        Stores joint position waypoints

        Navigator 'OK/Wheel' button callback
        """
        if value:
            print("Waypoint Recorded")
            # add to the list x,y,z coordinates
            self._waypoints.append(self._limb.endpoint_pose()['position'][:])

    def _stop_recording(self, value):
        """
        Sets is_recording to false

        Navigator 'Rethink' button callback
        """
        # On navigator Rethink button press, stop recording
        if value:
            print("Recording Stopped")
            self._is_recording = False

    def record(self):
        """
        Records joint position waypoints upon each Navigator 'OK/Wheel' button
        press.
        """
        rospy.loginfo("Waypoint Recording Started")
        print("Press Navigator 'OK/Wheel' button to record a new joint "
        "joint position waypoint.")
        print("Press Navigator 'Rethink' button when finished recording "
              "waypoints to begin playback")
        # Connect Navigator callbacks
        # Navigator scroll wheel button press
        ok_id = self._navigator.register_callback(self._record_waypoint, 'right_button_ok')
        # Navigator Rethink button press
        show_id = self._navigator.register_callback(self._stop_recording, 'right_button_show')

        # Set recording flag
        self._is_recording = True

        # Loop until waypoints are done being recorded ('Rethink' Button Press)
        while not rospy.is_shutdown() and self._is_recording:
            rospy.sleep(1.0)

        # We are now done with the navigator callbacks, disconnecting them
        self._navigator.deregister_callback(ok_id)
        self._navigator.deregister_callback(show_id)


    def clean_shutdown(self):
        print("\nExiting example...")
        return True

class CobotCalibrator(Thread):
    def __init__(self,callback,label):
        super(CobotCalibrator,self).__init__()
        self.daemon=True
        self.callback=callback
        self.label=label
        self.speed=0.3
        self.accuracy=intera_interface.settings.JOINT_ANGLE_TOLERANCE
    

    def run(self):
        self.calibrateCobot()
        self.callback(self)

    def calibrateCobot():
        """Records joint positions each time the navigator 'OK/wheel'
        button is pressed.
        Upon pressing the navigator 'Rethink' button, the recorded joint positions
        """
        

        self.label.setText("Initializing node... ")
        rospy.init_node("sdk_joint_position_waypoints", anonymous=True)

        waypoints = Waypoints(self.speed, self.accuracy)

        # Register clean shutdown
        rospy.on_shutdown(waypoints.clean_shutdown)

        # Begin example program
        waypoints.record()

        # Print waypoints
        self.label.setText(waypoints._waypoints)

        # Save csv file with robot coordinates
        with open('cobot_acquired_points.csv', 'w', newline='') as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(waypoints._waypoints)

        # display waypoints coordinates in 3d scatter plot
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        for point in waypoints._waypoints:
            ax.scatter(point[0],point[1],point[2])
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        ax.set_xlim(0,1)
        ax.set_ylim(0,1)
        ax.set_zlim(0,1)
        plt.show()


