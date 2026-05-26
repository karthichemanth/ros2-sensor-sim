import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String

class AlertNode(Node):
    def __init__(self):
        super().__init__('alert_node')
        self.subscription = self.create_subscription(
            Float32, 'temperature', self.callback, 10)
        self.publisher = self.create_publisher(String, 'alert', 10)
        self.get_logger().info('Alert node started!')

    def callback(self, msg):
        temp = msg.data
        if temp > 40.0:
            alert = String()
            alert.data = f'WARNING! Temperature critical: {temp} C'
            self.publisher.publish(alert)
            self.get_logger().warn(f'ALERT published: {temp} C')
        else:
            self.get_logger().info(f'Temperature normal: {temp} C')

def main():
    rclpy.init()
    node = AlertNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()