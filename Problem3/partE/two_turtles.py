import math
import rclpy
from rclpy.node import Node

#pose of a frame
from geometry_msgs.msg import TransformStamped
#used to publish transforms to tf2
from tf2_ros import TransformBroadcaster

#turtlesim services: Spawn creates a new turtle, TeleportAbsolute sets a pose,SetPen turns the drawing pen on or off
from turtlesim.srv import Spawn, TeleportAbsolute, SetPen

#parameters
R = 5.0            
w = 0.40           
T = 8.0            
a = 3.0            
lam = 6.0          
Om = 2 * math.pi / T

#the turtlesim window is only 11 x 11, so we scale the world down
scale = 0.5
#the world origin is placed at the centre of the turtlesim window
cx = 5.544
cy = 5.544

#from (a)
def poseA(t):
    x = R * math.cos(w * t)
    y = R * math.sin(w * t)
    theta = w * t + math.pi / 2
    return x, y, theta


#part b
def poseB(t):
    s = lam * t / T                       
    x = -(1 / math.sqrt(2)) * (s + a * math.sin(Om * t))
    y = (1 / math.sqrt(2)) * (s - a * math.sin(Om * t))
    vx = -(1 / math.sqrt(2)) * (lam / T + a * Om * math.cos(Om * t))
    vy = (1 / math.sqrt(2)) * (lam / T - a * Om * math.cos(Om * t))
    theta = math.atan2(vy, vx)
    return x, y, theta

class TwoTurtleNode(Node):

    # constructor
    def __init__(self):
        super().__init__('two_turtles_node')

        self.broadcaster = TransformBroadcaster(self)

        #service clients for turtlesim
        self.spawnClient = self.create_client(Spawn, '/spawn')
        self.teleportA = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.teleportB = self.create_client(TeleportAbsolute, '/turtle2/teleport_absolute')
        self.penA = self.create_client(SetPen, '/turtle1/set_pen')
        self.penB = self.create_client(SetPen, '/turtle2/set_pen')

        #spawn robot B at the world origin
        self.spawnClient.wait_for_service()
        spawnRequest = Spawn.Request()
        spawnRequest.x = cx
        spawnRequest.y = cy
        spawnRequest.theta = 0.0
        spawnRequest.name = 'turtle2'
        self.spawnClient.call_async(spawnRequest)

        # time when we started, used to compute t
        self.startTime = self.get_clock().now()
        # one full revolution of robot A, after this we stop
        self.revolution = 2 * math.pi / w
        #counts timer calls, used to lift the pens during the first jump
        self.stepCount = 0

        commRate = 0.02  #50 times per second
        self.timer = self.create_timer(commRate, self.callbackFunction)

    def makeTransform(self, childName, x, y, theta):
        transform = TransformStamped()
        # time stamp and the names of the parent and child frames
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = 'world'
        transform.child_frame_id = childName
        #translation
        transform.transform.translation.x = x
        transform.transform.translation.y = y
        transform.transform.translation.z = 0.0
        #rotation about z
        transform.transform.rotation.x = 0.0
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = math.sin(theta / 2)
        transform.transform.rotation.w = math.cos(theta / 2)
        return transform

    #this function places a turtle at a pose in the turtlesim window
    def teleport(self, client, x, y, theta):
        if client.service_is_ready():
            request = TeleportAbsolute.Request()
            request.x = cx + scale * x
            request.y = cy + scale * y
            request.theta = theta
            client.call_async(request)

    #turns a turtle's pen on (off=0) or off (off=1)
    def setPen(self, client, off):
        if client.service_is_ready():
            request = SetPen.Request()
            request.r = 255
            request.g = 255
            request.b = 255
            request.width = 2
            request.off = off
            client.call_async(request)

    def callbackFunction(self):
        #time since start in seconds
        t = (self.get_clock().now() - self.startTime).nanoseconds * 1e-9

        #stop after one full revolution of A
        if t > self.revolution:
            self.timer.cancel()
            self.get_logger().info('One full revolution of robot A completed, stopping')
            return

        #compute both poses from the equations of parts (a) and (b)
        xA, yA, thetaA = poseA(t)
        xB, yB, thetaB = poseB(t)

        #publish the transforms to tf2
        transformA = self.makeTransform('robot_a', xA, yA, thetaA)
        transformB = self.makeTransform('robot_b', xB, yB, thetaB)
        self.broadcaster.sendTransform([transformA, transformB])

        #lift the pens at the start so no line is drawn while the turtles jump to their starting positions, then put them back down
        if self.stepCount == 0:
            self.setPen(self.penA, 1)
            self.setPen(self.penB, 1)
        if self.stepCount == 10:
            self.setPen(self.penA, 0)
            self.setPen(self.penB, 0)
        self.stepCount = self.stepCount + 1

        #place the turtles at their poses in the turtlesim window
        self.teleport(self.teleportA, xA, yA, thetaA)
        self.teleport(self.teleportB, xB, yB, thetaB)

        self.get_logger().info('t = %.2f s | A: (%.2f, %.2f) | B: (%.2f, %.2f)' % (t, xA, yA, xB, yB))


def main(args=None):
    rclpy.init(args=args)
    node_dance = TwoTurtleNode()
    rclpy.spin(node_dance)
    node_dance.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
