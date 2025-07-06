#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8

class Rpm_Publisher(Node):
    def __init__(self):
        super().__init__("rpm_publisher")
        self.pub = self.create_publisher(UInt8, "rpm", 10) 
        self.timer = self.create_timer(1, self.publish_rpm_callback)
        self.wheel

    def publish_rpm_callback(self):
