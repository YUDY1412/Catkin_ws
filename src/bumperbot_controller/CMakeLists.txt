cmake_minimum_required(VERSION 3.0.2)
project(bumperbot_controller)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  geometry_msgs
  sensor_msgs
  nav_msgs
  tf2
  tf2_ros
)

catkin_python_setup() 

catkin_package(
  CATKIN_DEPENDS
  std_msgs
  geometry_msgs
  sensor_msgs
  nav_msgs
  tf2
  tf2_ros
)

 
include_directories(

  ${catkin_INCLUDE_DIRS}
)

 catkin_install_python(
  PROGRAMS
  nodes/simple_controller_node.py
  nodes/noise_controller_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
 ) 
 # INSTALL THE EXECUTABLE TO DEVEL FOLDER IN CATKIN_WS