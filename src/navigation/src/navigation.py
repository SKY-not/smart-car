#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from std_msgs.msg import Float64MultiArray
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

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

def main():
    global id, x_rad, y_rad
    rospy.init_node('simple_navigation_goals')
    sub = rospy.Subscriber('radiation', Float64MultiArray, radiation_sub)
    ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    goal = MoveBaseGoal()

    while not ac.wait_for_server(rospy.Duration(5.0)):
        rospy.loginfo("Waiting for the move_base action server to come up")

    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.z = 0.0
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.0
    goal.target_pose.pose.orientation.w = 1.0

    for i in range(key_points):
        rospy.loginfo("%d?", i)
        goal.target_pose.pose.position.x = x[i]
        goal.target_pose.pose.position.y = y[i]
        ac.send_goal(goal)
        ac.wait_for_result()
        id = i
        rospy.spin_once()
        rospy.loginfo("%d!", i)

    get_rad_xy()

    with open("/home/ucar/ucar_ws/rad_info.txt", "w") as fout:
        fout.write(f"{x_rad} {y_rad}\n")

    goal.target_pose.pose.position.x = x_rad
    goal.target_pose.pose.position.y = y_rad
    rospy.loginfo(f"meow {x_rad} {y_rad}")
    ac.send_goal(goal)
    ac.wait_for_result()

if __name__ == '__main__':
    main()
