#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import glob
import numpy as np
import cv2
import PIL
from PIL import ImageDraw, ImageFont
import pyzbar.pyzbar as pyzbar
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge

class QrcodeDetector:
    detectResult = None

    def __init__(self, app):
        #创立节点
        rospy.init_node('qrcode_node', anonymous=True) 
        
        #订阅usb_cam发出的图像消息，接收到消息后进入回调函数callback()
        rospy.Subscriber('usb_cam/image_raw', Image, self.callback)
        
        self.resultPub = rospy.Publisher("qrcode_result", String, queue_size=5)
        rospy.loginfo(str(app))
        self.app = app
        
        #等待
        rospy.spin()   
        
    def callback(self, data):
        #通过cvBridge将ROS中图片的格式转换为Opencv中的格式
        bridge = CvBridge()
        frame = bridge.imgmsg_to_cv2(data, "bgr8")
        
        #轴对称翻转照片，否则二维码是镜像的
        frame = cv2.flip(frame,1)

        #将图像转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        barcodes = pyzbar.decode(gray)
        
        #如果检测到二维码，输出其编号
        if len(barcodes) > 0:
            resultFrame, resultData, resultType = self.processResult(frame, barcodes)
            self.resultPub.publish(str([resultData, resultType]))
            if self.app:
                self.detectResult = resultFrame
        
        if self.app:
            if self.detectResult is None:
                appFrame = frame.copy()
            else:
                width = frame.shape[1]
                appFrame = np.zeros((frame.shape[0], 2 * width, frame.shape[2]), np.uint8)
                appFrame[:, width:, :] = self.detectResult
                appFrame[:, :width, :] = frame
            cv2.imshow("frame", appFrame)
            
            #关闭程序
            key = cv2.waitKey(1)
            
    def processResult(self, frame, barcodes):
        resultFrame = frame.copy()
        resultData = list()
        resultType = list()
        if self.app:
            font = ImageFont.truetype(glob.glob(os.path.join(os.path.dirname(__file__), "*.ttf"))[0], 25)
        print()
        for barcode in barcodes:
            barcodeType = barcode.type
            
            # 条形码数据为字节对象，所以如果我们想在输出图像上画出来，就需要先将它转换成字符串
            barcodeData = barcode.data.decode("utf-8")
            
            resultType.append(barcodeType)
            resultData.append(barcodeData)
            outputText = resultType[-1] + ", " + resultData[-1]
            rospy.loginfo(outputText)
            if self.app:
                # 提取条形码的边界框的位置
                (x, y, w, h) = barcode.rect
                
                # 画出图像中条形码的边界框
                cv2.rectangle(resultFrame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                
                # opencv不支持中文，使用PIL
                framePIL = PIL.Image.fromarray(cv2.cvtColor(resultFrame, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(framePIL)
                draw.text((x, y-10), outputText, font=font, fill=(255, 0, 0))
                
                # 转换回opencv格式
                resultFrame = cv2.cvtColor(np.asarray(framePIL), cv2.COLOR_RGB2BGR)
        return resultFrame, resultData, resultType
                                         
 
if __name__ == '__main__':
    ad = QrcodeDetector(rospy.get_param("qrcode_app", default=False))
