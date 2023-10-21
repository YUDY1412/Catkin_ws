20/11 : done with connecting buster-1 to Laptop with dead-reckoning (simu version) with a little bit change in twist_to_motors

BLUETOOTH:
    sudo rfcomm connect /dev/rfcomm0 98:D3:41:F6:6D:FC
    sudo chmod 666 /dev/rfcomm0
    rosrun rosserial_python serial_node.py _port:=/dev/rfcomm0 _baud:=9600