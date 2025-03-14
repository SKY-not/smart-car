catkin_make
gnome-terminal -e "roslaunch gazebo_nav dwa_race_demo_singlepath.launch"
gnome-terminal -e "rosrun radiation_pub radiation_pub"
gnome-terminal -e "rosrun simple_navigation_goals simple_navigation_goals"