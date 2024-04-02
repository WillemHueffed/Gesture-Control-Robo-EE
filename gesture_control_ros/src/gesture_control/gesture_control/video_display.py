import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
import cv2
from sensor_msgs.msg import Image

class VideoDisplay(Node):

    def __init__(self):
        super().__init__('video_display')

        # Subscribe to the camera Feed
        self.subscriber_ = self.create_subscription(Image, 'rs_camera_feed', self.listener_callback, 10)

        # Create bridge object to allow OpenCV image format to be casted into ROS2 image format
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        try:
            # Cast ROS2 image -> OpenCV Image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Display the image with OpenCV
            cv2.imshow('RS Video Feed', cv_image)
            cv2.waitKey(1)

        except Exception as e:
            self.get_logger().error('Error in video node')

def main(args=None):
    rclpy.init(args=args)
    video_display = VideoDisplay()
    rclpy.spin(video_display)
    video_display.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
