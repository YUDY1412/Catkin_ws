#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def talker():
    rospy.init_node('talker',anonymous=True)
    pub=rospy.Publisher('chatter',String,queue_size=10)
    rate=rospy.Rate(10)
    
    while not rospy.is_shutdown():
        hello_str="hello World %s" % rospy.get_time()
        pub.publish(hello_str)
        rospy.loginfo(hello_str)
        rate.sleep()
        
if __name__=="__main__":
    try:
        talker()
    except rospy.ROSInternalException:
        pass    
    