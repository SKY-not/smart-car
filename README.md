# smart-car

- This is a project to develop smart car.
- This project mainly consists of two parts：
  - Solving for radiation sources
  - Navigation


## 关于DWA
[DWA参数调整详细介绍](https://www.bilibili.com/video/BV1Gp421R7hx/?spm_id_from=333.337.search-card.all.click&vd_source=e16234f501c80e845b428ec57d0f8c05)
### 调整参数具体方法
- 手动调整参数 使用rqt_reconfigure工具 不断调整参数直到效果达到预期
- 自动调整参数 使用rosbag数据进行训练 训练出模型 然后使用模型进行参数调整（AIGC）


## 关于TEB
[TEB参数调整详细介绍]()

## Cheat Sheet

在file文件夹中放了一些可以看的资料，供参考用

如果你不想在bashrc中修改文件，不妨在每次开始前执行添加工作空间的指令，这样可能会更加稳定？

```shell
  source devel/setup.bash
```

ROS 中如何创建新的功能包

```shell
  cd ~/catkin_ws/src
  catkin_create_pkg beginner_tutorials std_msgs rospy roscpp
  catkin_make
```

动态调整参数
```shell
 rosrun rqt_reconfigure rqt_reconfigure
 ```
