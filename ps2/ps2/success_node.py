#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

class SuccessNode(Node):
    def __init__(self):
        super().__init__('success_node')
        self.get_logger().info("Package created successfully")

def main():
    rclpy.init()
    node = SuccessNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
