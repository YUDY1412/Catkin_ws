#!usr/bin/env python3
import rospy
from bumperbot_example.srv import AddTwoInts
import sys

if __name__== '__main__':
    if len(sys.argv) == 3:
        a=int(sys.argv[1])
        b=int(sys.argv[2])
        print("Requesting....",a,b)
        rospy.wait_for_service('add_two_ints')
        add_two_ints= rospy.ServiceProxy('add_two_ints', AddTwoInts)
        response=add_two_ints(a,b)
        print("Service response",response)
    else:
        print("Request two argument")
        sys.exit(-1)
        