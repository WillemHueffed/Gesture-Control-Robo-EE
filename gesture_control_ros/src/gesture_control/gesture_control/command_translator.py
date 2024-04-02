import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# Pose is my custom message interface
from gesture_interfaces.msg import Pose

class CommandTranslator(Node):

    def __init__(self):
        super().__init__('command_translator')
        self.pose_publisher = self.create_publisher(Pose, 'gesture_cmd', 10)
        self.subscriber = self.create_subscription(String, 'recognized_gesture', self.listener_callback, 10)

    # The listener callback converts hand gestures into pose commands
    def listener_callback(self, msg):
        pose_msg = Pose()

        if msg.data == 'None':
            pass
        if msg.data == 'Open_Palm':
            pose_msg.z = 0.01
        if msg.data == 'Closed_Fist':
            pose_msg.z = -0.01
        if msg.data == 'Thumb_Up':
            pose_msg.x = 0.01
        if msg.data == 'Thumb_Down':
            pose_msg.x = -0.01
        if msg.data == 'Victory':
            pose_msg.y = 0.01
        if msg.data == 'Pointing_Up':
            pose_msg.y = -0.01
        if msg.data == 'ILoveYou':
            pose_msg.reset = True

        # Publish the translated message
        self.pose_publisher.publish(pose_msg)

def main(args=None):
    rclpy.init(args=args)
    command_translator = CommandTranslator()
    rclpy.spin(command_translator)
    command_translator.destory_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
