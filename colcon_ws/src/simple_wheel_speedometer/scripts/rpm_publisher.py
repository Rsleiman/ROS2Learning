#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8


class RpmPublisher(Node):
    RPM_DEFAULT = 10

    def __init__(self):
        super().__init__("rpm_publisher")
        self.pub = self.create_publisher(UInt8, "rpm", 10) 
        self.timer = self.create_timer(1, self.publish_rpm_callback)
        print("RPM Publisher Running...")

    def publish_rpm_callback(self):
        msg = UInt8()
        msg.data = self.RPM_DEFAULT
        self.pub.publish(msg)

def main():
    rclpy.init()
    pub = RpmPublisher()

    try:
        rclpy.spin(pub)
    except KeyboardInterrupt:
        pub.destroy_node()
        

if __name__ == "__main__":
    main()