#!/usr/bin/env python3
from math import dist
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
from nav_action_walkthrough.action import Navigate
from geometry_msgs.msg import Point

DISTANCE_THRESHOLD = 0.05 # m

class NavigateActionServer(Node):
    def __init__(self):
        super().__init__("action_server_node")
        self._action_server = ActionServer(self, Navigate, "navigate", self.navigate_callback)
        self.position_sub = self.create_subscription(Point, "robot_position", self.update_robot_position, 1)
        self.robot_current_position = None
        print("Action Server running...")

    def navigate_callback(self, goal_handle:ServerGoalHandle):
        print("Received goal")
        start_time = self.get_clock().now()
        self.robot_goal_point = [goal_handle.request.goal_point.x,
                                 goal_handle.request.goal_point.y,
                                 goal_handle.request.goal_point.z]
        print(f"Goal point: {self.robot_goal_point}")

        while not self.robot_current_position:
            print("Waiting for robot position to be detected")
            rclpy.spin_once(self, timeout_sec=2) # spin_once does not stop rest of class from running

        self.distance_to_goal = dist(self.robot_current_position, self.robot_goal_point)
        feedback_msg = Navigate.Feedback()

        print(self.distance_to_goal)
        while self.distance_to_goal > DISTANCE_THRESHOLD:
            self.distance_to_goal = dist(self.robot_current_position, self.robot_goal_point)
            feedback_msg.distance_to_point = self.distance_to_goal
            goal_handle.publish_feedback(feedback_msg)
            rclpy.spin_once(self, timeout_sec=0.5)

        goal_handle.succeed()
        result = Navigate.Result()
        result.elapsed_time = float((self.get_clock().now() - start_time).nanoseconds / 1e9)

        return result

    
    def update_robot_position(self, point_msg: Point):
        self.robot_current_position = [point_msg.x, point_msg.y, point_msg.z]
        

def main(args=None):
    rclpy.init()
    action_server_node = NavigateActionServer()

    try:
        while rclpy.ok():
            rclpy.spin_once(action_server_node)
    except KeyboardInterrupt:
        print("Terminating node...")
        action_server_node._action_server.destroy()
        action_server_node.destroy_node()


if __name__ == "__main__":
    main()