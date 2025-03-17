cd ~/SmartCar/smart-car
source devel/setup.bash
catkin_make
gnome-terminal -e "roslaunch gazebo_nav dwa_race_demo_singlepath.launch"
gnome-terminal -e "rosrun radiation_pub radiation_pub"
chmod +x $(rospack find navigation)/src/navigation.py
chmod +x $(rospack find navigation)/src/navigation2.py
gnome-terminal -e "rosrun navigation navigation2.py"
