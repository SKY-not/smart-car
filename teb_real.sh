# 将当前目录位置添加到环境变量中
cd ~/SmartCar/smart-car
source devel/setup.bash
# 编译
catkin_make
# 运行
# gnome-terminal -e "roslaunch nav teb_race_demo_singlepath.launch"
gnome-terminal -e "roslaunch nav teb_real.launch"
sleep 5
gnome-terminal -e "rosrun radiation_pub2 radiation_pub2"
sleep 5
gnome-terminal -e "roslaunch ucar_controller base_driver.launch"
sleep 5
gnome-terminal -e "roslaunch ydlidar ydlidar.launch"
sleep 5
gnome-terminal -e "roslaunch xf_mic_asr_offline xf_mic_asr_offline.launch"
sleep 5
chmod +x $(rospack find navigation2)/src/navigation2.py
gnome-terminal -e "rosrun navigation2 navigation2.py"