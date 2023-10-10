#!usr/bin/env python3
import rospy
from bumperbot_controller.noise_controller import NoiseController
 
if __name__ == '__main__':
    rospy.init_node('noise_controller')
    
    wheel_radius =rospy.get_param('~wheel_radius')
    wheel_separation =rospy.get_param('~wheel_separation')
    controller=NoiseController(wheel_radius,wheel_separation)
    
    rospy.spin()
    