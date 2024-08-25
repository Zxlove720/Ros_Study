#!/usr/bin/env python3
# coding=utf-8

import rospy
from geometry_msgs.msg import Twist

if __name__ == '__main__':
    # 初始化ros节点
    rospy.init_node("velocity_node")
    rospy.logwarn("velocity_node is run")
    # 获得publish对象
    velocity_publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    # 获得消息对象
    velocity_message = Twist()
    # 设置对应的速度
    velocity_message.linear.x = 0.5
    # 控制消息发送频率
    velocity_rate = rospy.Rate(30)
    while not rospy.is_shutdown():
        # 发送消息，控制速度
        velocity_publisher.publish(velocity_message)
        # 用rospy中的loginfo方法表明该节点仍然在运行
        rospy.loginfo("velocity_node is still running")
        # 控制频率
        velocity_rate.sleep()
