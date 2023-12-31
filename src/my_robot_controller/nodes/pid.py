#!/usr/bin/env python3

"""
   twist_to_motors - converts a twist message to motor commands.  Needed for navigation stack
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
    def __init__(self):
#############################################################
        rospy.init_node("twist_to_motors")
        nodename = rospy.get_name()
        rospy.loginfo("%s started" % nodename)

        rospy.on_shutdown(self.shutdown_cb)
        self.wheelradius=0.033
        self.wheel_separation=0.092
        self.left_speed = Int32()
        self.right_speed = Int32()
        
        self.pub_joint=rospy.Publisher("jointstate",JointState,queue_size=2)
        self.pub_lmotor = rospy.Publisher('set_left_speed', Int32,queue_size=1)
        self.pub_rmotor = rospy.Publisher('set_right_speed', Int32,queue_size=1)
        self.reset = rospy.Publisher('reset', Bool,queue_size=1)
        self.cmd_sub=rospy.Subscriber('/cmd_vel', Twist, self.twistCallback)
        self.left_tick_sub=rospy.Subscriber("left_ticks",Int32,self.left_callback) 
        self.right_tick_sub=rospy.Subscriber("right_ticks",Int32,self.right_callback) 
    
        self.rate = rospy.get_param("~rate", 50)
        # self.timeout_ticks = rospy.get_param("~timeout_ticks", 2)
        self.left = 0
        self.right = 0
        self.kp=1
        self.kd=1
        self.ki=1
        self.encoder_max=  2147483648
        self.encoder_min= -2147483648
        self.encoder_low_wrap =(self.encoder_max - self.encoder_min) * 0.3 + self.encoder_min
        self.encoder_high_wrap = (self.encoder_max - self.encoder_min) * 0.7 + self.encoder_min 
        self.lmult=0
        self.rmult=0 
        self.right_goal=0
        self.left_goal=0
        self.integ_rprev=0
        self.error_rprev=0
        self.integ_lprev=0
        self.error_lprev=0
        self.right_angle_prev=0
        self.left_angle_prev=0
        self.right_wheel_prev_pos=0
        self.left_wheel_prev_pos=0
        self.Time_Prev=rospy.Time.now()
        self.dt =0.00001
        
################################################################
    def shutdown_cb(self):
        rospy.logwarn("Resetting board")
        self.pub_lmotor.publish(0)
        self.pub_rmotor.publish(0)
        self.reset.publish(0)
        pass
 
################################################################
    
    def spin(self):   
        r = rospy.Rate(self.rate)
        idle = rospy.Rate(10)
        then = rospy.Time.now()
        # self.ticks_since_target = self.timeout_ticks
    
        ###### main loop  ######
        while not rospy.is_shutdown():
        
            while not rospy.is_shutdown():
                self.spinOnce()
                r.sleep()
            idle.sleep()
                
    #############################################################
    def spinOnce(self):
        
        self.velocity()
        self.pid_right()
        self.pid_left()
        # self.ticks_since_target += 1

#################################################################
    def twistCallback(self,msg):
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
        
        # rospy.loginfo(msg.data)
################################################################            
    def right_callback(self,msg):
        enc = msg.data
        if(enc < self.encoder_low_wrap and self.prev_rencoder > self.encoder_high_wrap):
            self.rmult = self.rmult + 1
        
        if(enc > self.encoder_high_wrap and self.prev_rencoder < self.encoder_low_wrap):
            self.rmult = self.rmult - 1
            
        self.right = 1.0 * (enc + self.rmult * (self.encoder_max - self.encoder_min))

        self.prev_rencoder = enc

        # rospy.loginfo(msg.data)   
###############################################################current velocity 
    def velocity(self):
            self.right_angle= self.right * 2 * 3.14/20
            self.left_angle=  self.left  * 2 * 3.14/20  
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
        integ_now = self.integ_rprev + (self.dt * (error_now + self.error_rprev) / 2)
        pwr = self.kp * error_now + self.ki * integ_now + (self.kd * (error_now - self.error_rprev) / self.dt) 

        if pwr >255:
            pwr=255
        elif pwr <-255:
            pwr=-255
            
        self.right_speed.data=int(pwr)
        self.pub_rmotor.publish(self.right_speed)
        
          # rospy.loginfo("right")      
        self.integr_rprev = integ_now
        self.errorr_rprev = error_now

################################################################         
    def pid_left(self):
        error_now=self.left_goal - self.left
        integ_now = self.integ_lprev + (self.dt * (error_now + self.error_lprev) / 2)
        pwr = self.kp * error_now + self.ki * integ_now + (self.kd * (error_now - self.error_lprev) / self.dt) 
        
        if pwr >255:
            pwr=255
        elif pwr <-255:
            pwr=-255
            
        self.left_speed.data=int(pwr)
        self.pub_lmotor.publish(self.left_speed) 
        
        # rospy.loginfo("left")
        self.integr_lprev = integ_now
        self.errorr_lprev = error_now
################################################################ 
if __name__ == '__main__':
    """ main """
    twistToMotors = TwistToMotors()
    twistToMotors.spin()