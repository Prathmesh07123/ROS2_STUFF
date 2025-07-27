import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
# from launch_ros.substitutions
# from launch_ros.actions import Node
# from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
import os
from launch_ros.descriptions import ParameterValue

'''from launch import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution'''

#import xacro
#from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='differential_robot_description').find('differential_robot_description')
    world_pkg = launch_ros.substitutions.FindPackageShare(package='slam_diffrobot').find('slam_diffrobot')
    default_model_path = os.path.join(pkg_share,'urdf/differential_robot.xacro')
    default_rviz_config_path=os.path.join(pkg_share,'config/display.rviz')


    use_sim_time = LaunchConfiguration('use_sim_time',default='True')
    world_path = os.path.join(world_pkg,'worlds/wall.sdf')

    #xacro_file = os.path.join(pkg_share, 'models/urdf', 'diff_drive_robot.xacro')
    #robot_description_config = xacro.process_file(xacro_file)
    #robot_urdf = robot_description_config.toxml()

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time},{'robot_description': ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),value_type=str)}]
    )

    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters= [{'use_sim_time': use_sim_time}],
    )

    spawn_entity = launch_ros.actions.Node(
        
    condition= IfCondition(use_sim_time),
    package='gazebo_ros',
    executable='spawn_entity.py',
    arguments=['-entity', 'differential_robot', '-topic', 'robot_description'],
    parameters= [{'use_sim_time': use_sim_time}],
    output='screen'
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                    description='Flag to enable use_sim_time'),

        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),

        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        launch.actions.ExecuteProcess(condition= IfCondition(use_sim_time),cmd=['gazebo', '--verbose', '-s', 
                                            'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so',world_path], 
                                            output='screen'),
        robot_state_publisher_node,
        joint_state_publisher_node,
        spawn_entity,
   
    ])
