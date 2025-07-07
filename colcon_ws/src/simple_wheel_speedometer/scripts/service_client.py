#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from simple_wheel_speedometer.srv import OddEvenCheck

class OddEvenCheckClient(Node):
    def __init__(self):
        super().__init__("odd_even_client_node")
        self.client = self.create_client(OddEvenCheck, "odd_even_check_service")
        print("Odd/Even Check Client Running...")
        self.req = OddEvenCheck.Request()

    def send_request(self, number):
        self.req.number = int(number)
        self.client.wait_for_service()
        self.future = self.client.call_async(self.req) # QUESTION: What is a ROS Future?
        rclpy.spin_until_future_complete(self, self.future)

        self.result = self.future.result()
        return self.result

def main():
    rclpy.init()
    client_node = OddEvenCheckClient()

    try:
        user_input = input("Enter an integer: ")
        res = client_node.send_request(user_input)
        print(f"Server returned: {res.decision}")
    except KeyboardInterrupt:
        client_node.destroy_node()
        

if __name__ == "__main__":
    main()