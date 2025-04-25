#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float64MultiArray, Int32
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import numpy as np
from scipy.optimize import least_squares

## 调试信息输出
# 输出调试信息
def meow(str):
    rospy.loginfo(str)
    # with open("/home/kiwi/SmartCar/smart-car/debug.txt", "w") as fout:
    with open("debug.txt", "w") as fout:
        fout.write(str)

# 输出测试点的坐标def save_data_to_txt(points, measurements, file_path):
def save_data_to_txt(points, measurements, file_path):  
    with open(file_path, 'w') as f:
        f.write("Points and Measurements:\n")
        for point, measurement in zip(points, measurements):
            f.write(f"({point[0]}, {point[1]}): {measurement}\n")

## 辐射源位置估计
# 计算两个点之间的平方距离
def dist_sqr(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

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

class navigation_node2:
    def __init__(self):
        rospy.init_node('navigation_node')
        meow("navigation2.py starts")

        # 订阅唤醒信号
        self.awake_angle = -1  # 初始化唤醒角度
        self.awake_received = False  # 标志是否收到唤醒信号
        self.awake_sub = rospy.Subscriber('/mic/awake/angle', Int32, self.awake_callback)
        
        # 订阅辐射源强度
        self.sub = rospy.Subscriber('radiation2', Float64MultiArray, self.radiation_callback)
        meow("navigation2.py raidiation2 subscriber starts")
        self.pub = rospy.Publisher('points', Float64MultiArray)
        meow("navigation2.py points pubisher starts")
        self.ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        meow("navigation2.py action client")
        self.goal = MoveBaseGoal()
        meow("navigation2.py move base goal")

        self.key_points = 6
        self.measurements = []  # Initialize measurements with a default value
        while not self.ac.wait_for_server(rospy.Duration.from_sec(5.0)):
            rospy.loginfo("Waiting for the move_base action server to come up")

    def get_rad(self):
        self.x = np.linspace(0.0, 3, self.key_points)
        self.y = np.linspace(0.0, 3, self.key_points)
        self.points = np.array([[self.x[i], self.y[j]] for i in range(self.key_points) for j in range(self.key_points)])
        meow("Generated points array")
        # 保存点坐标到文件
        # save_data_to_txt(points, self.measurements, "points.txt")
        
        # 发送点坐标
        points_msg = Float64MultiArray()
        points_msg.data = self.points.flatten().tolist()
        self.pub.publish(points_msg)
        meow("navigation2.py points published")

        # 接受辐射源强度
        self.received_radiation = False
        meow("Received radiation intensity!!!!!")

    def get_radiation_sources(self):
        rospy.sleep(5)
        initial_params = initial_guess(self.points, self.measurements)
        save_data_to_txt(self.points, self.measurements, "points.txt")
        result = least_squares(
            residual, 
            initial_params, 
            args=(self.points, self.measurements),
            method='lm',  # Levenberg-Marquardt算法
            max_nfev=3000   # 最大迭代次数
        )
        self.x_rad_1, self.y_rad_1, k_rad_1, self.x_rad_2, self.y_rad_2, k_rad_2 = result.x
        
        # 通过暴力的方式将坐标转换为给定的象限
        self.x_rad_1 = abs(self.x_rad_1)
        self.y_rad_1 = -abs(self.y_rad_1)
        self.x_rad_2 = abs(self.x_rad_2)
        self.y_rad_2 = -abs(self.y_rad_2)

        # 将第1次的结果作为第2次下降的初始值
        initial_params = [self.x_rad_1, self.y_rad_1, k_rad_1, self.x_rad_2, self.y_rad_2, k_rad_2]
        result = least_squares(
            residual, 
            initial_params, 
            args=(self.points, self.measurements),
            method='lm',  # Levenberg-Marquardt算法
            max_nfev=8000   # 最大迭代次数
        )
        self.x_rad_1, self.y_rad_1, k_rad_1, self.x_rad_2, self.y_rad_2, k_rad_2 = result.x
        # 通过暴力的方式将坐标转换为给定的象限
        self.x_rad_1 = abs(self.x_rad_1)
        self.y_rad_1 = -abs(self.y_rad_1)
        self.x_rad_2 = abs(self.x_rad_2)
        self.y_rad_2 = -abs(self.y_rad_2)
        meow(f"Calculated radiation sources: {self.x_rad_1:.2f} {self.y_rad_1:.2f} {self.x_rad_2:.2f} {self.y_rad_2:.2f}")

    def run(self):
        meow("navigation2.py run")
        self.goal.target_pose.header.frame_id = "map"
        self.goal.target_pose.header.stamp = rospy.Time.now()
        self.goal.target_pose.pose.position.z = 0.0
        self.goal.target_pose.pose.orientation.x = 0.0
        self.goal.target_pose.pose.orientation.y = 0.0
        self.goal.target_pose.pose.orientation.z = 0.0
        self.goal.target_pose.pose.orientation.w = 1.0
        meow("navigation2.py move base goal init")

        # 根据距离原点的距离排序辐射源
        dist1 = dist_sqr(self.x_rad_1, self.y_rad_1, 0, 0)
        dist2 = dist_sqr(self.x_rad_2, self.y_rad_2, 0, 0)
        if dist1 > dist2:
            self.x_rad_1, self.x_rad_2 = self.x_rad_2, self.x_rad_1
            self.y_rad_1, self.y_rad_2 = self.y_rad_2, self.y_rad_1

        # 输出辐射源的坐标
        with open("rad_info.txt", "w") as fout:
            fout.write(f"第一个辐射源坐标（较近）：{self.x_rad_1:.2f} {self.y_rad_1:.2f}\n")
            fout.write(f"第二个辐射源坐标（较远）：{self.x_rad_2:.2f} {self.y_rad_2:.2f}\n")

        # 移动到辐射源1的位置
        self.goal.target_pose.pose.position.x = self.x_rad_1
        self.goal.target_pose.pose.position.y = self.y_rad_1
        self.goal.target_pose.pose.orientation.x = 0.0
        self.goal.target_pose.pose.orientation.y = 0.0
        self.goal.target_pose.pose.orientation.z = 0.7071
        self.goal.target_pose.pose.orientation.w = 0.7071
        rospy.loginfo(f"meow {self.x_rad_1:.2f} {self.y_rad_1:.2f}")
        self.ac.send_goal(self.goal)
        self.ac.wait_for_result()
        meow("navigation2.py move to first radiation source")

        # 移动到辐射源2的位置
        self.goal.target_pose.pose.position.x = self.x_rad_2
        self.goal.target_pose.pose.position.y = self.y_rad_2
        self.goal.target_pose.pose.orientation.x = 0.0
        self.goal.target_pose.pose.orientation.y = 0.0
        self.goal.target_pose.pose.orientation.z = 0.7071
        self.goal.target_pose.pose.orientation.w = 0.7071
        rospy.loginfo(f"meow {self.x_rad_2:.2f} {self.y_rad_2:.2f}")
        self.ac.send_goal(self.goal)
        self.ac.wait_for_result()
        meow("navigation2.py move to second radiation source")

        # 移动到家的位置
        self.goal.target_pose.pose.position.x = 0.0
        self.goal.target_pose.pose.position.y = 0.0
        self.goal.target_pose.pose.orientation.x = 0.0
        self.goal.target_pose.pose.orientation.y = 0.0
        self.goal.target_pose.pose.orientation.z = 0.0
        self.goal.target_pose.pose.orientation.w = 1.0
        rospy.loginfo(f"meow {0.0:.2f} {0.0:.2f}")
        self.ac.send_goal(self.goal)
        self.ac.wait_for_result()
        meow("navigation2.py move to home")

        meow("navigation2.py end")

    def wait_for_call(self):
        meow("navigation2.py begins waiting for call")
        rospy.sleep(5) # 
        meow("Wake-up signal received, starting navigation...")

    def radiation_callback(self, msg):
        self.received_radiation = True
        meow("navigation2.py Received radiation intensity")
        self.measurements = msg.data
        meow(f"Received radiation intensity: {self.measurements}")

    def awake_callback(self, msg):
        """处理唤醒信号的回调函数"""
        self.awake_angle = msg.data
        self.awake_received = True
        meow(f"Received wake-up signal with angle: {self.awake_angle}")

if __name__ == '__main__':
    try:
        navigation_node = navigation_node2()
        navigation_node.get_rad()
        navigation_node.get_radiation_sources()
        navigation_node.wait_for_call()
        navigation_node.run()
    except rospy.ROSInterruptException:
        pass
