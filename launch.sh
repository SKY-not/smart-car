cd ~/SmartCar/smart-car
source devel/setup.bash
catkin_make
gnome-terminal -e "roslaunch nav teb_race_demo_singlepath.launch"
gnome-terminal -e "rosrun radiation_pub radiation_pub"
chmod +x $(rospack find navigation)/src/navigation1.py
gnome-terminal -e "rosrun navigation navigation1.py"