# 动作控制
import struct
from datetime import time
from socket import socket


class ControlRobot():
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_addr = ('192.168.1.120', 43893)

    def send_pack(self, code, value, type):  # 发送指令包
        pack = struct.pack("<3i", code, value, type)
        self.udp_socket.sendto(pack, self.send_addr)

    def auto_control(self):  # 发送自动模式指令
        self.send_pack(0x21010C03, 0, 0)
        time.sleep(0.05)

    def hand_control(self):  # 发送手动模式指令
        self.send_pack(0x21010C02, 0, 0)
        time.sleep(0.05)

    def in_place(self):  # 发送原地模式指令
        self.send_pack(0x21010D05, 0, 0)
        time.sleep(0.05)

    def mobile(self):  # 发送移动模式指令
        self.send_pack(0x21010D06, 0, 0)
        time.sleep(0.05)

    def stand_up(self):  # 起立
        self.send_pack(0x21010202, 0, 0)
        self.send_pack(0x21010D06, 0, 0)
        time.sleep(5)

    def get_down(self):  # 趴下
        self.send_pack(0x21010202, 0, 0)
        time.sleep(2)

    def obstacle(self):  # 越障
        self.send_pack(0x21010401, 0, 0)
        time.sleep(0.05)

    def normal_move(self):  # 正常步态
        self.send_pack(0x21010300, 0, 0)
        time.sleep(0.05)

    # 抬头低头 value为幅度
    def nod(self, value):
        self.send_pack(0x21010130, value, 0)

    # 摇头 value为幅度
    def shake(self, value):
        self.send_pack(0x21010135, value, 0)

    # 前进
    def forward(self, duration):
        start_time = time.time()
        while time.time() - start_time < duration:
            self.send_pack(0x21010130, 13000, 0)
            time.sleep(0.05)

    # 左走
    def move_left(self, duration):
        self.hand_control()
        self.auto_control()
        self.hand_control()
        start_time = time.time()
        while time.time() - start_time < duration:
            self.send_pack(0x21010131, -20000, 0)
            time.sleep(0.05)
        self.hand_control()
        self.auto_control()

    # 右走
    def move_right(self, duration):
        self.hand_control()
        self.auto_control()
        self.hand_control()
        start_time = time.time()
        while time.time() - start_time < duration:
            self.send_pack(0x21010131, 20000, 0)
            time.sleep(0.05)
        self.hand_control()
        self.auto_control()

    # 左转90度
    def voice_tl_90(self):
        self.hand_control()
        self.auto_control()
        self.hand_control()
        self.send_pack(0x21010C0A, 13, 0)
        time.sleep(2.5)
        self.hand_control()
        self.auto_control()

    # 右转90度
    def voice_tr_90(self):
        self.hand_control()
        self.auto_control()
        self.hand_control()
        self.send_pack(0x21010C0A, 14, 0)
        time.sleep(2.5)
        self.hand_control()
        self.auto_control()