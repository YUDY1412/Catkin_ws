#!/usr/bin/env python3

import rospy
from turtlesim.msg import Pose


class TurtlesimKinematics(object):
    def __init__(self):
        self.turle1_pose_sub = rospy.Subscriber(
            "/turtle1/pose", Pose, self.turtle1Posecallback
        )
        self.turle2_pose_sub = rospy.Subscriber(
            "/turtle2/pose", Pose, self.turtle2Posecallback
        )

        self.last_turtle1_pose_ = Pose()
        self.last_turtle2_pose_ = Pose()

    def turtle1Posecallback(self, pose):
        self.last_turtle1_pose_ = pose

    def turtle2Posecallback(self, pose):
        self.last_turtle2_pose_ = pose

        Tx = self.last_turtle2_pose_.x - self.last_turtle1_pose_.x

        Ty = self.last_turtle2_pose_.y - self.last_turtle1_pose_.y
        theta_rad = self.last_turtle1_pose_.theta - self.last_turtle2_pose_.theta
        theta_deg = theta_rad * 180 / 3.14
        rospy.loginfo(
            """-------------------- \n
                       Translation Vector turtle1 -> turtle2 \n
                       Tx: %f\n
                       Ty: %f\n
                       Rotation matrix turtle 1 -> turtle2\n
                       theta_rad: %f\n
                       theta_deg: %f\n""",
            Tx,
            Ty,
            theta_rad,
            theta_deg
        )
