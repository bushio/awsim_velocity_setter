#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import rclpy
import pygame
from rclpy.node import Node
from autonoma_msgs.msg import VehicleInputs

class Controller_setter(Node):
    def __init__(self, joystick=None):
        super().__init__('Controller_setter')

        # dallara_interface からトピックを受信
        self.create_subscription(VehicleInputs, "/vehicle_inputs_prepare", self.onTrigger, 1)

        # AWSIM にトピックを送信
        self.vehicle_inputs_pub_ = self.create_publisher(VehicleInputs, "/vehicle_inputs", 1)

        # throttle を 10 で固定とする
        self.throttle = 10.0
        self.brake = 0.0

        # 0.1 秒ごとにコントローラーの入力を更新
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)

        if joystick is None:
            print("ジョイスティックが見つかりません。")
            sys.exit()
        self.joystick = joystick

    # コントローラーからの入力を更新
    def timer_callback(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        self.throttle = self.throttle + self.joystick.get_axis(3) * -1.0
        
        # Aボタンでthrottle +10
        if self.joystick.get_button(0): 
            self.throttle += 10.0
        
        # Bボタンでブレーキ
        if self.joystick.get_button(1): 
            self.throttle = 0.0
            self.brake = 800

        # Xボタンでブレーキとthrottle を 0にする。
        if self.joystick.get_button(2): 
            self.throttle = 0.0
            self.brake = 0.0
        
        # throttle が 0より大きければbrakeを0にする。
        if self.throttle > 0:
            self.brake = 0.0

        self.throttle = min(max(self.throttle, 0), 100)
        self.get_logger().info("throttle:{} brake:{}".format(self.throttle, self.brake))

    # 制御コマンドを送受信
    def onTrigger(self, msg):
        msg.throttle_cmd = float(self.throttle)
        msg.brake_cmd = float(self.brake)
        # トピックを送信
        self.vehicle_inputs_pub_.publish(msg)

def main(args=None):
    print('Hi from Controller_setter.')

    # rosノードを初期化
    rclpy.init(args=args)

    # Pygameの初期化
    pygame.init()

    # pygame を初期化
    pygame.joystick.init()

    # 利用可能なジョイスティックの数を取得
    joystick_count = pygame.joystick.get_count()

    if joystick_count == 0:
        print("ジョイスティックが見つかりません。")
        sys.exit()

    # 0番のジョイスティックを取得
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    node = Controller_setter(joystick=joystick)
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()