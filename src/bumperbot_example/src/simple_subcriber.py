#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def msgcallback(msg):
    rospy.loginfo("New messege receive %s",msg.data)
    
    

if __name__== '__main__':
    rospy.init_node('simple_subcriber',anonymous=True)
    pub=rospy.Subscriber("hello",String,callback=msgcallback)
    rospy.spin()