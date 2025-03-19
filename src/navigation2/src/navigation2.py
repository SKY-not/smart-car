#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float64MultiArray
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import numpy as np
from scipy.optimize import least_squares

## 调试信息输出
# 输出调试信息
def meow(str):
    rospy.loginfo(str)
    with open("/home/kiwi/SmartCar/smart-car/debug.txt", "w") as fout:
        fout.write(str)

# 输出测试点的坐标def save_data_to_txt(points, measurements, file_path):
def save_data_to_txt(points, measurements, file_path):  
    with open(file_path, 'w') as f:
        # 写入points数据
        f.write("Points:\n")
        for point in points:
            f.write(f"({point[0]}, {point[1]})\n")
        
        # 写入measurements数据
        f.write("\nMeasurements:\n")
        for measurement in measurements:
            f.write(f"{measurement}\n")

# 定义残差函数
def residual(params, points, measurements, epsilon=1e-6):
    x1, y1, k1, x2, y2, k2 = params
    predicted = []
    for (x, y) in points:
        # 计算辐射源贡献
        dist_sq1 = (x - x1)**2 + (y - y1)**2 + epsilon
        dist_sq2 = (x - x2)**2 + (y - y2)**2 + epsilon
        I_pred = k1 / dist_sq1 + k2 / dist_sq2
        predicted.append(I_pred)
    return np.array(predicted) - np.array(measurements)

# 初始化猜测（需合理策略，见下文）
def initial_guess(points, measurements):
    # 假设第一个辐射源靠近最大测量值点
    max_idx = np.argmax(measurements)
    x_guess1, y_guess1 = points[max_idx]
    k_guess1 = measurements[max_idx]
    
    # 对第一个辐射源的位置进行一定程度的平移得到第二个辐射源的位置
    x_guess2, y_guess2 = x_guess1 + 0.5, y_guess1 + 0.5
    k_guess2 = measurements[max_idx]
    return [x_guess1, y_guess1, k_guess1, x_guess2, y_guess2, k_guess2]


def dist_sqr(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

class navigation_node2:
    key_points = 30
    id = 0
    rad = [0.0] * key_points
    x_rad_1, y_rad_1 = 0.0, 0.0
    x_rad_2, y_rad_2 = 0.0, 0.0
    x = np.linspace(0.0, 3.6, key_points)
    y = np.zeros_like(x)
    x_real = [0.0] * key_points
    y_real = [0.0] * key_points
    flag = [False] * key_points

    def get_rad_xy(self):
        #global x_rad, y_rad, rad , x_real, y_real
        points = [(self.x_real[i], self.y_real[i]) for i in range(self.key_points)]
        measurements = [self.rad[i] for i in range(self.key_points)]
        initial_params = initial_guess(points, measurements)
        result = least_squares(
            residual, 
            initial_params, 
            args=(points, measurements),
            method='lm',  # Levenberg-Marquardt算法
            max_nfev=3000   # 最大迭代次数
        )
        self.x_rad_1, self.y_rad_1, k_rad_1, self.x_rad_2, self.y_rad_2, k_rad_2 = result.x
        save_data_to_txt(points, measurements, "/home/kiwi/SmartCar/smart-car/data_output.txt")

        # 通过暴力的方式将坐标转换为给定的象限
        self.x_rad_1 = abs(self.x_rad_1)
        self.y_rad_1 = abs(self.y_rad_1)
        self.x_rad_2 = abs(self.x_rad_2)
        self.y_rad_2 = abs(self.y_rad_2)

        # 获取辐射强度信息
    def radiation_sub(self, msg):
        # global id, rad, x_real, y_real, flag
        if not self.flag[self.id]:
            self.rad[self.id] = msg.data[0]
            self.x_real[self.id] = msg.data[1]
            self.y_real[self.id] = msg.data[2]

    def __init__(self):
        rospy.init_node('navigation_node')
        meow("navigation2.py start")
        self.sub = rospy.Subscriber('radiation', Float64MultiArray, self.radiation_sub)
        meow("navigation2.py subscribe radiation")
        self.ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        meow("navigation2.py action client")
        self.goal = MoveBaseGoal()
        meow("navigation2.py move base goal")

        while not self.ac.wait_for_server(rospy.Duration.from_sec(5.0)):
            rospy.loginfo("Waiting for the move_base action server to come up")
        
        self.goal.target_pose.header.frame_id = "map"
        self.goal.target_pose.header.stamp = rospy.Time.now()
        self.goal.target_pose.pose.position.z = 0.0
        self.goal.target_pose.pose.orientation.x = 0.0
        self.goal.target_pose.pose.orientation.y = 0.0
        self.goal.target_pose.pose.orientation.z = 0.0
        self.goal.target_pose.pose.orientation.w = 1.0
        meow("navigation2.py move base goal init")

        for i in range(self.key_points):
            rospy.loginfo("%d?", i)
            self.goal.target_pose.pose.position.x = self.x[i]
            self.goal.target_pose.pose.position.y = self.y[i]
            self.ac.send_goal(self.goal)
            self.ac.wait_for_result()
            self.id = i
            msg = rospy.wait_for_message('radiation', Float64MultiArray, timeout=None)
            meow("navigation2.py waits for radiation, try running radiation_sub")
            self.radiation_sub(msg)
            meow("navigation2.py runs radiation_sub successfully")
            rospy.loginfo("%d!", i)

        meow("try 2 cacl radiation source")
        self.get_rad_xy()
        meow("navigation2.py get radiation source")

        # 输出辐射源的坐标
        with open("/home/kiwi/SmartCar/smart-car/rad_info.txt", "w") as fout:
            fout.write(f"第一个辐射源坐标：{self.x_rad_1} {self.y_rad_1}\n")
            fout.write(f"第二个辐射源坐标：{self.x_rad_2} {self.y_rad_2}\n")
            fout.write("from navigation1.py")

        self.target_pose.pose.position.x = self.x_rad
        self.target_pose.pose.position.y = self.y_rad
        rospy.loginfo(f"meow {self.x_rad} {self.y_rad}")
        self.ac.send_goal(self.goal)
        self.ac.wait_for_result()

if __name__ == '__main__':
    try:
        navigation_node2()
    except rospy.ROSInterruptException:
        pass
