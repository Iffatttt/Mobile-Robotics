import rclpy
from rclpy.node import Node
from std_msgs.msg import Char

class CharSubscriber(Node):
    def __init__(self):
        super().__init__('char_subscriber')
        self.subscription = self.create_subscription(
            Char, 'char_topic', self.listener_callback, 10)

    def listener_callback(self, msg):
        received_char = chr(msg.data)
        print(f'Received: {received_char}')

def main(args=None):
    rclpy.init(args=args)
    node = CharSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#an AI tool was used to assist writing this script