cd ~/SmartCar/smart-car
source devel/setup.bash
catkin_make
gnome-terminal -e "roslaunch nav teb_race_demo_singlepath.launch"
# gnome-terminal -e "rosrun radiation_pub radiation_pub"
gnome-terminal -e "rosrun rqt_reconfigure rqt_reconfigure"
# gnome-terminal -e "rosrun simple_navigation_goals simple_navigation_goals"`