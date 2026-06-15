#!/usr/bin/env python3
# Description: Broadcasts TF2 transforms for our robot's sensors

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import math


class RobotTFPublisher(Node):
    def __init__(self):
        super().__init__('robot_tf_publisher')

        # TF2 broadcaster
        self.broadcaster = TransformBroadcaster(self)

        # Timer — 50Hz-ல transforms broadcast பண்றோம்
        self.timer = self.create_timer(0.02, self.broadcast_transforms)

        # Robot position (simulate பண்றோம்)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0  # Robot heading angle

        self.get_logger().info('Robot TF Publisher started!')

    def make_transform(self, parent, child, x, y, z, roll=0.0, pitch=0.0, yaw=0.0):
        """Helper — ஒரு transform create பண்றது"""
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = parent
        t.child_frame_id = child

        t.transform.translation.x = x
        t.transform.translation.y = y
        t.transform.translation.z = z

        # Euler angles → Quaternion convert பண்றோம்
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)

        t.transform.rotation.w = cr * cp * cy + sr * sp * sy
        t.transform.rotation.x = sr * cp * cy - cr * sp * sy
        t.transform.rotation.y = cr * sp * cy + sr * cp * sy
        t.transform.rotation.z = cr * cp * sy - sr * sp * cy

        return t

    def broadcast_transforms(self):
        transforms = []

        # 1. odom → base_link (robot moving in circle)
        self.theta += 0.01  # Slowly rotate
        self.x = 2.0 * math.cos(self.theta)  # Circle path
        self.y = 2.0 * math.sin(self.theta)

        transforms.append(self.make_transform(
            'odom', 'base_link',
            self.x, self.y, 0.0,
            yaw=self.theta
        ))

        # 2. base_link → front_camera
        transforms.append(self.make_transform(
            'base_link', 'front_camera',
            0.525, 0.0, 0.0  # Robot front-ல
        ))

        # 3. base_link → back_camera
        transforms.append(self.make_transform(
            'base_link', 'back_camera',
            -0.525, 0.0, 0.0,  # Robot back-ல
            yaw=math.pi         # 180° திரும்பி
        ))

        # 4. base_link → lidar
        transforms.append(self.make_transform(
            'base_link', 'lidar',
            0.0, 0.0, 0.24  # Robot top-ல
        ))

        # 5. map → odom (static — நாம் map origin-ல start பண்றோம்)
        transforms.append(self.make_transform(
            'map', 'odom',
            0.0, 0.0, 0.0
        ))

        self.broadcaster.sendTransform(transforms)


def main(args=None):
    rclpy.init(args=args)
    node = RobotTFPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()