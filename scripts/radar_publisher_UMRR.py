#!/usr/bin/env python
#coding:utf-8

import rospy
import os
import socket
import time
from std_msgs.msg import String
from data_fusion_shenzhen.msg import radarmsg

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.settimeout(60)
host = "192.168.1.2"
port = 4001
server.bind((host, port))
MaxBytes=1024*1024

server.listen(1)
######################
client,addr = server.accept()
print(addr,"The device is connected")
cont = 0
rospy.init_node('radar_publicer', anonymous = True)
pub = rospy.Publisher('radar_1', radarmsg, queue_size = 10)
rate = rospy.Rate(20)
while not rospy.is_shutdown():
    data = client.recv(MaxBytes)
    if not data:
        print('data is empty, closing...')
        break
    localTime = time.asctime( time.localtime(time.time()))
    # print(localTime,' Bytes:',len(data))
    if data[0] == "\xff":
        if len(data) > 40 and ord(data[40]) != 0:
            msg = radarmsg()
            publish_data = []
            for num in range(ord(data[40])):
                if len(data) > (41+11*(num+1)) and ord(data[(40+11*num+2)]) == (16+num):
                    string_data = String()
                    str_data = str()
                    for tem_j in range(8):
                        str_data = str_data + "{:08b}".format(ord(data[(40+11*num+4+tem_j)]))
                    string_data.data = str_data
                    publish_data.append(string_data)
            msg.data = publish_data
            pub.publish(publish_data)
            print("%s cars are detected by radar!" % ord(data[40]))
            rate.sleep()
        else:
            msg = radarmsg()
            publish_data = []
            string_data = String()
            string_data.data = "null"
            publish_data.append(string_data)
            msg = publish_data
            pub.publish(msg)
            print("no cars are detected!")
            rate.sleep()

# try:
#     pass


# except BaseException as e:
#     print("Error")
#     print(repr(e))
# finally:
#     server.close()
#     print("server is closed!")

