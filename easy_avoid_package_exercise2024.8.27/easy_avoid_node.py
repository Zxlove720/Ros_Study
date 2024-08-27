#!/usr/bin/env python3
# coding=utf-8

import rospy
from sensor_msgs.msg import LaserScan
# 传感器消息类型 LaserScan翻译为激光扫描
from geometry_msgs.msg import Twist


# 几何消息类型 geometry翻译为几何 Twist翻译为转动、扭转


def LidarCallback(message):
    # 声明全局变量，用来发送速度的消息，控制消息
    global velocity_publisher
    # count变量用来控制避障时，机器人转向的时间
    global count
    # 得到机器人正前方的障碍物距离，并输出
    distance = message.ranges[180]
    rospy.loginfo("距离前方障碍物还有%.2fm", distance)

    # 此刻是避障调整代码执行，只调整角度，调整完了直接推出函数，不会发布速度，所以说是静止调整好了角度再运行的
    if count > 0:
        count = count - 1
        return
    # 创建速度控制的消息
    velocity_command = Twist()
    # 如果距离前方障碍物距离小于1.5m，则给count赋值为35，激光雷达的扫描频率大概是11hz，相当于角度调整了3.5s左右
    # 调整的是旋转的角度以避开障碍，0.3rad/s
    if distance < 1.5:
        velocity_command.angular.z = 0.3
        count = 35
    # 如果没有到达避障的位置，则正常的向前方以0.15m/s的速度直行
    else:
        velocity_command.linear.x = 0.15
    # 不管是调整还是正常直行，都需要发布速度给机器人，来控制速度
    velocity_publisher.publish(velocity_command)


if __name__ == '__main__':
    # 初始化ros节点并发出警告，表明节点开始运行
    rospy.init_node("easy_avoid_node")
    rospy.logwarn("easy_avoid_node start running")
    # 创建激光雷达的订阅者对象
    lidar_subscriber = rospy.Subscriber("/scan", LaserScan, LidarCallback, queue_size=10)
    # 创建速度发布者对象
    count = 0
    velocity_publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    # 控制节点，一直运行
    rospy.spin()



