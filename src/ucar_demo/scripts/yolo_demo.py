#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor

import numpy as np
import cv2

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from tools.yolo import YOLO

class YoloNode:
    pool = ThreadPoolExecutor()
    threadExecutor = None
    detectResult = None
    
    def __init__(self) -> None:
        #创立节点
        rospy.init_node('aruco_node', anonymous=True) 
        
        #订阅usb_cam发出的图像消息，接收到消息后进入回调函数callback()
        rospy.Subscriber('usb_cam/image_raw', Image, self.callback)
        
        #等待
        rospy.spin()
        
    def callback(self, data):
        #通过cvBridge将ROS中图片的格式转换为Opencv中的格式
        bridge = CvBridge()
        frame = bridge.imgmsg_to_cv2(data, "bgr8")
        
        #轴对称翻转照片，否则二维码是镜像的
        frame = cv2.flip(frame,1)
        
        if self.detectResult is None:
            appFrame = frame.copy()
        else:
            width = frame.shape[1]
            appFrame = np.zeros((frame.shape[0], 2 * width, frame.shape[2]), np.uint8)
            appFrame[:, width:, :] = self.detectResult
            appFrame[:, :width, :] = frame
        cv2.imshow("frame", appFrame)
        
        #图片显示时间为1ms
        key = cv2.waitKey(1)
        if key == ord('p'):
            if self.threadExecutor is None:
                self.threadExecutor = self.pool.submit(YoloNode.yoloDetector, (frame))
                # _, self.detectResult = YoloNode.yoloDetector(frame)
            elif self.threadExecutor.done():
                    _, resultFrame = self.threadExecutor.result()
                    self.detectResult = cv2.cvtColor(np.asarray(resultFrame), cv2.COLOR_RGB2BGR)
                    self.threadExecutor = self.pool.submit(YoloNode.yoloDetector, (frame))
        elif not (self.threadExecutor is None) and self.threadExecutor.done():
            _, resultFrame = self.threadExecutor.result()
            self.detectResult = cv2.cvtColor(np.asarray(resultFrame), cv2.COLOR_RGB2BGR)
    
    @staticmethod
    def yoloDetector(frame):
        y = YOLO()
        return y.detect_image(frame)

if __name__ == "__main__":
    yn = YoloNode()
        
