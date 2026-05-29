#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from sensor_sim_interfaces.srv import GetTemperature


class TemperatureService(Node):
    def __init__(self):
        super().__init__('temperature_service')
        self.latest_temp = None

        # Cache latest temperature from the topic
        self.subscription = self.create_subscription(
            Float32, 'temperature', self.temp_callback, 10)

        # Service server — answers "what is the current temperature?"
        self.srv = self.create_service(
            GetTemperature, 'get_temperature', self.handle_request)

        self.get_logger().info('Temperature service started!')

    def temp_callback(self, msg):
        self.latest_temp = msg.data

    def handle_request(self, request, response):
        if self.latest_temp is not None:
            response.temperature = self.latest_temp
            response.status = f'OK - Latest reading: {self.latest_temp} C'
            self.get_logger().info(f'Service request served: {self.latest_temp} C')
        else:
            response.temperature = 0.0
            response.status = 'ERROR - No temperature data received yet'
            self.get_logger().warn('Service request received but no data yet')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = TemperatureService()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
