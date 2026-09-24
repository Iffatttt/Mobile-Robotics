#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
import time

class CosineWaveDriver(Node):
    def __init__(self):
        super().__init__('cosine_wave_driver')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.v = 1.5          # v
        self.amp = 1.0        # omega
        self.freq = 0.6       # oscillation
        self.start_time = time.time()
        self.timer = self.create_timer(0.05, self.publish_cmd)  # 20 Hz

    def publish_cmd(self):
        t = time.time() - self.start_time
        msg = Twist()
        msg.linear.x = self.v
        msg.angular.z = self.amp * math.cos(self.freq * t)
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CosineWaveDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
