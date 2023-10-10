#include<ros/ros.h>
#include<std_msgs/String.h>
#include<sstream>

int main(int argc, char **argv)
{
    ros::init(argc,argv,"talker");
    ros::NodeHandle nh ;
    ros::Publisher pub= nh.advertise<std_msgs::String>("chatter",1000);
    ros::Rate rate(10) ;
    int count=0;
    while (ros::ok())
    {
        std::stringstream ss;
        std_msgs::String msg;
        ss<<"hello wotld" << count;
        msg.data=ss.str();
        ROS_INFO("%s",msg.data.c_str());
        pub.publish(msg);
        ros::spinOnce();
        rate.sleep();
        ++count;

    }
    return 0;

}