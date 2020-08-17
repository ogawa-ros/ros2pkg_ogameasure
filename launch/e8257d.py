from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2pkg_ogameasure',
            node_executable='e8257d',
            parameters=[
                {'host': '192.168.100'},
                {'port': '10001'}
            ]
        )],
       )
    
