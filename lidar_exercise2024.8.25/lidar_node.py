#!/usr/bin/env python3
# coding=utf-8

import rospy
from sensor_msgs.msg import LaserScan


def LidarCallback(message):
    distance = message.ranges[180]
    rospy.loginfo("前方障碍物的距离是： %f", distance)


if __name__ == '__main__':
    rospy.init_node("lidar_node")
    rospy.logwarn("lidar_node start running")
    # 订阅消息
    lidar_subscriber = rospy.Subscriber("/scan", LaserScan, LidarCallback, queue_size=10)
    rospy.spin() #自旋
    # spin()的作用是让ROS节点进入一个循环，保持节点的运行状态，直到节点被手动关闭。
    # 具体来说，它会持续调用回调函数（如你的LidarCallback），处理订阅的消息和其他事件