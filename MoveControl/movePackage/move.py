import sys
import time
from ipykernel.heartbeat import Heartbeat
from MoveControl.movePackage import ControlRobot
from MoveControl.movePackage import MoveControl


def odom_callback(msg):
    print("腿部里程计调用")
    global body_x, body_y
    print(f"body_x:{body_x}   body_y:{body_y}")

class MoveControl:
    def __init__(self):
        # 连接机器狗的运动主机及其端口
        self.server_address = ("192.168.1.120", 43893)
        self.engine = pyttsx3.init()
        self.speak_engine()
        # 速度发布 话题是cmd_vel；消息类型是Twist
        self.vel_cmd = Twist()
        self.vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=5)
    # 速度设置函数
    def vel_cmd_config(self, x=0.0, y=0.0, z=0.0):
        self.vel_cmd.linear.x = x
        self.vel_cmd.linear.y = y
        # angular是控制狗的旋转
        self.vel_cmd.angular.z = z
        self.vel_pub.publish(self.vel_cmd)

move_controller = MoveControl
robot_controller = ControlRobot
body_x = 0
body_y = 0
if __name__ == '__main__':
    # 初始化ROS节点
    rospy.init_node('move_node')
    # 订阅腿部里程计
    leg_odom_sub = rospy.Subscriber('leg_odom', PoseWithCovarianceStamped, odom_callback, queue_size=10)

    # 发送信号包，让狗能够持续受到控制
    heart = Heartbeat()
    time.sleep(1)
    print("Wait 5 seconds and stand up......")
    # 狗起立了
    robot_controller.stand_up()
    # 如果没有起立，那么就提示应该重启程序
    print("Now,dog should stand up, otherwise press 'ctrl + c' to shut down and re-run the demo")
    # 发送自主模式指令
    robot_controller.auto_control()
    # 输入指令开始运行
    run_flag = int(input("输入1开始运行:"))
    # 如果输入的不是1，那么直接关闭程序
    if run_flag != 1:
        sys.exit()
    # 初始点
    target = -1
    # 初始化计时
    time_threshold = 20
    timer = time.time()
    try:
        while not rospy.is_shutdowm():
            if target == 0:
                if body_x < 0.85:
                    # 当x方向没有到0.85的时候，发送x方向的速度：0.15
                    move_controller.vel_cmd_config(0.15, 0)
                if body_x >= 0.85:
                    time.sleep(3)
                    move_controller.vel_cmd_config(0.15, 0)
                    print("开启越障模式了")
                    # 开启越障模式
                    robot_controller.obstacle()
                    move_controller.vel_cmd_config(0.15, 0)
                    if body_x >= 1.3:
                        move_controller.vel_cmd_config(0, 0)
                        # 关闭避障模式
                        # 继续前进到转向点
                        move_controller.vel_cmd_config(0.15, 0)
                        target = 1
            elif target == 1:
                # 右转
                robot_controller.voice_tr_90()
                time.sleep(3)
                move_controller.vel_cmd_config(0.15)
                if body_y > -0.9:
                    ControlRobot.in_place()
                    # 抬头
                    ControlRobot.nod()
                    time.time(3)
                    target = 2

            elif target == 2:
                # 左转
                robot_controller.voice_tl_90()
                time.sleep(3)
                # 切换匍匐

                move_controller.vel_cmd_config(0.15)
                if body_x >= 4.2:
                    ControlRobot.in_place()
                    robot_controller.shake()
                    time.time(3)
                    robot_controller.shake()













