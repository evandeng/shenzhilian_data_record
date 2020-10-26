#!/usr/bin/env python
#coding:utf-8

import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time


login_nm = "admin"
login_pwd = "hik12345"
camera_ip = "192.168.1.237"


def main():
    # init the ros node
    rospy.init_node('img_publicer', anonymous = True)
    pub = rospy.Publisher('camera_'+camera_ip, Image, queue_size = 10)
    rate = rospy.Rate(30)
    bridge = CvBridge()
     
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    print(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()))
    cap = cv2.VideoCapture("rtsp://" + login_nm + ":" + login_pwd + "@" + camera_ip + "/")

    #out = cv2.VideoWriter(dir_path + time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()) + str(camera.direction) + '.avi', fourcc, 20.0, (1280,720))  # (名字, 编解码器, 帧率, 分辨率)
    count = 0
    while cap.isOpened() and not rospy.is_shutdown():
        ret, frame = cap.read()
        count = count + 1
        if ret:
            # out.write(frame)
            # print(frame.shape)

            # cv2.namedWindow(camera_ip, flags=cv2.WINDOW_FREERATIO)
            # cv2.imshow(camera_ip, frame)
            # k = cv2.waitKey(1) & 0xFF
            frame = cv2.resize(frame, (1280, 720))
            pub.publish(bridge.cv2_to_imgmsg(frame,"bgr8"))
            rate.sleep()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # elif cv2.waitKey(1) & 0xFF == ord('s'):
                # cv2.imwrite(dir_path + str(camera.ip)+'.png', frame)

        else:
            break

    cap.release()
    # out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        print("Something's wrong. Please check codes.")
