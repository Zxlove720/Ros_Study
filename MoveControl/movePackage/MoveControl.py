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
