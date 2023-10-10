#!/usr/bin/env python3
import rospy
from tf2_ros import StaticTransformBroadcaster,TransformBroadcaster,TransformListener,Buffer
from geometry_msgs.msg import TransformStamped
from bumperbot_example.srv import GetTransform,GetTransformResponse
from tf.transformations import quaternion_from_euler,quaternion_multiply,quaternion_inverse
class TfExample(object):
    def __init__(self):
        self.static_broadcaster = StaticTransformBroadcaster()
        self.dynamic_broadcaster = TransformBroadcaster()
        
        self.static_transform_stamped = TransformStamped()
        self.dynamic_transform_stamped =TransformStamped()
        
        self.timer = rospy.Timer(rospy.Duration(0.1),self.timercallback)
        
        self.static_transform_stamped.header.stamp=rospy.Time.now()
        self.static_transform_stamped.header.frame_id="bumperbot_base"
        self.static_transform_stamped.child_frame_id="bumperbot_top"
        
        self.x_increment=0.05
        self.last_x=0
        self.rotation_counter=0
        self.last_orientation= quaternion_from_euler(0, 0, 0)
        self.orientation_increment=quaternion_from_euler(0, 0, 0.05)
        
        self.static_transform_stamped.transform.translation.x=0
        self.static_transform_stamped.transform.translation.y=0
        self.static_transform_stamped.transform.translation.z=0.3
        self.static_transform_stamped.transform.rotation.x =0
        self.static_transform_stamped.transform.rotation.y =0
        self.static_transform_stamped.transform.rotation.z =0
        self.static_transform_stamped.transform.rotation.w = 1 
        
        self.static_broadcaster.sendTransform(self.static_transform_stamped)
        rospy.loginfo("Publish static transform info between %s and %s",self.static_transform_stamped.header.frame_id,
                      self.static_transform_stamped.child_frame_id)     
        self.get_transform_service= rospy.Service("get_transfrom",GetTransform,self.gettransformcallback)
        self.tf_buffer= Buffer()
        self.tf_listener =TransformListener(self.tf_buffer)
        
    def timercallback(self,event):
        self.dynamic_transform_stamped.header.stamp=rospy.Time.now()
        self.dynamic_transform_stamped.header.frame_id="odom"
        self.dynamic_transform_stamped.child_frame_id="bumperbot_base"
        
        self.dynamic_transform_stamped.transform.translation.x= self.last_x + self.x_increment
        self.dynamic_transform_stamped.transform.translation.y =0
        self.dynamic_transform_stamped.transform.translation.z=0
        
        # self.dynamic_transform_stamped.transform.rotation.x=0
        # self.dynamic_transform_stamped.transform.rotation.y=0
        # self.dynamic_transform_stamped.transform.rotation.z=0
        # self.dynamic_transform_stamped.transform.rotation.w=1
        q=quaternion_multiply(self.last_orientation,self.orientation_increment)
        self.dynamic_transform_stamped.transform.rotation.x=q[0]
        self.dynamic_transform_stamped.transform.rotation.y=q[1]
        self.dynamic_transform_stamped.transform.rotation.z=q[2]
        self.dynamic_transform_stamped.transform.rotation.w=q[3]
        
        self.dynamic_broadcaster.sendTransform(self.dynamic_transform_stamped)
        self.last_x=self.dynamic_transform_stamped.transform.translation.x
        self.rotation_counter+=1
        self.last_orientation=q
        
        if self.rotation_counter >=100:
            self.orientation_increment=quaternion_inverse(self.orientation_increment)
            self.rotation_counter =0
            
    def gettransformcallback(self,req):
        rospy.loginfo("Request to get transform between %s and %s",req.frame_id ,req.child_frame_id )
        res=GetTransformResponse()
        request_transform=TransformStamped()
        try:
            request_transform= self.tf_buffer.lookup_transform(req.frame_id,req.child_frame_id,rospy.Time())
        except Exception as e:
            rospy.logerr("An error occur while transform %s and %s ",req.frame_id ,req.child_frame_id )
            res.succeed= False
            return res
        rospy.loginfo("The Request if : %s",request_transform)
        res.transform=request_transform
        res.succeed =True
        return res
        
        
            
            
        
        
