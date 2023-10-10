#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
if __name__== '__main__':
	rospy.init_node('simple_publisher',anonymous=True)
	pub=rospy.Publisher("hello",String,queue_size=10)
	r=rospy.Rate(10)
	counter=0
	while not rospy.is_shutdown():
		hello_msg="hello world %d " % counter
		pub.publish(hello_msg)
		r.sleep()
		counter+=1
		  
