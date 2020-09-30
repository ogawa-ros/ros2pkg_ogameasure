from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2pkg_ogameasure',
            node_executable='nd287',
            parameters=[
                {'~az_usbport': 'azz'},
                {'~el_usbport': 'ell'}
            ]
        )],
       )
    
