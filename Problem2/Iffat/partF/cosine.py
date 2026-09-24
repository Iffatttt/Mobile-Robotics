import math
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

topic1='/turtle1/cmd_vel'
#messages per second
period= 20

#cosine wave parameters
A = 1.0                     
wavelength = 4.0            
k = 2 * math.pi / wavelength
vx = 0.5                   

def main(args=None):

    rclpy.init(args=args)
    controlVel = Twist()

    TestNode = Node('cosine_wave_node')
    publisher = TestNode.create_publisher(Twist, topic1, 1)

    #sending period messages per second
    rate = TestNode.create_rate(period)

    startTime = TestNode.get_clock().now()

    while rclpy.ok():
        #time since start in seconds
        t = (TestNode.get_clock().now() - startTime).nanoseconds * 1e-9

        # position along the wave
        x = vx * t
        slope = -A * k * math.sin(k * x)

        #forward speed: the turtle moves vx along x and vx*slope along y
        v = vx * math.sqrt(1 + slope ** 2)
        # turning rate:derivative of the heading angle theta = atan(slope)
        # dtheta/dt = w
        w = -A * k ** 2 * vx * math.cos(k * x) / (1 + slope ** 2)

        # components of the linear velocity vector
        #differential drive: only forward motion, no sideways motion
        controlVel.linear.x = v
        controlVel.linear.y = 0.0
        controlVel.linear.z = 0.0
        #components of the angular velocity vector
        #only the z-component is used, since the robot moves in 2D
        controlVel.angular.x = 0.0
        controlVel.angular.y = 0.0
        controlVel.angular.z = w

        print('Sending control message: v = %.2f, w = %.2f' % (v, w))
        publisher.publish(controlVel)

        #Execute one item of work or wait until a timeout expires.
        rclpy.spin_once(TestNode)
        #sleep for the specified period
        rate.sleep()

    TestNode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
