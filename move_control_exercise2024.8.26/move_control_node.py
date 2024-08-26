#!/usr/bin/env python3
# coding=utf-8

import rospy
import math
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Imu

count = 0


def ImuCallback(message):
    global velocity_publisher
    if message.orientation_covariance[0] < 0:
        return
    quaternion = [
        message.orientation.x,
        message.orientation.y,
        message.orientation.z,
        message.orientation.w
    ]
    (roll, pitch, yaw) = euler_from_quaternion(quaternion)
    roll = roll * 180 / math.pi
    pitch = pitch * 180 / math.pi
    yaw = yaw * 180 / math.pi
    rospy.loginfo("滚转=%.2f   俯仰=%.2f   朝向=%.2f" % (roll, pitch, yaw))
    # 航向锁定
    target_yaw = 90
    difference = target_yaw - yaw
    velocity_command = Twist()
    velocity_command.angular.z = difference * 0.05
    velocity_command.linear.x = 0.15
    velocity_publisher.publish(velocity_command)


def MoveCallback(message):
    global velocity_publisher
    global count
    distance = message.ranges[180]
    rospy.loginfo("距离前方障碍物还有%.2fm", distance)

    if count > 0:
        count = count - 1
        return
    velocity_command = Twist()
    if distance < 1.5:
        count = 35
        velocity_command.angular.z = 0.3
    else:
        velocity_command.linear.x = 0.15
    velocity_publisher.publish(velocity_command)


if __name__ == '__main__':
    rospy.init_node("move_control_node")
    rospy.logwarn("move_control_node start running")

    imu_subscriber = rospy.Subscriber("/imu/data", Imu, ImuCallback, queue_size=10)
    lidar_subscriber = rospy.Subscriber("/scan", LaserScan, MoveCallback, queue_size=10)
    velocity_publisher = rospy.Publisher("cmd_vel", Twist, queue_size=10)

    rospy.spin()