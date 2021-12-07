#! /usr/bin/env python
# Copyright (c) 2016-2018, Rethink Robotics Inc.
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

import rospy
import argparse
from intera_motion_interface import (
    MotionTrajectory,
    MotionWaypoint,
    MotionWaypointOptions
)
from intera_motion_msgs.msg import TrajectoryOptions
from geometry_msgs.msg import PoseStamped
import PyKDL
from tf_conversions import posemath
from intera_interface import Limb

from threading import Thread


class CartesianMover(Thread):
    """ create a cartesian mover thread and move cobot to position=[x,y,z] coordinats in meters. When cobot is in position it calls the given callback function  """
    def __init__(self, position,callback):
        super(CartesianMover, self).__init__()
        self.daemon = True
        self.DefaultValues()
        self.callback=callback
        self.position=position
    
    def run(self):
        self.MoveToPosition()
        self.callback(self)


    def DefaultValues(self):
        self.linear_speed = 0.6
        self.linear_accel = 0.6
        self.rotational_speed = 1.57
        self.rotational_accel = 1.57
        self.tip_name = 'right_hand'

    def MoveToPosition(self):
        try:
            rospy.init_node('go_to_cartesian_pose_py')
            limb = Limb()

            traj_options = TrajectoryOptions()
            traj_options.interpolation_type = TrajectoryOptions.CARTESIAN
            traj = MotionTrajectory(trajectory_options=traj_options, limb=limb)

            wpt_opts = MotionWaypointOptions(max_linear_speed=self.linear_speed,
                                             max_linear_accel=self.linear_accel,
                                             max_rotational_speed=self.rotational_speed,
                                             max_rotational_accel=self.rotational_accel,
                                             max_joint_speed_ratio=1.0)
            waypoint = MotionWaypoint(options=wpt_opts.to_msg(), limb=limb)

            joint_names = limb.joint_names()
            endpoint_state = limb.tip_state(args.tip_name)
            pose = endpoint_state.pose
            pose.position.x = self.position[0]
            pose.position.y = self.position[1]
            pose.position.z = self.position[2]

            poseStamped = PoseStamped()
            poseStamped.pose = pose
            # using current joint angles for nullspace bais if not provided
            joint_angles = limb.joint_ordered_angles()
            waypoint.set_cartesian_pose(
                poseStamped, self.tip_name, joint_angles)

            rospy.loginfo('Sending waypoint: \n%s', waypoint.to_string())

            traj.append_waypoint(waypoint.to_msg())

            result = traj.send_trajectory(timeout=args.timeout)
            if result is None:
                rospy.logerr('Trajectory FAILED to send')
                return

            if result.result:
                rospy.loginfo(
                    'Motion controller successfully finished the trajectory!')
            else:
                rospy.logerr('Motion controller failed to complete the trajectory with error %s',
                             result.errorId)
        except rospy.ROSInterruptException:
            rospy.logerr(
                'Keyboard interrupt detected from the user. Exiting before trajectory completion.')

