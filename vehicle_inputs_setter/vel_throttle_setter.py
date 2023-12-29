#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import rclpy
from rclpy.node import Node
from autonoma_msgs.msg import VehicleInputs


class vel_throttle_setter(Node):
    def __init__(self):
        super().__init__('vel_throttle_setter')

        # raw_vehicle_cmd_coverter からトピックを受信
        self.create_subscription(VehicleInputs, "/vehicle_inputs_prepare", self.onTrigger, 1)

        # dallara_interface にトピックを送信
        self.vehicle_inputs_pub_ = self.create_publisher(VehicleInputs, "/vehicle_inputs", 1)

        self.throttleb = 10

    def onTrigger(self, msg):
        self.get_logger().info("throttle_cmd {}".format(msg.throttle_cmd))
        self.get_logger().info("brake_cmd {}".format(msg.brake_cmd))
        self.get_logger().info("brake_cmd_count {}".format(msg.brake_cmd_count))
        msg.throttle_cmd = self.throttle
        # トピックを送信
        self.vehicle_inputs_pub_.publish(msg)

def main(args=None):
    print('Hi from vel_throttle_setter.')
    rclpy.init(args=args)
    node = vel_throttle_setter()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()