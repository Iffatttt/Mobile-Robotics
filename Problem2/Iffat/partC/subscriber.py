import rclpy
from rclpy.node import Node
from std_msgs.msg import Char

class SubscriberNode(Node):

#constructor
    def __init__(self):
        super().__init__('char_subscriber_node')
        #(message type, topic name, function called when a message arrives, queue size)
        self.subscription = self.create_subscription(Char, 'char_topic', self.callbackFunction, 10)
        # this is to prevent an unused variable warning
        self.subscription

    # this is the callback function that is executed every time a message is received
    def callbackFunction(self, message):
        #convert the received number back to a character using chr
        receivedChar = chr(message.data)
        #print the message on the screen using the logger
        self.get_logger().info('Subscriber node received:"%s"' % receivedChar)


# main function
def main(args=None):
    # initialize
    rclpy.init(args=args)
    # create the object
    node_subscriber = SubscriberNode()
    # call the spin function that will spin the node and make sure that callbacks are called
    rclpy.spin(node_subscriber)
    node_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
