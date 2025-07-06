#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8, Float32

class SpeedCalculater(Node):
    WHEEL_RADIUS_M = 0.125
    WHEEL_CIRCUMFERENCE_M = 2*3.14159*WHEEL_RADIUS_M

    def __init__(self):
        super().__init__("speed_calc")
        self.sub = self.create_subscription(UInt8, "rpm", self.speed_publisher, 10)
        self.speed_pub = self.create_publisher(Float32, "speed", 10) 
        print("Speed calculator running...")

    def speed_publisher(self, rpm_msg: UInt8):
        """
        speed calculation:
            - Wheel circumference (m) = 2*Pi*r = 2*Pi*wheelRadius_m
            - RPS = RPM/60
            - Speed = RPS * Wheel circumference
        """
        rps = float(rpm_msg.data)/60
        speed = rps*self.WHEEL_CIRCUMFERENCE_M # in m/s

        speed_msg = Float32() 
        speed_msg.data = speed
        self.speed_pub.publish(speed_msg)


def main():
    rclpy.init()
    speed_calc = SpeedCalculater()

    try:
        rclpy.spin(speed_calc)
    except KeyboardInterrupt:
        speed_calc.destroy_node()
        

if __name__ == "__main__":
    main()
