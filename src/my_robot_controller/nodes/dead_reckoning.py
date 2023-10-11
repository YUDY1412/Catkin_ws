#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped,Twist
from nav_msgs.msg import Odometry
import tf_conversions 
import math
from math import radians, degrees

class D_r(object):
    def __init__(self):
        self.pose_goal_sub=rospy.Subscriber("/move_base_simple/goal",PoseStamped,self.goalcallback)
        self.pose_current_sub=rospy.Subscriber("/my_robot_controller/odom",Odometry,self.odomcallback)
        self.cmd_vel_pub=rospy.Publisher("/my_robot_controller/cmd_vel",Twist,queue_size=1)
        self.cur_x=0
        self.cur_y=0
        self.cur_angle=0
        self.goal_x=0
        self.goal_y=0
        self.goal_angle =0
        self.tulp=0.2
        self.tuln=-0.2
        self.delta_angle=0.5
        self.distance_delta =0.1
        self.stop_vel=0
        self.check=0
        
    def odomcallback(self,msg):
        self.cur_x=msg.pose.pose.position.x
        self.cur_y=msg.pose.pose.position.y
        msg.pose.pose.orientation.x
        q = tf_conversions.transformations.euler_from_quaternion([msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w])
        self.cur_angle = degrees(q[2]) 
        #rospy.loginfo("self.cur_angle: %d",self.cur_angle)   
    
    def goalcallback(self,msg):
        self.goal_x = msg.pose.position.x
        self.goal_y =msg.pose.position.y
        q = tf_conversions.transformations.euler_from_quaternion([msg.pose.orientation.x,msg.pose.orientation.y,msg.pose.orientation.z,msg.pose.orientation.w])
        self.goal_angle = degrees(math.atan2(self.goal_y-self.cur_y , self.goal_x-self.cur_x))-self.cur_angle
        rospy.loginfo("hello")
        self.check=0
        
    def excute(self):
        self.angle_diff = self.cur_angle - self.goal_angle  
        while (abs(self.goal_angle)>self.delta_angle):
            self.goal_angle = degrees(math.atan2(self.goal_y-self.cur_y , self.goal_x-self.cur_x))-self.cur_angle
            rospy.loginfo("goal_angle: %d",self.goal_angle)
            rospy.loginfo("rotating")
            cur_diff_angle=abs(self.goal_angle)

            if (degrees(math.atan2(self.goal_y-self.cur_y , self.goal_x-self.cur_x))>0):
                self.tul=self.tulp
            else:
                self.tul=self.tuln
            self.check=2
            self.rotate(self.tul)
            
          #  rospy.loginfo(self.tul)
        ######################################################################
        rospy.loginfo("Robot moving to the goal point")
        
        distance = math.hypot(self.goal_x - self.cur_x, self.goal_y - self.cur_y)
        rospy.loginfo("Robot moving to the goal point [%f]" % (distance))
        rospy.loginfo(self.check)
        while distance > self.distance_delta :
            if(self.check==3):
                break
            distance = math.hypot(self.goal_x - self.cur_x, self.goal_y - self.cur_y)
            self.linear(0.2)
            # if (distance >2):
            #     rospy.logwarn("robot went outside the goal")
            #     break 
            rospy.loginfo("distance: %d",distance)
            self.check=1
            
        rospy.loginfo("STOPPPPPPPPP")
        if self.check==1 or self.check ==2:
            self.check=3
        self.linear(self.stop_vel)
        rospy.sleep(2)       
            
    def spin(self):
        while not rospy.is_shutdown():
            self.excute()
    
    def linear(self,speed):
        twist = Twist()
        twist.linear.x = speed
        twist.linear.y = 0
        twist.linear.z = 0

        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0

        self.cmd_vel_pub.publish(twist)
    def rotate(self,speed):
        twist = Twist()
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0

        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = speed
        self.cmd_vel_pub.publish(twist)
        
if __name__=='__main__':
    rospy.init_node("dead_reckoning")
    dr=D_r()
    dr.spin()
    