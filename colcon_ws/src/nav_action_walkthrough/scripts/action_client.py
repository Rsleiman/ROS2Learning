#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav_action_walkthrough.action import Navigate
from rclpy.task import Future

DISTANCE_THRESHOLD = 0.4 # m

class NavigateActionClient(Node):
    def __init__(self):
        super().__init__("action_client_node")
        self._action_client = ActionClient(self, Navigate, "navigate")
        print("Action Client running...")


    def send_goal(self, x, y, z):
        goal_msg = Navigate.Goal()
        goal_msg.goal_point.x = float(x)
        goal_msg.goal_point.y = float(y)
        goal_msg.goal_point.z = float(z)

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback) # To see if server accepts or rejects our goal

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        print(f"Feedback: {feedback.distance_to_point}")

    def goal_response_callback(self, future: Future):
        goal_handle = future.result()
        if goal_handle.accepted == False:
            print("Goal Rejected...")
            return None
        
        print("Goal Accepted")
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback) # To see what the result of the accepted goal is once accomplished

    def get_result_callback(self, future: Future):
        result = future.result().result
        print(f"Result: {result.elapsed_time} seconds")
        rclpy.shutdown()



def main(args=None):
    rclpy.init()
    action_client_node = NavigateActionClient()

    try:
        x = input("Enter X coordinate: ")
        y = input("Enter Y coordinate: ")
        z = input("Enter Z coordinate: ")

        action_client_node.send_goal(x, y, z)
        rclpy.spin(action_client_node)
    except KeyboardInterrupt:
        print("Terminating Node...")
        action_client_node.destroy_node()


if __name__ == "__main__":
    main()