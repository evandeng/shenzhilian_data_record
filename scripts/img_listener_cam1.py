#!/usr/bin/env python
#coding:utf-8

import rospy
import cv2
import os
from sensor_msgs.msg import Image
from cv_bridge import CvBridge,CvBridgeError

camera_ip = "192.168.1.91"

def callback(data):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data,"bgr8")
    print(cv_image.shape)
    cv_image = cv2.resize(cv_image, (1280, 960))
    cv2.imshow("listener_"+camera_ip,cv_image)
    cv2.waitKey(50)

def listener():
# 参数为相机的ip
    rospy.init_node('img_listener',anonymous = True)
    rospy.Subscriber('camera_'+camera_ip, Image, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()