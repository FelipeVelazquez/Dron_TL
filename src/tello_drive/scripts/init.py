#!/usr/bin/env python

#################################################
#												
#  This program init the tello dron 		
#                 		&						
# get the data of sensor and turn on ROS data	
#												
#	Author: L. Felipe Velazquez					
#												
#################################################

import socket
import rospy
from std_msgs.msg import String

host = ''
port = 9000
locaddr = (host,port) 

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ('192.168.10.1', 8889)

sock.bind(locaddr)


# Used to encode the msgs and sent to tello & return a answer
def encoder(msg):
	msg = msg
	msg = msg.encode() 
	sent = sock.sendto(msg, tello_address)
	info, st = sock.recvfrom(1024)
	print("Replay of " + str(msg) + ":" + info.decode())
	r = info.decode()
	return r

def init_tello():
    pub = rospy.Publisher('Init_state_tello', String, queue_size=10)
    rospy.init_node('init', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    replay = encoder('command')
    encoder('streamon')
    while not rospy.is_shutdown():
        r_str = "Dron state " + str(replay) 
        rospy.loginfo(r_str)
        pub.publish(r_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        init_tello()
    except rospy.ROSInterruptException:
    	encoder('streamoff')
        pass