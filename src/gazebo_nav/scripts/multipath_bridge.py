#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import glob
from collections import deque
import time
import csv
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped

SAVESPACE = os.path.join("/home", "ucar", "Documents", "GazeboResult")
WORKSPACE = os.path.dirname(__file__)
TESTFILEPATH = os.path.join(SAVESPACE, time.strftime("%Y%m%d%H%M.csv"))

class Bridge(object):
    startFlag = False
    goals = deque()
    
    def __init__(self):
        rospy.init_node("bridge")
        csvfiles = glob.glob(os.path.join(WORKSPACE, "*.csv"))
        if len(csvfiles) > 0:
            with open(csvfiles[0], 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.goals.append(list())
                    for cell in row:
                        self.goals[-1].append(eval(cell))
        self.client = actionlib.SimpleActionClient("real_base", MoveBaseAction)
        self.server = actionlib.SimpleActionServer("move_base", MoveBaseAction, execute_cb=self.callback)
        rospy.Subscriber("/move_base_simple/goal", PoseStamped, callback=self.simpleCallback)
        self.publisher = rospy.Publisher("/real_base_simple/goal", PoseStamped, queue_size=5)
        self.client.wait_for_server()
        rospy.logwarn("Finish init!")
        while not self.startFlag:
            pass
        while len(self.goals) != 0:
            self.send_goal(self.goals.popleft())
            self.client.wait_for_result()
        rospy.spin()
    

    def callback(self, goal):
        self.goals.append([goal.target_pose.pose.position.x, goal.target_pose.pose.position.y, goal.target_pose.pose.orientation.z, goal.target_pose.pose.orientation.w])
        self.startFlag = True
        rospy.logwarn("Catch goal!")
        
    def send_goal(self, goal):
        pos_x, pos_y, ori_z, ori_w = goal
        newGoal = MoveBaseGoal()
        newGoal.target_pose.header.frame_id = "map"
        newGoal.target_pose.pose.position.x = pos_x
        newGoal.target_pose.pose.position.y = pos_y
        newGoal.target_pose.pose.position.z = 0.0
        newGoal.target_pose.pose.orientation.x = 0.0
        newGoal.target_pose.pose.orientation.y = 0.0
        newGoal.target_pose.pose.orientation.z = ori_z
        newGoal.target_pose.pose.orientation.w = ori_w
        self.client.send_goal(newGoal)
        
    def simpleCallback(self, pose):
        rospy.logwarn("Catch simple goal!")
        newPose = PoseStamped()
        newPose.header.frame_id = "map"
        pos_x = pose.pose.position.x
        newPose.pose.position.x = pos_x
        pos_y = pose.pose.position.y
        newPose.pose.position.y = pos_y
        newPose.pose.position.z = pose.pose.position.z
        newPose.pose.orientation.x = pose.pose.orientation.x
        newPose.pose.orientation.y = pose.pose.orientation.y
        ori_z = pose.pose.orientation.z
        newPose.pose.orientation.z = ori_z
        ori_w = pose.pose.orientation.w
        newPose.pose.orientation.w = ori_w
        result = [pos_x, pos_y, ori_z, ori_w]
        rospy.loginfo(str(result))
        with open(TESTFILEPATH, "a") as f:
            writer = csv.writer(f)
            writer.writerow(result)
        self.publisher.publish(newPose)

if __name__ == "__main__":
    if not os.path.exists(SAVESPACE):
        os.makedirs(SAVESPACE)
    b = Bridge()