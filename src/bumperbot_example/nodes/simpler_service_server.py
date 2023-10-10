#!/usr/bin/env python3

import rospy
from bumperbot_example.srv import AddTwoInts,AddTwoIntsResponse

def servicefunction(req):
    rospy.loginfo("Ready to sum 2 ints %d and %d",req.a,req.b)
    return AddTwoIntsResponse(req.a+req.b)
    

if __name__=='__main__':
    rospy.init_node('simple_service_node',anonymous=True)
    service =rospy.Service('add_two_ints',AddTwoInts,servicefunction)
    rospy.loginfo("this service is ready to serve")
    rospy.spin()