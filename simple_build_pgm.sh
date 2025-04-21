# 将当前目录位置添加到环境变量中
# cd ~/SmartCar/smart-car
# source devel/setup.bash
# 编译
catkin_make
# 运行
gnome-terminal -- bash -c "echo '运行smart-car'; roslaunch build_pgm build_pgm.launch; exec bash"  
gnome-terminal -- bash -c "echo '查看ROS话题'; rostopic list; exec bash"  # 查看ROS话题
gnome-terminal -- bash -c "echo '查看激光雷达数据'; rostopic echo /scan; exec bash"  # 查看激光雷达数据
# rosrun map_server map_saver -f ~/map  # 保存地图
# xdg-open ~/map.pgm    # 打开地图