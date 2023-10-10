#ifndef TURTLESIM_KINEMATICS_H
#define TURTLESIM_KINEMATICS_H
#include <ros/ros.h>
#include <turtlesim/Pose.h>
class Turtlesim_Kinematics
{
public:
    Turtlesim_Kinematics();
    ros::NodeHandle nh;
    ros::Subscriber turtle1_pose_sub;
    ros::Subscriber turtle2_pose_sub;
    turtlesim::Pose turtle1_last_pose;
    turtlesim::Pose turtle2_last_pose;
    void turtle1callback(const turtlesim::Pose &pose);
    void turtle2callback(const turtlesim::Pose &pose);
};

#endif