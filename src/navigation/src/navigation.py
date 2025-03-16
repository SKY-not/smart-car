#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from std_msgs.msg import Float64MultiArray
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import numpy as np
from scipy.optimize import least_squares

key_points = 3
id = 0
rad = [0.0] * key_points
x_rad, y_rad = 0.0, 0.0
x = [1, 3, 5]
y = [0, 0, 0]
x_real = [0.0] * key_points
y_real = [0.0] * key_points
flag = [False] * key_points

def radiation_sub(msg_s):
    global id, rad, x_real, y_real, flag
    if not flag[id]:
        rad[id] = msg_s.data[0]
        x_real[id] = msg_s.data[1]
        y_real[id] = msg_s.data[2]

def dist_sqr(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

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

#'''
def get_rad_xy():
    global x_rad, y_rad, rad, x_real, y_real
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
                x_rad = i_val
                y_rad = j_val
#'''
'''
def get_rad_xy():
    global x_rad, y_rad, rad, x_real, y_real
    points = [(x_real[i], y_real[i]) for i in range(key_points)]
    measurements = [rad[i] for i in range(key_points)]
    initial_params = initial_guess(points, measurements)
    result = least_squares(
        residual, 
        initial_params, 
        args=(points, measurements),
        method='lm',  # Levenberg-Marquardt算法
        max_nfev=1000   # 最大迭代次数
    )
    x_rad, y_rad, k_rad = result.x
'''
# 输出调试信息
def meow(str):
    with open("/home/kiwi/SmartCar/smart-car/debug.txt", "w") as fout:
        fout.write(str)


def main():
    global id, x_rad, y_rad
    rospy.init_node('simple_navigation_goals')
    meow("navigation.py started")
    sub = rospy.Subscriber('radiation', Float64MultiArray, radiation_sub)
    meow("subscribed to radiation")
    ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    meow("created action client")
    goal = MoveBaseGoal()
    meow("created goal")

    while not ac.wait_for_server(rospy.Duration(5.0)):
        rospy.loginfo("Waiting for the move_base action server to come up")

    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.z = 0.0
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.0
    goal.target_pose.pose.orientation.w = 1.0
    meow("set goal")

    for i in range(key_points):
        rospy.loginfo("%d?", i)
        goal.target_pose.pose.position.x = x[i]
        goal.target_pose.pose.position.y = y[i]
        ac.send_goal(goal)
        meow("sent goal")
        ac.wait_for_result()
        meow("finished goal")
        id = i
        rospy.spin()
        rospy.loginfo("%d!", i)

    get_rad_xy()

    # 输出辐射源位置
    '''
    with open("/home/kiwi/SmartCar/smart-car/rad_info.txt", "w") as fout:
        fout.write(f"{x_rad} {y_rad}\n")
    '''

    with open("/home/kiwi/SmartCar/smart-car/rad_info.txt", "w") as fout:
        fout.write(f"{x_rad} {y_rad}\n")
        fout.write("from navigation.py")

    goal.target_pose.pose.position.x = x_rad
    goal.target_pose.pose.position.y = y_rad
    rospy.loginfo(f"meow {x_rad} {y_rad}")
    ac.send_goal(goal)
    ac.wait_for_result()

if __name__ == '__main__':
    main()
