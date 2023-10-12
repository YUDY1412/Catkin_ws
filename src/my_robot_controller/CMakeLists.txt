cmake_minimum_required(VERSION 3.0.2)
project(my_robot_controller)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  turtlesim
  tf2
  std_msgs
  nav_msgs
  geometry_msgs

)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES my_robot_controller
 CATKIN_DEPENDS 
 tf2
 std_msgs
 nav_msgs
 geometry_msgs

#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)



catkin_install_python(
  PROGRAMS
  nodes/pid.py
  nodes/tf_to_diff.py
  nodes/twist_to_motors.py
  nodes/dead_reckoning.py
  nodes/controller.py
  nodes/teleop.py
  nodes/gazebo_odom.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
