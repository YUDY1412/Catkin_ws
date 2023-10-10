#!/usr/bin/env python3
import rospy
from bumperbot_example.turtlesim_kinematics import TurtlesimKinematics

if __name__== '__main__':
    rospy.init_node('tutlesim_kinematics_node')
    turtlesim_kinematics = TurtlesimKinematics()
    rospy.loginfo("info message")
    rospy.spin()
    
    