#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32
import math
import tf_conversions
from  tf2_ros   import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
def left_callback(msg):
    pass
def right_callback(msg):
    pass

class DiffTf:
    def __init__(self):
        self.wheelradius=0.065
        self.wheel_separation=0.13
        self.left_tick_sub=rospy.Subscriber("left_ticks",Int32,self.left_callback) 
        self.right_tick_sub=rospy.Subscriber("right_ticks",Int32,self.right_callback) 
        self.odom_pub=rospy.Publisher("/odom",Odometry,queue_size=10)

        self.encoder_max=  2147483648
        self.encoder_min= -2147483648
        self.encoder_low_wrap =(self.encoder_max - self.encoder_min) * 0.3 + self.encoder_min
        self.encoder_high_wrap = (self.encoder_max - self.encoder_min) * 0.7 + self.encoder_min       
        self.lmult=0
        self.rmult=0
        
        self.right=0
        self.left=0

        self.rate=10
        self.x=0
        self.y=0
        self.ds=0
        self.theta=0
        self.left_angle=0
        self.right_angle=0
        self.right_angle_prev=0
        self.left_angle_prev=0
        self.left_wheel_prev_pos=0.0
        self.right_wheel_prev_pos=0.0
        self.Time_Prev=rospy.Time.now()
        self.t_delta = rospy.Duration(1.0/self.rate)
        self.t_next = rospy.Time.now() + self.t_delta
        
        self.linear=0
        self.Angular=0
        self.odom_msg=Odometry()
        self.odom_msg.header.frame_id="odom"
        self.odom_msg.child_frame_id="base_footprint"
        self.odom_msg.pose.pose.orientation.x=0
        self.odom_msg.pose.pose.orientation.y=0
        self.odom_msg.pose.pose.orientation.z=0
        self.odom_msg.pose.pose.orientation.w=1
        
        self.tf_pub=TransformBroadcaster()
        self.tf=TransformStamped()
        self.tf.header.frame_id="odom"
        self.tf.child_frame_id="base_footprint"
        
    def left_callback(self,msg):
        enc=msg.data
        if (enc < self.encoder_low_wrap and self.prev_lencoder > self.encoder_high_wrap):
            self.lmult = self.lmult + 1
            
        if (enc > self.encoder_high_wrap and self.prev_lencoder < self.encoder_low_wrap):
            self.lmult = self.lmult - 1
            
        self.left = 1.0 * (enc + self.lmult * (self.encoder_max - self.encoder_min)) 
        self.prev_lencoder = enc
        
        rospy.loginfo(msg.data)
          
    def right_callback(self,msg):
        enc = msg.data
        if(enc < self.encoder_low_wrap and self.prev_rencoder > self.encoder_high_wrap):
            self.rmult = self.rmult + 1
        
        if(enc > self.encoder_high_wrap and self.prev_rencoder < self.encoder_low_wrap):
            self.rmult = self.rmult - 1
            
        self.right = 1.0 * (enc + self.rmult * (self.encoder_max - self.encoder_min))

        self.prev_rencoder = enc
 
        rospy.loginfo(msg.data)   

    def spin(self):
        rate=rospy.Rate(10)
        while not rospy.is_shutdown():
            self.update()
            rate.sleep()

    def update(self):
        
        
        now =rospy.Time.now()
        if (now >self.t_next):
            
            self.right_angle= self.right * 2 * 3.14/20
            self.left_angle=  self.left  * 2 * 3.14/20
            right_angle_diff=self.right_angle-self.right_angle_prev
            left_angle_diff=self.left_angle-self.left_angle_prev
            
            dt= (now - self.Time_Prev).to_sec()
            
            self.right_angle_prev=self.right_angle
            self.left_angle_prev=self.left_angle
            self.Time_Prev=rospy.Time.now()
            
            d_right=(self.right_angle-self.right_wheel_prev_pos)/dt
            d_left=(self.left_angle -self.left_wheel_prev_pos)/dt
            
            self.left_wheel_prev_pos=self.left_angle
            self.right_wheel_prev_pos =self.right_angle
            
            self.linear=self.wheelradius*(d_right + d_left)/2
            self.angular=self.wheelradius*(d_right - d_left)/(2*self.wheel_separation)
            
            self.ds =self.wheelradius*(right_angle_diff+left_angle_diff)/2
            d_theta =self.wheelradius*(right_angle_diff-left_angle_diff)/(2*self.wheel_separation)
            self.theta +=d_theta
            
            self.x=self.x + self.ds*math.cos(self.theta)
            self.y=self.y +self.ds*math.sin(self.theta)

            q = tf_conversions.transformations.quaternion_from_euler(0,0,self.theta)
            
            self.odom_msg.header.stamp=rospy.Time.now()
            
            self.odom_msg.pose.pose.orientation.x=q[0]
            self.odom_msg.pose.pose.orientation.y=q[1]
            self.odom_msg.pose.pose.orientation.z=q[2]
            self.odom_msg.pose.pose.orientation.w=q[3]
            self.odom_msg.header.stamp=rospy.Time.now()
            
            self.odom_msg.pose.pose.position.x=self.x
            self.odom_msg.pose.pose.position.y=self.y
            self.odom_msg.twist.twist.linear.x=self.linear
            self.odom_msg.twist.twist.angular.z=self.angular
            self.odom_pub.publish(self.odom_msg)
            
            self.tf.header.stamp=rospy.Time.now()
            self.tf.transform.translation.x=self.x
            self.tf.transform.translation.y=self.y
            self.tf.transform.rotation.x=q[0]
            self.tf.transform.rotation.y=q[1]
            self.tf.transform.rotation.z=q[2]
            self.tf.transform.rotation.w=q[3]
            
            self.tf_pub.sendTransform(self.tf)
            # rospy.loginfo("self.left_angle: %d",self.left_angle)
            # rospy.loginfo("left_angle_diff: %d",left_angle_diff)
            # rospy.loginfo("right_angle_diff: %d",right_angle_diff)
            # rospy.loginfo("self.ds: %d",self.ds)
            # rospy.loginfo("self.d_right: %d",d_right)
            # rospy.loginfo("self.right_angle: %d",self.right_angle)
            # rospy.loginfo("self.right_wheel_prev_pos: %d",self.right_wheel_prev_pos)
            # rospy.loginfo("dt: %d",dt)
            # rospy.loginfo("-----------------------------    -------------")
        else:
            rospy.loginfo("Having error in dt")
        
if __name__== '__main__':
    rospy.init_node("tf_to_diff",anonymous=True)
    rospy.loginfo("TfDiff is Running")
    difftf=DiffTf()
    difftf.spin()
    