#!/usr/bin/env python3
#coding=utf-8

import rospy
from std_msgs.msg import String

if __name__ == '__main__':
    # 初始化节点
    rospy.init_node("python_publisher_node")
    # 发送警告日志，表明节点开始正常运行
    rospy.logwarn("python_publisher_node is run")
    # 创建话题发布者对象
    publisher = rospy.Publisher("python_topic", String, queue_size=10)
    # 创建控制话题发布的频率的对象
    rate = rospy.Rate(2)

    while not rospy.is_shutdown():
        # 循环条件：节点没有被关闭
        # 发送消息日志，表明节点还在运行
        rospy.loginfo("python_publisher_node still running")
        # 创建消息
        message = String()
        message.data = "python_publisher_node send a message"
        # 发送消息
        publisher.publish(message)
        # 控制频率
        rate.sleep()