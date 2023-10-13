#!/usr/bin/env python3

"""
   twist_to_motors - converts a twist message to motor commands.  Needed for navigation stack
   
   
    Copyright (C) 2012 Jon Stephan. 
     
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import rospy
from std_msgs.msg import Float32, Int32, Bool
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import JointState

#Mapping -1 - 1 to -255 to 255
from numpy import interp
#############################################################
#############################################################
class TwistToMotors():
#############################################################
#############################################################

    #############################################################
    def __init__(self):
    #############################################################
        rospy.init_node("twist_to_motors")
        nodename = rospy.get_name()
        rospy.loginfo("%s started" % nodename)

        rospy.on_shutdown(self.shutdown_cb)
        self.wheelradius=0.033
        self.wheel_separation=0.092

        self.sign = lambda a: (a>0) - (a<0)

        self.left_speed = Int32()
        self.right_speed = Int32()

        self.w = rospy.get_param("~base_width", 0.125)
        self.fixed_speed = rospy.get_param("~fixed_speed", 255)
        self.pub_joint=rospy.Publisher("jointstate",JointState,queue_size=2)
        self.pub_lmotor = rospy.Publisher('set_left_speed', Int32,queue_size=1)
        self.pub_rmotor = rospy.Publisher('set_right_speed', Int32,queue_size=1)

        self.reset = rospy.Publisher('reset', Bool,queue_size=1)
        rospy.Subscriber('/cmd_vel', Twist, self.twistCallback)
        self.left_tick_sub=rospy.Subscriber("left_ticks",Int32,self.left_callback) 
        self.right_tick_sub=rospy.Subscriber("right_ticks",Int32,self.right_callback) 
    
    
        self.rate = rospy.get_param("~rate", 50)
        self.timeout_ticks = rospy.get_param("~timeout_ticks", 2)
        self.left = 0
        self.right = 0
        self.kp=1
        self.kd=1
        self.ki=1
    def shutdown_cb(self):
        rospy.logwarn("Resetting board")
        self.pub_lmotor.publish(0)
        self.pub_rmotor.publish(0)

        self.reset.publish(0)


        pass

    #############################################################
    def spin(self):
    #############################################################
    
        r = rospy.Rate(self.rate)
        idle = rospy.Rate(10)
        then = rospy.Time.now()
        self.ticks_since_target = self.timeout_ticks
    
        ###### main loop  ######
        while not rospy.is_shutdown():
        
            while not rospy.is_shutdown() and self.ticks_since_target < self.timeout_ticks:
                self.spinOnce()
                r.sleep()
            idle.sleep()
                
    #############################################################
    def spinOnce(self):
    #############################################################
        # dx = (l + r) / 2
        # dr = (r - l) / w
    #############################################################
        # self.right = 1.0 * self.dx + self.dr
        # self.left = 1.0 * self.dx - self.dr
               
        # self.left_mapped = interp(self.left,(-2,2),(-1,1))*self.fixed_speed
        # self.right_mapped = interp(self.right,(-2,2),(-1,1))*self.fixed_speed

        # self.left_speed.data = int(self.left_mapped)
        # self.right_speed.data =int(self.right_mapped)

        # rospy.loginfo(self.left_speed)
        # rospy.loginfo(self.right_speed)

        # self.pub_lmotor.publish(self.left_speed)
        # self.pub_rmotor.publish(self.right_speed)
        self.pid_right()
        self.pid_left()
        self.ticks_since_target += 1

    #############################################################
    def twistCallback(self,msg):
    #############################################################
        # rospy.loginfo("-D- twistCallback: %s" % str(msg))
        self.ticks_since_target = 0
        self.dx = msg.linear.x
        self.dr = msg.angular.z
        self.dy = msg.linear.y
        self.right_goal=(self.dx+self.wheel_separation*self.dr)/self.wheelradius
        self.left_goal=(self.dx-self.wheel_separation*self.dr)/self.wheelradius
#################################################################
    def left_callback(self,msg):
        enc=msg.data
        if (enc < self.encoder_low_wrap and self.prev_lencoder > self.encoder_high_wrap):
            self.lmult = self.lmult + 1
            
        if (enc > self.encoder_high_wrap and self.prev_lencoder < self.encoder_low_wrap):
            self.lmult = self.lmult - 1
            
        self.left = 1.0 * (enc + self.lmult * (self.encoder_max - self.encoder_min)) 
        self.prev_lencoder = enc
        
        rospy.loginfo(msg.data)
################################################################            
    def right_callback(self,msg):
        enc = msg.data
        if(enc < self.encoder_low_wrap and self.prev_rencoder > self.encoder_high_wrap):
            self.rmult = self.rmult + 1
        
        if(enc > self.encoder_high_wrap and self.prev_rencoder < self.encoder_low_wrap):
            self.rmult = self.rmult - 1
            
        self.right = 1.0 * (enc + self.rmult * (self.encoder_max - self.encoder_min))

        self.prev_rencoder = enc

        rospy.loginfo(msg.data)   
###############################################################current velocity 
    def velocity(self):
            self.right_angle= self.right * 2 * 3.14/20
            self.left_angle=  self.left  * 2 * 3.14/20
            right_angle_diff=self.right_angle-self.right_angle_prev
            left_angle_diff=self.left_angle-self.left_angle_prev
            
            self.dt= (rospy.Time.now() - self.Time_Prev).to_sec()
            
            self.right_angle_prev=self.right_angle
            self.left_angle_prev=self.left_angle
            self.Time_Prev=rospy.Time.now()
            
            d_right=(self.right_angle-self.right_wheel_prev_pos)/self.dt
            d_left=(self.left_angle -self.left_wheel_prev_pos)/self.dt
            
            self.left_wheel_prev_pos=self.left_angle
            self.right_wheel_prev_pos =self.right_angle
            
            self.linear=self.wheelradius*(d_right + d_left)/2
            self.angular=self.wheelradius*(d_right - d_left)/(2*self.wheel_separation)
################################################################   PID   
                            
    def pid_right(self):
        error_now=self.right_goal - self.right
        integ_now = integ_prev + (self.dt * (error_now + error_prev) / 2)
        pwr = self.kp * error_now + self.ki * integ_now + (self.kd * (error_now - error_prev) / self.dt) 
        integ_prev = integ_now
        error_prev = error_now
        self.pub_rmotor.publish(pwr)
        
    def pid_left(self):
        error_now=self.left_goal - self.left
        integ_now = integ_prev + (self.dt * (error_now + error_prev) / 2)
        pwr = self.kp * error_now + self.ki * integ_now + (self.kd * (error_now - error_prev) / self.dt) 
        integ_prev = integ_now
        error_prev = error_now
        self.pub_lmotor.publish(pwr)

if __name__ == '__main__':
    """ main """
    twistToMotors = TwistToMotors()
    twistToMotors.spin()