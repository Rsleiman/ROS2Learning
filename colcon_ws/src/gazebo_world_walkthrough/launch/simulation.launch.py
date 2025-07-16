from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

# Retrieving path information
from ament_index_python.packages import get_package_share_directory
from pathlib import Path

# Utilising launch files from other packages
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

# Set environment variables
from launch.actions import SetEnvironmentVariable

# Simulation event handling
from launch.actions import RegisterEventHandler, EmitEvent
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown 


ign_ros_pkg_path = get_package_share_directory("ros_gz_sim")
gazebo_world_walkthrough_pkg_path = get_package_share_directory("gazebo_world_walkthrough")
sim_world_file_path = Path(gazebo_world_walkthrough_pkg_path, "worlds/wheeled_model_world.sdf").as_posix()
sim_models_path = Path(gazebo_world_walkthrough_pkg_path, "models").as_posix()

### Can't use with event handlers ###
# # Way to include external launch descriptions from other packages
# simulation = IncludeLaunchDescription(
#                 PythonLaunchDescriptionSource(
#                     launch_file_path=Path(ign_ros_pkg_path, "launch/gz_sim.launch.py").as_posix()
#                 ),
#                 launch_arguments=[("gz_args", f"-r {sim_world_file_path}")]
#             )

simulation = ExecuteProcess(
    cmd=["ign", "gazebo", "-r", sim_world_file_path],
    output="screen"
)

def generate_launch_description():
    return LaunchDescription([
        SetEnvironmentVariable(
            name="IGN_GAZEBO_RESOURCE_PATH",
            value=sim_models_path
        ),
        simulation,
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            arguments=["/model/wheeled_model/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist"],
            # ros_arguments=["-r /model/wheeled_model/cmd_vel:=/cmd_vel"], # Using ros arguments to remap topic name
            remappings=[("/model/wheeled_model/cmd_vel", "/cmd_vel")], # Using remappings parameter directly to remap topic names
            output="screen"
        ),
        # Shutdown ROS instance if we close gazebo simulation
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=simulation,
                on_exit=[EmitEvent(event=Shutdown())]
            )
        )
    ])