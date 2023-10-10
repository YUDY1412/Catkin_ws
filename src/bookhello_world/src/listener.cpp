#include<ros/ros.h>
#include<std_msgs/String.h>
#include<iostream>

void callbackfunc(const std_msgs::String:: ConstPtr& msg)
{
 ROS_INFO("i heard [%s]",msg->data.c_str());



}

int main(int agrc, char **agrv)
{
    ros::init(agrc,agrv,"listener");
    ros::NodeHandle nh;
    ros::Subscriber sub = nh.subscribe("chatter",1000,callbackfunc);
    ros::spin();
return 0;
}

