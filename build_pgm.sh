# 将当前目录位置添加到环境变量中
cd ~/SmartCar/smart-car
source devel/setup.bash
# 编译
catkin_make
# 运行
gnome-terminal -- bash -c "echo '启动激光雷达'; roslaunch ydlidar lidar_view.launch; exec bash"  # 启动激光雷达
gnome-terminal -- bash -c "echo '启动小车控制'; roslaunch ucar_controller base_driver.launch; exec bash"  # 启动底盘
gnome-terminal -- bash -c "echo '启动gmapping建图'; rosrun gmapping slam_gmapping scan:=/scan cmd_vel:=/cmd_vel; exec bash" # 启动gmapping建图
gnome-terminal -- bash -c "echo '查看ROS话题'; rostopic list; exec bash"  # 查看ROS话题
gnome-terminal -- bash -c "echo '查看激光雷达数据'; rostopic echo /scan; exec bash"  # 查看激光雷达数据
# rosrun map_server map_saver -f ~/map  # 保存地图
# xdg-open ~/map.pgm    # 打开地图
