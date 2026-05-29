#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_sim_interfaces.srv import GetTemperature


class TemperatureClient(Node):
    def __init__(self):
        super().__init__('temperature_client')
        self.client = self.create_client(GetTemperature, 'get_temperature')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for temperature_service...')

        self.get_logger().info('Connected to temperature service!')

    def request_temperature(self):
        request = GetTemperature.Request()
        return self.client.call_async(request)


def main(args=None):
    rclpy.init(args=args)
    node = TemperatureClient()

    future = node.request_temperature()
    rclpy.spin_until_future_complete(node, future)

    response = future.result()
    node.get_logger().info(f'Status:      {response.status}')
    node.get_logger().info(f'Temperature: {response.temperature} C')

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
