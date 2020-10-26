#!/usr/bin/env python
#coding:utf-8

import rospy
from data_fusion_shenzhen.msg import radarmsg

def callback(data):
    if data.data[0].data == "null":
        print("no cars are detected!")
    else:
        for len_i in range(len(data.data)):
            v_id = int(data.data[0].data[0:6], 2)
            v_len = (int(data.data[0].data[6:14], 2) - 0) * 0.2 # m
            v_Vy = (int(data.data[0].data[14:25], 2) - 1024) * 100 # km/h
            v_Vx = (int(data.data[0].data[25:36], 2) - 1024) * 100 # km/h
            v_Y = (int(data.data[0].data[36:50], 2) - 8192) * 64 # m
            v_X = (int(data.data[0].data[50:64], 2) - 8192) * 64 # m
            print("ID:%s, len:%s, X:%s, Y:%s, Vx:%s, Vy:%s" % (v_id, v_len, v_X, v_Y, v_Vx, v_Vy))

def listener():
    rospy.init_node('radar_listener',anonymous = True)
    rospy.Subscriber('radar_1', radarmsg, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()