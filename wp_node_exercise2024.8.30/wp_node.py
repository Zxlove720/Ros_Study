#!/usr/bin/env python3
#coding = utf-8

import rospy
# 导入sys包，为了在结束导航之后调用exit方法退出程序
import sys
# 导入导航控制的消息类型——String
from std_msgs.msg import String

def navi_callback(message):
    # 声明全局变量target
    global target
    # 输出导航的结果
    rospy.logwarn("导航的结果是： %s", message.data)
    # 输出target的值，方便观察
    rospy.loginfo("target = %d", target)
    # 将target加一，代表当前目标变为下一个航点
    target = target + 1

if __name__ == '__main__':
    # 初始化rosnode
    rospy.init_node("wp_node")
    rospy.logwarn("wp_node start running")

    # 发布航点控制信息  话题是/waterplus/navi_waypoint
    navi_publisher = rospy.Publisher("/waterplus/navi_waypoint", String, queue_size=10)

    # 订阅导航结果      话题是/waterplus/navi_result
    result_subscriber = rospy.Subscriber("/waterplus/navi_result", String, navi_callback, queue_size=10)

    # 多个航点的导航
    target = 1 # 设置初始目标点为航点1
    while not rospy.is_shutdown():
        # 假设有四个航点，当目标大于第四个航点，则说明所有航点都已经到达，则退出程序
        if target > 4:
            sys.exit()
        rospy.sleep(1)
        # 设置目标航点的消息
        navi_message = String()
        # 因为消息类型是String，而目标target是int，所以说需要强制类型转换
        navi_message.data = str(target)
        # 发送消息
        navi_publisher.publish(navi_message)
    # 保持节点持续运行
    rospy.spin()