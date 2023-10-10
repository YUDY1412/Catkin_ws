execute_process(COMMAND "/home/d20/catkin_ws/build/bumperbot_example/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/d20/catkin_ws/build/bumperbot_example/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
