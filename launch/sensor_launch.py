from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='sensor_sim',
            executable='publisher',
            name='temperature_publisher',
            output='screen'
        ),
        Node(
            package='sensor_sim',
            executable='subscriber',
            name='temperature_subscriber',
            output='screen'
        ),
        Node(
            package='sensor_sim',
            executable='alert_node',
            name='alert_node',
            output='screen'
        ),
        Node(
            package='sensor_sim',
            executable='alert_subscriber',
            name='alert_subscriber',
            output='screen'
        ),
        Node(
            package='sensor_sim',
            executable='temperature_service',
            name='temperature_service',
            output='screen'
        ),
    ])