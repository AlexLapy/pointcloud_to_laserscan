from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    return LaunchDescription([
        # Declare arguments
        DeclareLaunchArgument(
            'use_sim_time', default_value='True',
            description='Use sim time if true'
        ),
        DeclareLaunchArgument(
            'target_frame', default_value='base_link',
            description='Target frame for point cloud to laser scan conversion'
        ),
        DeclareLaunchArgument(
            'cloud_in_topic', default_value='/velodyne_points',
            description='Input point cloud topic'
        ),
        DeclareLaunchArgument(
            'scan_topic', default_value='/scan_from_pc',
            description='Output scan topic'
        ),
        DeclareLaunchArgument(
            'scanner', default_value='scanner',
            description='Namespace for sample topics'
        ),

        # Static Transform Publisher Node
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', '1', 'map', 'cloud'],
            parameters=[{
                'use_sim_time': LaunchConfiguration('use_sim_time')
            }]
        ),

        # PointCloud to LaserScan Node
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            remappings=[
                ('cloud_in', [LaunchConfiguration('cloud_in_topic')]),
                ('scan', [LaunchConfiguration('scan_topic')])
            ],
            parameters=[{
                'use_sim_time': LaunchConfiguration('use_sim_time'),
                'target_frame': LaunchConfiguration('target_frame'),
                'transform_tolerance': 0.01,
                'min_height': -0.425,  # lidar_link height is 0.427
                'max_height': 0.10,  # Top clearance
                'angle_min': -3.14159,  # -M_PI/2
                'angle_max': 3.14159,  # M_PI/2
                'angle_increment': 0.0087,  # M_PI/360.0
                'scan_time': 0.3333,
                'range_min': 0.2,
                'range_max': 150.0,
                'use_inf': True,
                'inf_epsilon': 1.0
            }]
        )
    ])