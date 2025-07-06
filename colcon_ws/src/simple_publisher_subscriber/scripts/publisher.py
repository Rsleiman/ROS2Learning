#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Publisher(Node):
    def __init__(self):
        super().__init__("pub_node")
        self.pub = self.create_publisher(String, "hello_world", 10)
        self.timer = self.create_timer(1, self.timer_callback)
        self.count = 0
        print("Publisher running...")

    def timer_callback(self):
        self.count += 1
        msg = String()
        msg.data = f"Hello World {self.count}"
        self.pub.publish(msg)

def main(args=None):
    rclpy.init()
    pub = Publisher()

    try:
        rclpy.spin(pub)
    except KeyboardInterrupt:
        pub.destroy_node()


if __name__ == "__main__":
    main()