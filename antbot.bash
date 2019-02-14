source /opt/ros/kinetic/setup.bash
source /home/ros1/catkin_ws/devel/setup.sh
echo 123 | sudo -S ip route add 172.17.191.0/24 via 172.17.128.1
export ROS_MASTER_URI=http://hal:11311/
export ROS_IP=172.17.191.23

