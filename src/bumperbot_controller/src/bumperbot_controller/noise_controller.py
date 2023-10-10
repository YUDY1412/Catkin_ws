#!/usr/bin/env python3
import rospy
import numpy as np
from sensor_msgs.msg import JointState
import math
from nav_msgs.msg import Odometry
import tf_conversions 
from  tf2_ros   import TransformBroadcaster
from geometry_msgs.msg import TransformStamped


class NoiseController(object):

    def __init__(self, wheel_radius, wheel_separation):
        rospy.loginfo("Using wheel radius %d" % wheel_radius)
        rospy.loginfo("Using wheel separation %d" % wheel_separation)
        
        self.wheel_radius=wheel_radius
        self.wheel_separation=wheel_separation
        self.left_wheel_prev_pos= 0.0
        self.right_wheel_prev_pos= 0.0
        self.prev_time=rospy.Time.now()
        self.x= 0.0
        self.y= 0.0
        self.theta=0.0
        self.odom_msg =Odometry()
        self.odom_msg.header.frame_id="odom"
        self.odom_msg.child_frame_id="base_footprint_ekf"
        self.odom_msg.pose.pose.orientation.x=0.0
        self.odom_msg.pose.pose.orientation.y=0.0
        self.odom_msg.pose.pose.orientation.z=0.0
        self.odom_msg.pose.pose.orientation.w=1.0
        
        self.br =TransformBroadcaster()
        self.transform_stamp= TransformStamped()
        self.transform_stamp.header.stamp=rospy.Time.now()
        self.transform_stamp.header.frame_id="odom"
        self.transform_stamp.child_frame_id="base_footprint_ekf"

        self.odom_pub=rospy.Publisher("bumperbot_controller/odom_noisy",Odometry,queue_size=10)
        self.joint_sub=rospy.Subscriber("joint_states",JointState,self.jointcallback)
        

    def jointcallback(self, msg):
        wheel_encoder_left=msg.position[0]
        wheel_encoder_right=msg.position[1]
        dp_left= wheel_encoder_left - self.left_wheel_prev_pos
        dp_right= wheel_encoder_right - self.right_wheel_prev_pos
        dt= (msg.header.stamp - self.prev_time).to_sec()
        
        self.left_wheel_prev_pos  = msg.position[0] + np.random.normal(0,0.005)
        self.right_wheel_prev_pos = msg.position[1] + np.random.normal(0,0.005)
        self.prev_time = msg.header.stamp
        
        
        fi_left= dp_left/dt
        fi_right= dp_right/dt
        linear =self.wheel_radius * (fi_right + fi_left) / 2
        angular =self.wheel_radius * (fi_right-fi_left)/self.wheel_separation
        
        d_s=self.wheel_radius * (dp_right + dp_left) / 2
        d_theta=self.wheel_radius*(dp_right - dp_left)/ self.wheel_separation
        self.theta +=d_theta
        self.x += d_s*math.cos(self.theta)
        self.y += d_s*math.sin(self.theta)
        
        
        rospy.loginfo("linear: %f , angular: %f ",linear,angular)
        rospy.loginfo("x: %f",self.x)
        rospy.loginfo("y: %f",self.y)
        rospy.loginfo("theta: %f",self.theta)
        
        q = tf_conversions.transformations.quaternion_from_euler(0,0,self.theta)
        self.odom_msg.pose.pose.orientation.x=q[0]
        self.odom_msg.pose.pose.orientation.y=q[1]
        self.odom_msg.pose.pose.orientation.z=q[2]
        self.odom_msg.pose.pose.orientation.w=q[3]
        self.odom_msg.header.stamp=rospy.Time.now()

        self.odom_msg.pose.pose.position.x=self.x
        self.odom_msg.pose.pose.position.y=self.y
        self.odom_msg.twist.twist.linear.x =linear
        self.odom_msg.twist.twist.angular.z=angular
        self.odom_pub.publish(self.odom_msg)
        
        
        self.transform_stamp.transform.translation.x=self.x
        self.transform_stamp.transform.translation.y=self.y
        self.transform_stamp.transform.rotation.x=q[0]
        self.transform_stamp.transform.rotation.y=q[1]
        self.transform_stamp.transform.rotation.z=q[2]
        self.transform_stamp.transform.rotation.w=q[3]
        self.transform_stamp.header.stamp=rospy.Time.now()
        self.br.sendTransform(self.transform_stamp)