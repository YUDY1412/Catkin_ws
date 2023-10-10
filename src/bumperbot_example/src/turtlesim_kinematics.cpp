#include "bumperbot_example/turtlesim_kinematics.h"

Turtlesim_Kinematics::Turtlesim_Kinematics()
{
    turtle1_pose_sub = nh.subscribe("/turtle1/pose", 1000, &Turtlesim_Kinematics::turtle1callback, this);
    turtle2_pose_sub = nh.subscribe("/turtle2/pose", 1000, &Turtlesim_Kinematics::turtle2callback, this);
}

void Turtlesim_Kinematics::turtle1callback(const turtlesim::Pose &pose)
{
    turtle1_last_pose = pose;
}
void Turtlesim_Kinematics::turtle2callback(const turtlesim::Pose &pose)
{
    turtle2_last_pose = pose;
    float Tx = turtle2_last_pose.x - turtle1_last_pose.x;
    float Ty = turtle2_last_pose.y - turtle1_last_pose.y;
    float theta_rad = turtle2_last_pose.theta - turtle1_last_pose.theta;
    float theta_deg = theta_rad * 180 / 3.14;
    ROS_INFO_STREAM("--------------\n"
                    << "Tx=" << Tx << "  Ty=" << Ty << "   theta_rad" << theta_rad << "  theta_deg" << theta_deg);
    ;
}