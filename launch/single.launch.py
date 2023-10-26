import os
import sys

import launch
import launch_ros.actions


def generate_launch_description():
    ld = launch.LaunchDescription(
        [
            launch.actions.DeclareLaunchArgument(name="eta", default_value="1.0"),
            launch.actions.DeclareLaunchArgument(name="Geta", default_value="15.0"),
            launch_ros.actions.Node(
                package="rrt_exploration",
                executable="global_rrt_detector",
                name="global_detector",
                output="screen",
                parameters=[
                    {"namespace_init_count": 1},
                    {"eta": launch.substitutions.LaunchConfiguration("Geta")},
                    {"map_topic": "/robot_1/map"},
                ],
            ),
            launch_ros.actions.Node(
                package="rrt_exploration",
                executable="local_rrt_detector",
                name="local_detector",
                output="screen",
                parameters=[
                    {"namespace_init_count": 1},
                    {"eta": launch.substitutions.LaunchConfiguration("eta")},
                    {"map_topic": "/robot_1/map"},
                    {"robot_frame": "/robot_1/base_link"},
                ],
            ),
            launch_ros.actions.Node(
                package="rrt_exploration",
                executable="filter.py",
                name="filter",
                output="screen",
                parameters=[
                    {"namespace_init_count": 1},
                    {"map_topic": "/robot_1/map"},
                    {"info_radius": "1"},
                    {"costmap_clearing_threshold": "70"},
                    {"goals_topic": "/detected_points"},
                    {"namespace": "/robot_"},
                    {"n_robots": "1"},
                    {"rate": "100"},
                ],
            ),
            launch_ros.actions.Node(
                package="rrt_exploration",
                executable="assigner.py",
                name="assigner",
                output="screen",
                parameters=[
                    {"namespace_init_count": 1},
                    {"map_topic": "/robot_1/map"},
                    {"global_frame": "/robot_1/map"},
                    {"info_radius": "1"},
                    {"info_multiplier": "3.0"},
                    {"hysteresis_radius": "3.0"},
                    {"hysteresis_gain": "2.0"},
                    {"frontiers_topic": "/filtered_points"},
                    {"n_robots": "1"},
                    {"namespace": "/robot_"},
                    {"delay_after_assignement": "0.5"},
                    {"rate": "100"},
                ],
            ),
        ]
    )
    return ld


if __name__ == "__main__":
    generate_launch_description()
