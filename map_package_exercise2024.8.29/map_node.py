#!/usr/bin/env python3
#coding = utf-8

import rospy
from nav_msgs.msg import OccupancyGrid

if __name__ == '__main__':
    rospy.init_node("map_test_node")
    rospy.logwarn("map_test_node start running")

    map_publisher = rospy.Publisher("/map", OccupancyGrid, queue_size = 10)

    map_rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        map_message = OccupancyGrid()
        # 坐标系ID
        map_message.header.frame_id = "map"
        # 时间戳
        map_message.header.stamp = rospy.Time.now()

        # 地图信息
        # 地图的原点位置，也就是地图中（0，0）和真实世界原点的xy轴的偏移量
        map_message.info.origin.position.x = 0
        map_message.info.origin.position.y = 0
        # 地图的分辨率（单元格的边长，单位：m）
        map_message.info.resolution = 1.0
        # 地图的长宽（高） （单位：栅格数）
        map_message.info.width = 4
        map_message.info.height = 4

        # 地图数据
        map_message.data = [0] * map_message.info.width * map_message.info.height
        map_message.data[0] = 100
        map_message.data[1] = 100
        map_message.data[2] = 0
        map_message.data[3] = -1

        # 发布地图
        map_publisher.publish(map_message)
        map_rate.sleep()




