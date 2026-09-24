# ------------------------commands----------------------------
#  source /opt/ros/jazzy/setup.bash
#  cd ~/ros2_ws
#  colcon build
#  ros2 pkg create --build-type ament_python first_package
#  then create publisher.py
#  edit package.xml to add library dependencies
#  edit setup.py to create entry point for talker
#  create subscriber.py
#  edit setup.py to create entry point for listener
#  rosdep install -i --from-path src --rosdistro jazzy -y
#  colcon build --packages-select first_package
# source ~/ros2_ws/install/setup.bash
#  source /opt/ros/jazzy/setup.bash
# terminal 1:ros2 run first_package talker
# terminal 2:ros2 run first_package listener


import rclpy
from std_msgs.msg import Char
from rclpy.node import Node

class PublisherNode(Node):
    def __init__(self):
        super().__init__('char_publisher')
        self.publisher=self.create_publisher(Char, 'char_topic', 10)
        comm_rate=1
        self.timer=self.create_timer(comm_rate, self.callback_function)

    def callback_function(self):
        user_input = input('Enter a character: ')
        if len(user_input)!= 1:
            self.get_logger().info('Please enter exactly one character')
            return
        msg_publisher=Char()
         #Char stores the character as a number so using ord to convert it 
        msg_publisher.data=ord(user_input)
        self.publisher.publish(msg_publisher)
        self.get_logger().info('Publisher node is publishing:"%s"' % user_input)

def main(args=None):
        rclpy.init(args=args)
        node_publisher=PublisherNode()
        rclpy.spin(node_publisher)
        node_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

