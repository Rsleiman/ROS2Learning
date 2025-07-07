#!/usr/bin/env python3

import cv2
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from camera_rotate_service.srv import TurnCamera

class TurnCameraServer(Node):
    def __init__(self):
        super().__init__("turn_camera_server_node")
        self.srv = self.create_service(TurnCamera, "turn_camera_service", self.turn_camera_response)
        print("Turn Camera Server Running...")

    def turn_camera_response(self, request: TurnCamera, response: TurnCamera):
        print("Request received")

        self.angle = request.angle
        im_path = f"{PROJECT_NAME}/resources/images/{self.angle}.png"

        image = cv2.imread(im_path)
        cv2.imshow(image)
        

        # print(request)
        # print(response)

        return response
        


def main():
    rclpy.init()
    server_node = TurnCameraServer()

    try:
        rclpy.spin(server_node)
    except KeyboardInterrupt:
        server_node.destroy_node()
        

if __name__ == "__main__":
    main()