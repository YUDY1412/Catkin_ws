#include "bumperbot_example/turtlesim_kinematics.h"

int main(int argc,char ** argv)
{
    ros::init(argc,argv,"turtlesim_kinematics_node");
    Turtlesim_Kinematics turtle_kinematics;
    ros::spin();
    return 0;
}