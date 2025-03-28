cd ~/SmartCar/smart-car
source devel/setup.bash
catkin_make
gnome-terminal -e "roslaunch gazebo_nav dwa_race_demo_singlepath.launch"
gnome-terminal -e "rosrun rqt_reconfigure rqt_reconfigure"
