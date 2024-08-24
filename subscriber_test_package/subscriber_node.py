#!/usr/bin/env python3
#coding=utf-8

import rospy
from std_msgs.msg import String

def callback1(message):
    rospy.loginfo(message)

def callback2(message):
    rospy.logwarn(message)

if __name__ == '__main__':
    rospy.init_node("python_subscriber_node")
    subscribe1 = rospy.Subscriber("python_topic", String, callback1, queue_size=10)
    subscribe2 = rospy.Subscriber("python2_topic", String, callback2, queue_size=10)

    rospy.spin()