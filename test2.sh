cd ~/SmartCar/smart-car
source devel/setup.bash
catkin_make
gnome-terminal -e "roslaunch gazebo_nav dwa_race_demo_singlepath.launch"
gnome-terminal -e "rosrun radiation_pub2 radiation_pub2"
chmod +x $(rospack find navigation2)/src/navigation2.py
gnome-terminal -e "rosrun navigation2 navigation2.py"
