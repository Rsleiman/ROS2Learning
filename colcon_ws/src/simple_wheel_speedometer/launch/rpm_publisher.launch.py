from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        Node(package="simple_wheel_speedometer",
             executable="rpm_publisher.py",
             name="rpm_publisher"),
             ExecuteProcess(
                 cmd=["ros2", "topic", "list"],  
                 output="screen"
             )
    ])