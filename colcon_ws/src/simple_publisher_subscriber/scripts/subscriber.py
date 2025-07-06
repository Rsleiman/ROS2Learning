#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Subscriber(Node):
    def __init__(self):
        super().__init__("sub_node")
        self.sub = self.create_subscription(String, "hello_world", self.subscriber_callback, 10)
        print("Waiting for data to be published...")

    def subscriber_callback(self, msg):
        print(f"I received message: {msg}")


def main(args=None):
    rclpy.init()
    sub = Subscriber()

    try:
        rclpy.spin(sub)
    except KeyboardInterrupt:
        sub.destroy_node()


if __name__ == "__main__":
    main() 