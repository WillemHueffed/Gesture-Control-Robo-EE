import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
import time
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyrealsense2 as rs
from std_msgs.msg import String
from sensor_msgs.msg import Image

class GestureRecognitionNode(Node):
    def __init__(self):
        super().__init__('camera_feed')
        # Start RealSense pipeline
        self.pipeline = rs.pipeline()
        self.pipeline.start()
        
        self.prev_timestamp_ms = 0

        # Create publisher for recognized gesture
        self.publisher_ = self.create_publisher(Image, 'rs_camera_feed', 10)

        self.timestamp_publisher = self.create_publisher(String, 'frame_timestamp', 10)

        # The CvBridge allows OpenCv data to be sent via ROS2 Interfaces
        self.bridge = CvBridge()

    def run(self):
        while True:
            # Wait for a coherent pair of frames: depth and color
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            color_frame_data = np.array(color_frame.get_data(), dtype=np.uint8)

            # Current timestamp in milliseconds
            frame_timestamp_ms = int(time.time() * 1000)  

            if frame_timestamp_ms <= self.prev_timestamp_ms:
                # If current timestamp is not greater than previous, skip processing
                continue

            # Update previous timestamp
            self.prev_timestamp_ms = frame_timestamp_ms  

            # Switch image color channel encoding
            img_msg = self.bridge.cv2_to_imgmsg(color_frame_data, encoding='bgr8')

            # Publish messages
            self.publisher_.publish(img_msg)
            msg = String()
            msg.data = str(frame_timestamp_ms)
            self.timestamp_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    gesture_recognition_node = GestureRecognitionNode()
    gesture_recognition_node.run()
    rclpy.spin(gesture_recognition_node)
    gesture_recognition_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
