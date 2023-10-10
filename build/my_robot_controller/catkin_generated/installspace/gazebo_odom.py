#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
import math
from math import degrees
import tf_conversions
from  tf2_ros   import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

class G_O(object):
    def __init__(self) :
        self.jointstate_sub=rospy.Subscriber("joint_states",JointState,self.joinstate)
        self.odom_pub=rospy.Publisher("odom1",Odometry,queue_size=10)
        self.odom_msg=Odometry()
        self.odom_msg.header.frame_id="odom"
        self.odom_msg.child_frame_id="base_footprint"
        self.odom_msg.pose.pose.orientation.x=0
        self.odom_msg.pose.pose.orientation.y=0
        self.odom_msg.pose.pose.orientation.z=0
        self.odom_msg.pose.pose.orientation.w=1
        
        self.br =TransformBroadcaster()
        self.transform_stamp= TransformStamped()
        self.transform_stamp.header.stamp=rospy.Time.now()
        self.transform_stamp.header.frame_id="odom"
        self.transform_stamp.child_frame_id="base_footprint"

        self.x=0
        self.y=0
        self.ds=0
        self.theta=0
        self.left_angle=0
        self.right_angle=0
        self.right_angle_prev=0
        self.left_angle_prev=0
        
        self.wheelradius=0.033
        self.wheel_separation=0.092
        
        
    def joinstate(self,msg):
        self.right_angle=msg.position[1]
        self.left_angle =msg.position[0]
        
        right_angle_diff=self.right_angle-self.right_angle_prev
        left_angle_diff=self.left_angle-self.left_angle_prev
        
        self.right_angle_prev=self.right_angle
        self.left_angle_prev=self.left_angle
        
        d_right = msg.velocity[1]
        d_left = msg.velocity[0]
        
        self.linear=self.wheelradius*(d_right + d_left)/2
        self.angular=self.wheelradius*(d_right - d_left)/(self.wheel_separation)
        
        self.ds =self.wheelradius*(right_angle_diff+left_angle_diff)/2
        d_theta =self.wheelradius*(right_angle_diff-left_angle_diff)/(self.wheel_separation)
        self.theta +=d_theta
        
        self.x=self.x + self.ds*math.cos(self.theta)
        self.y=self.y +self.ds*math.sin(self.theta)
        
        if self.theta >3.14159:
            self.theta -= 3.14159*2
        elif self.theta <-3.14159:
            self.theta += 3.14159*2
        
        q = tf_conversions.transformations.quaternion_from_euler(0,0,self.theta)
        
        self.odom_msg.header.stamp=rospy.Time.now()
        self.odom_msg.pose.pose.orientation.x=q[0]
        self.odom_msg.pose.pose.orientation.y=q[1]
        self.odom_msg.pose.pose.orientation.z=q[2]
        self.odom_msg.pose.pose.orientation.w=q[3]
        
        self.odom_msg.pose.pose.position.x=self.x
        self.odom_msg.pose.pose.position.y=self.y
        self.odom_msg.twist.twist.linear.x=self.linear
        self.odom_msg.twist.twist.angular.z=self.angular
        self.odom_pub.publish(self.odom_msg)
        
        self.transform_stamp.transform.translation.x=self.x
        self.transform_stamp.transform.translation.y=self.y
        self.transform_stamp.transform.rotation.x=q[0]
        self.transform_stamp.transform.rotation.y=q[1]
        self.transform_stamp.transform.rotation.z=q[2]
        self.transform_stamp.transform.rotation.w=q[3]
        self.transform_stamp.header.stamp=rospy.Time.now()
        self.br.sendTransform(self.transform_stamp)
        
        # rospy.loginfo(degrees(self.theta))
if __name__=='__main__':
    rospy.init_node("gazebo_odom")
    rospy.loginfo("gazebo_odom is running")
    g_o=G_O()
    rospy.spin()
    