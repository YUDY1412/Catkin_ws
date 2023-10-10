cmake_minimum_required(VERSION 3.0.2)
project(bumperbot_example)


find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  turtlesim
  geometry_msgs
  tf2_ros
  message_generation
)

catkin_python_setup()

add_service_files(
  FILES
  AddTwoInts.srv
  GetTransform.srv
)

generate_messages(
DEPENDENCIES
std_msgs
geometry_msgs
)

catkin_package(
  INCLUDE_DIRS include
 CATKIN_DEPENDS
 turtlesim
 geometry_msgs
tf2_ros
)

include_directories(
include
  ${catkin_INCLUDE_DIRS}
)


catkin_install_python(PROGRAMS
src/simple_publisher.py
src/simple_subcriber.py
nodes/turtlesim_kinematics_node.py
nodes/tf_example_node.py
nodes/simple_timer.py
nodes/simpler_service_server.py
nodes/simple_service_client.py
DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})  

add_library(turtlesim_kinematics src/turtlesim_kinematics.cpp )
add_dependencies(turtlesim_kinematics ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(turtlesim_kinematics ${catkin_LIBRARIES})

add_executable(simple_cpp_publisher src/simple_publisher_cpp.cpp)
target_link_libraries(simple_cpp_publisher ${catkin_LIBRARIES})

add_executable(simple_cpp_subcriber src/simple_subcriber_cpp.cpp)
target_link_libraries(simple_cpp_subcriber ${catkin_LIBRARIES})

add_executable(simple_cpp_publisher1 nodes/simple_publisher.cpp )
target_link_libraries(simple_cpp_publisher1 ${catkin_LIBRARIES})

add_executable(turtlesim_kinematics_node 
    nodes/turtlesim_kinematics_node.cpp
    src/turtlesim_kinematics.cpp
)
add_dependencies(turtlesim_kinematics_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
target_link_libraries(turtlesim_kinematics_node turtlesim_kinematics ${catkin_LIBRARIES})