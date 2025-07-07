#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from simple_wheel_speedometer.srv import OddEvenCheck

class OddEvenCheckServer(Node):
    def __init__(self):
        super().__init__("odd_even_server_node")
        self.srv = self.create_service(OddEvenCheck, "odd_even_check_service", self.odd_even_response)
        print("Odd/Even Check Server Running...")

    def odd_even_response(self, request: OddEvenCheck, response: OddEvenCheck):
        print("Request received")

        if request.number % 2 == 0:
            response.decision = "Even"
        elif request.number % 2 == 1:
            response.decision = "Odd"
        else:
            response.decision = "Error"

        # print(request)
        # print(response)

        return response
        


def main():
    rclpy.init()
    server_node = OddEvenCheckServer()

    try:
        rclpy.spin(server_node)
    except KeyboardInterrupt:
        server_node.destroy_node()
        

if __name__ == "__main__":
    main()