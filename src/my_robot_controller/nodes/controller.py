#!/usr/bin/env python3
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64

def cmdcallback(msg):
    robot_speed= np.array([[msg.linear.x],[msg.angular.z]])
    wheel_speed=np.matmul(np.linalg.inv(speed_conversion),robot_speed)
    rightspeed=Float64(wheel_speed[0,0])
    leftspeed=Float64(wheel_speed[1,0])
    right_cmd_pub.publish(rightspeed)
    left_cmd_pub.publish(leftspeed)
    
if __name__ =='__main__':
    rospy.init_node("controller_for_gazebo")
    
    global speed_conversion 
    global right_cmd_pub
    global left_cmd_pub
    right_cmd_pub=rospy.Publisher("wheel_right_controller/command",Float64,queue_size=1)
    left_cmd_pub=rospy.Publisher("wheel_left_controller/command",Float64,queue_size=1)
    cmd_sub=rospy.Subscriber("cmd_vel",Twist,cmdcallback)
    wheel_radius=0.033
    wheel_separation=0.092
    speed_conversion =np.array([[wheel_radius/2, wheel_radius/2],
                                           [wheel_radius/wheel_separation, -wheel_radius/wheel_separation]])
    rospy.spin()
    