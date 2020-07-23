#!/usr/bin/env python

#################################################
#												#
#  		This program init the tello dron 		#
#                 		&						#
# get the data of sensor and turn on ROS data	#
#												#
#	Author: L. Felipe Velazquez					#
#												#
#################################################

import cv2
import socket
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


# Tello stream the video on local host
tello_video = cv2.VideoCapture('udp://@0.0.0.0:11111')

def talker():
    image_pub = rospy.Publisher("Tello_Video",Image,queue_size=10)
    rospy.init_node('video_tello', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        bridge = CvBridge()
        _, image = tello_video.read()
        ros_image = bridge.cv2_to_imgmsg(image, "bgr8")
        image_pub.publish(ros_image)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass