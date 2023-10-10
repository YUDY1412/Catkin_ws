#include<ros/ros.h>
#include<std_msgs/String.h>
#include<sstream>
int main(int argc, char **argv)
{
ros::init(argc,argv,"simple_publisher_cpp");
ros::NodeHandle nh;
ros::Publisher pub =nh.advertise<std_msgs::String>("chatter",10);
ros::Rate rate(10);
int counter =0;
while (ros::ok())
{
    std_msgs::String msg;
    std::stringstream ss;
    ss<< "Hello world from C++"<<counter;
    msg.data=ss.str();
    ROS_INFO(msg.data.c_str());
    pub.publish(msg);
    ros::spinOnce();
    rate.sleep();
    counter ++;
}


return 0;
}