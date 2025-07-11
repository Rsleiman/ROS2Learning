#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from nav_action_walkthrough.action import Navigate


class NavigateActionServer(Node):
    def __init__(self):
        super().__init__("action_server_node")
        self._action_server = ActionServer(self, Navigate, "navigate", self.navigate_callback)


        
        print("Action Server running...")

    def navigate_callback(self, goal_handle):
        print("Received goal")
        self.robot_goal_point = [goal_handle.request.goal_point.x,
                                 goal_handle.request.goal_point.y,
                                 goal_handle.request.goal_point.z]

def main(args=None):
    rclpy.init()
    action_server_node = NavigateActionServer()

    try:
        rclpy.spin(action_server_node)
    except KeyboardInterrupt:
        action_server_node.destroy_node()


if __name__ == "__main__":
    main()