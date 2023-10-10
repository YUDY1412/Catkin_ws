#include <ros/ros.h>
#include <std_msgs/String.h>
void msgcallback(const std_msgs::String::ConstPtr& msg )
{
    ROS_INFO("nEW MESsege receive is: %s",msg->data.c_str());
    
}
 int main(int argc, char **argv)
{
    ros::init(argc,argv,"simple_subcriber_cpp");
    ros::NodeHandle n;
    ros::Subscriber sub;
    sub = n.subscribe("hello", 10, msgcallback);
    ros::spin();
    return 0;
}


