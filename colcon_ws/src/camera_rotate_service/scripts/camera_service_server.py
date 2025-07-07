#!/usr/bin/env python3

import os
import cv2
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from camera_rotate_service.srv import TurnCamera
from sensor_msgs.msg import Image

class TurnCameraServer(Node):
    def __init__(self):
        super().__init__("turn_camera_server_node")
        self.available_angles = [-30, -15, 0, 15, 30]
        self.srv = self.create_service(TurnCamera, "turn_camera_service", self.return_image)
        print("Turn Camera Server Running...")

    def return_image(self, request: TurnCamera, response: TurnCamera):
        self.angle = self.get_closest_available_angle(request.angle)
        im_path = self.get_im_path(self.angle)

        image = cv2.imread(im_path)
        image_msg = CvBridge().cv2_to_imgmsg(image)

        response.image = image_msg

        # print(request)
        # print(response)

        return response


    def get_closest_available_angle(self, angle):
        diff = 999
        closest_angle = 0
        for valid_angle in self.available_angles:
            if abs(valid_angle - angle) <= diff:
                diff = abs(valid_angle - angle)
                closest_angle = valid_angle
        print(f"closest angle: {closest_angle}")
        return closest_angle


    def get_im_path(self, angle):
        dir_name = os.path.dirname(__file__)
        install_dir_index = dir_name.index("install/")
        resource_path = dir_name[0:install_dir_index] + "src/camera_rotate_service/resources/images"
    
        return f"{resource_path}/{angle}.png"

def main():
    rclpy.init()
    server_node = TurnCameraServer()

    try:
        rclpy.spin(server_node)
    except KeyboardInterrupt:
        server_node.destroy_node()
        

if __name__ == "__main__":
    main()