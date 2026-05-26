import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class AlertSubscriber(Node):
    def __init__(self):
        super().__init__('alert_subscriber')
        self.subscription = self.create_subscription(
            String, 'alert', self.callback, 10)
        self.get_logger().info('Alert subscriber waiting...')

    def callback(self, msg):
        self.get_logger().error(f'🚨 {msg.data}')

def main():
    rclpy.init()
    node = AlertSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()