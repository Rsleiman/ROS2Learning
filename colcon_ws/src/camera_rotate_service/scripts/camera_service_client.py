#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from camera_rotate_service.srv import TurnCamera

class TurnCameraClient(Node):
    def __init__(self):
        super().__init__("turn_camera_client_node")
        self.client = self.create_client(TurnCamera, "turn_camera_service")
        print("Turn Camera Client Running...")
        self.req = TurnCamera.Request()

    def send_request(self, angle):
        self.req.angle = int(angle)
        self.client.wait_for_service()
        self.future = self.client.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)

        self.result = self.future.result()
        return self.result

def main():
    rclpy.init()
    client_node = TurnCameraClient()

    try:
        user_input = input("Enter an angle: ")
        res = client_node.send_request(user_input)
        print(f"Server returned: {res.decision}")
    except KeyboardInterrupt:
        client_node.destroy_node()
        

if __name__ == "__main__":
    main()