cd ~/SmartCar/smart-car
source devel/setup.bash
catkin_make
gnome-terminal -e "roslaunch gazebo_nav dwa_race_demo_singlepath.launch"
gnome-terminal -e "rosrun radiation_pub2 radiation_pub2"
gnome-terminal -e "rosrun simple_navigation_goals2 simple_navigation_goals2"
