#!/usr/bin/env python3
# coding=utf-8

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

if __name__ == '__main__':
    rospy.init_node("nav_client")
    actionclient = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    actionclient.wait_for_server()

    goal = MoveBaseGoal()

    goal.target_pose.header.frame_id = "map"
    goal.target_pose.pose.position.x = -3.0
    goal.target_pose.pose.position.y = 2.0
    goal.target_pose.pose.position.z = 0.0

    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.0
    goal.target_pose.pose.orientation.w = 1.0

    actionclient.send_goal(goal)
    rospy.logwarn("导航开始")
    actionclient.wait_for_result()

    if actionclient.get_state() == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("导航成功")
    else:
        rospy.loginfo("导航失败")


