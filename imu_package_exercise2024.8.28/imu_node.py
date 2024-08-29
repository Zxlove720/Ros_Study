#!/usr/bin/env python3
#coding=utf-8

import rospy
# 数学模块提供pi的值，便于弧度转角度
import math
from sensor_msgs.msg import Imu
# 导入tf工具，可以将看不懂的四元数转换成欧拉角，方便转换为角度
from tf.transformations import euler_from_quaternion
# euler是欧拉，quaternion是四元数

def imu_callback(message):
    # orientation是方向、方位   convariance是协方差
    if message.orientation_covariance[0] < 0:
        # 检查IMU消息的方向协方差，如果小于0则无意义，那么直接返回
        return
    quaternion = [
        # 提取四元数
        message.orientation.x,
        message.orientation.y,
        message.orientation.z,
        message.orientation.w
    ]
    # 用方法将四元数转换为欧拉角（弧度）
    (roll, pitch, yaw) = euler_from_quaternion(quaternion)
    # 弧度转换成角度
    roll = roll * 180 / math.pi
    pitch = pitch * 180 / math.pi
    yaw = yaw * 180 / math.pi
    rospy.loginfo("滚转=%.2f   俯仰=%.2f   朝向=%.2f" % (roll, pitch, yaw))


if __name__ == '__main__':
    rospy.init_node("imu_node")
    rospy.logwarn("imu_node start running")
    imu_subscriber = rospy.Subscriber("/imu/data", Imu, imu_callback, queue_size=10)
    rospy.spin()