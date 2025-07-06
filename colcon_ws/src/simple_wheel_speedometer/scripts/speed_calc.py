#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt8, Float32

class SpeedCalculater(Node):
    WHEEL_RADIUS_DEFAULT_M = 0.125

    def __init__(self):
        super().__init__("speed_calc")
        self.declare_parameter("wheel_radius_m", self.WHEEL_RADIUS_DEFAULT_M)
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
        wheel_radius_m_param = self.get_parameter("wheel_radius_m").get_parameter_value().double_value
        wheel_circumference_m = 2*3.14159*wheel_radius_m_param
        speed = rps*wheel_circumference_m # in m/s

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
