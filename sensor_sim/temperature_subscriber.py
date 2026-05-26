import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class TemperatureSubscriber(Node):
    def __init__(self):
        super().__init__('temperature_subscriber')
        self.subscription = self.create_subscription(
            Float32, 'temperature', self.callback, 10)
        self.get_logger().info('Waiting for temperature data...')

    def callback(self, msg):
        temp = msg.data
        status = 'HOT!' if temp > 38.0 else 'Normal'
        self.get_logger().info(f'Received: {temp} C -- {status}')

def main():
    rclpy.init()
    node = TemperatureSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()