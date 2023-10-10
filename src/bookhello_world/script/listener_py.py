#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
def callbackfunc(data):
    rospy.loginfo("%s",data.data)

def listen():
    rospy.init_node("listener2",anonymous=True)
    sub=rospy.Subscribe("chatter",String,callbackfunc)
    rospy.spin()
    
if __name__=="__main__":
    listen()