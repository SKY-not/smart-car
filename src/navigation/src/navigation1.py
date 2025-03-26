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
    x1, y1, k1 = params
    predicted = []
    for (x, y) in points:
        # 计算辐射源贡献
        dist_sq1 = (x - x1)**2 + (y - y1)**2 + epsilon
        I_pred = k1 / dist_sq1
        predicted.append(I_pred)
    return np.array(predicted) - np.array(measurements)

# 初始化猜测（需合理策略，见下文）
def initial_guess(points, measurements):
    # 假设第一个辐射源靠近最大测量值点
    max_idx = np.argmax(measurements)
    x_guess1, y_guess1 = points[max_idx]
    k_guess1 = measurements[max_idx]
    
    return [x_guess1, y_guess1, k_guess1]


def dist_sqr(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

class navigation_node:
    key_points = 10
    id = 0
    rad = [0.0] * key_points
    x_rad, y_rad = 0.0, 0.0
    x = np.linspace(0.0, 3.6, key_points)
    y = np.zeros_like(x)
    # y = np.tile([0.5, -0.5], key_points/2)
    x_real = [0.0] * key_points
    y_real = [0.0] * key_points
    flag = [False] * key_points


    def get_rad_xy(self):
        # global x_rad, y_rad, rad, x_real, y_real
        rad = self.rad
        x_real = self.x_real
        y_real = self.y_real
        ans = 100.0
        for i in range(0, 60):
            i_val = i * 0.1
            for j in range(-60, 0):
                j_val = j * 0.1
                t1 = (rad[2] - rad[0]) / (rad[1] - rad[0])
                t2 = (1 / dist_sqr(x_real[2], y_real[2], i_val, j_val) - 1 / dist_sqr(x_real[0], y_real[0], i_val, j_val)) / \
                    (1 / dist_sqr(x_real[1], y_real[1], i_val, j_val) - 1 / dist_sqr(x_real[0], y_real[0], i_val, j_val))
                if ans > abs(t1 - t2):
                    ans = abs(t1 - t2)
                    self.x_rad = i_val
                    self.y_rad = j_val


    def get_rad_xy2(self):
        #global x_rad, y_rad, rad , x_real, y_real
        points = [(self.x_real[i], self.y_real[i]) for i in range(self.key_points)]
        measurements = [self.rad[i] for i in range(self.key_points)]
        initial_params = initial_guess(points, measurements)
        result = least_squares(
            residual, 
            initial_params, 
            args=(points, measurements),
            method='lm',  # Levenberg-Marquardt算法
            max_nfev=2000   # 最大迭代次数
        )
        self.x_rad, self.y_rad, k_rad = result.x
        save_data_to_txt(points, measurements, "/home/kiwi/SmartCar/smart-car/data_output.txt")

        # 通过暴力的方式将坐标转换为给定的象限
        self.x_rad = abs(self.x_rad)
        self.y_rad = -abs(self.y_rad)

        # 获取辐射强度信息
    def radiation_sub(self, msg):
        # global id, rad, x_real, y_real, flag
        if not self.flag[self.id]:
            self.rad[self.id] = msg.data[0]
            self.x_real[self.id] = msg.data[1]
            self.y_real[self.id] = msg.data[2]

    def __init__(self):
        rospy.init_node('navigation_node')
        meow("navigation1.py start")
        self.sub = rospy.Subscriber('radiation', Float64MultiArray, self.radiation_sub)
        meow("navigation1.py subscribe radiation")
        self.ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        meow("navigation1.py action client")
        self.goal = MoveBaseGoal()
        meow("navigation1.py move base goal")

        while not self.ac.wait_for_server(rospy.Duration.from_sec(5.0)):
            rospy.loginfo("Waiting for the move_base action server to come up")
        
        self.goal.target_pose.header.frame_id = "map"
        self.goal.target_pose.header.stamp = rospy.Time.now()
        self.goal.target_pose.pose.position.z = 0.0
        self.goal.target_pose.pose.orientation.x = 0.0
        self.goal.target_pose.pose.orientation.y = 0.0
        self.goal.target_pose.pose.orientation.z = 0.0
        self.goal.target_pose.pose.orientation.w = 1.0
        meow("navigation1.py move base goal init")

        for i in range(self.key_points):
            rospy.loginfo("%d?", i)
            self.goal.target_pose.pose.position.x = self.x[i]
            self.goal.target_pose.pose.position.y = self.y[i]
            self.ac.send_goal(self.goal)
            self.ac.wait_for_result()
            self.id = i
            msg = rospy.wait_for_message('radiation', Float64MultiArray, timeout=None)
            meow("navigation1.py waits for radiation, try running radiation_sub")
            self.radiation_sub(msg)
            meow("navigation1.py runs radiation_sub successfully")
            #rospy.loginfo("has reached point %d %f %f ", i, x[i], y[i])
            rospy.loginfo("%d!", i)

        meow("try 2 cacl radiation source")
        #self.get_rad_xy()
        self.get_rad_xy2()
        meow("navigation1.py get radiation source")

        # 输出辐射源的坐标
        with open("/home/kiwi/SmartCar/smart-car/rad_info.txt", "w") as fout:
            fout.write(f"{self.x_rad} {self.y_rad}\n")
            fout.write("from navigation1.py")

        self.target_pose.pose.position.x = self.x_rad
        self.target_pose.pose.position.y = self.y_rad
        rospy.loginfo(f"meow {self.x_rad} {self.y_rad}")
        self.ac.send_goal(self.goal)
        self.ac.wait_for_result()

if __name__ == '__main__':
    try:
        navigation_node()
    except rospy.ROSInterruptException:
        pass
