from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="simple_wheel_speedometer",
            executable="rpm_publisher.py",
            name="rpm_publisher",
        ),
        Node(
            package="simple_wheel_speedometer",
            executable="speed_calc.py",
            name="speed_calc",
            parameters=[{"wheel_radius_m":0.2}]
        ),
        ExecuteProcess(
            cmd=["ros2", "topic", "echo", "speed"],
            output="screen"
        )
    ])
