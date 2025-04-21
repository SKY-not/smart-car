#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob

import numpy as np
import cv2

from tools.yolo import YOLO

if __name__ == "__main__":
    yolo = YOLO()

    '''
    1、如果想要进行检测完的图片的保存，利用r_image.save("img.jpg")即可保存，直接在predict.py里进行修改即可。 
    2、如果想要获得预测框的坐标，可以进入yolo.detect_image函数，在绘图部分读取top，left，bottom，right这四个值。
    3、如果想要利用预测框截取下目标，可以进入yolo.detect_image函数，在绘图部分利用获取到的top，left，bottom，right这四个值
    在原图上利用矩阵的方式进行截取。
    4、如果想要在预测图上写额外的字，比如检测到的特定目标的数量，可以进入yolo.detect_image函数，在绘图部分对predicted_class进行判断，
    比如判断if predicted_class == 'car': 即可判断当前目标是否为车，然后记录数量即可。利用draw.text即可写字。
    '''
    frame_dir = os.path.join(os.path.dirname(__file__), "yolo_test_frames")
    if os.path.exists(frame_dir):
        for frame_path in glob.glob(os.path.join(frame_dir, "*.jpg")):
            try:
                image = cv2.imread(frame_path)
            except:
                print('Open Error! Path: {:s}'.format(frame_path))
                continue
            else:
                result, r_image = yolo.detect_image(image)
                frame = cv2.cvtColor(np.asarray(r_image), cv2.COLOR_RGB2BGR)
                cv2.imshow("yolo test", frame)
                cv2.waitKey(500)
    else:
        print('Open Error! Path: {:s}'.format(frame_dir))
    cv2.destroyAllWindows()
        
