import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class TemperaturePublisher(Node):
    def __init__(self):
        super().__init__('temperature_publisher')
        self.publisher = self.create_publisher(Float32, 'temperature', 10)
        self.timer = self.create_timer(1.0, self.publish_temp)
        self.get_logger().info('Temperature publisher started!')

    def publish_temp(self):
        temp = Float32()
        temp.data = round(random.uniform(20.0, 45.0), 2)
        self.publisher.publish(temp)
        self.get_logger().info(f'Published: {temp.data} C')

def main():
    rclpy.init()
    node = TemperaturePublisher()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()