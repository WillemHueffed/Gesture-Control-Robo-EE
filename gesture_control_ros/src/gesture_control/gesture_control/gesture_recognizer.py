import rclpy
from rclpy.node import Node
import time
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

# Do configurations for the mediapipe gesture recognition object
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

class GestureRecognitionNode(Node):
    def __init__(self):
        super().__init__('gesture_recognition_node')
        self.img = None
        
        # Create a gesture recognizer instance in live stream mode
        self.options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path='/home/locobot/SU_Robotics/gesture_control_ros/src/gesture_control/gesture_control/gesture_recognizer.task'),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=self.publish_result)
        self.recognizer = GestureRecognizer.create_from_options(self.options)
        
        # Create publisher for recognized gesture
        self.publisher_ = self.create_publisher(String, 'recognized_gesture', 10)

        # Create a subscriber for camera feed
        self.subscriber_ = self.create_subscription(Image, 'rs_camera_feed', self.listener_callback, 10)

        # Create a subcription for the frame timestamp
        self.timestamp_subscirber = self.create_subscription(String, 'frame_timestamp', self.timestamp_callback, 10)

        # Create the CvBridge object which allows casting ROS2 image data into OpenCV's image format
        self.bridge = CvBridge()

    def publish_result(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        if result.gestures:
            self.get_logger().info("{}".format(result.gestures[0][0].category_name))
            msg = String()
            #Grab just the recognized gesture -> filter out the noise
            msg.data = result.gestures[0][0].category_name
            self.publisher_.publish(msg)

    def listener_callback(self, msg):
        # Do image format type casting
        img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        # Convert image into a media pipe image format
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
        self.img = mp_img
    
    def timestamp_callback(self, msg):
        if self.img:
            timestamp = int(msg.data)
            # Do gesture recognition on image
            self.recognizer.recognize_async(self.img, timestamp)

def main(args=None):
    rclpy.init(args=args)
    gesture_recognition_node = GestureRecognitionNode()
    rclpy.spin(gesture_recognition_node)
    gesture_recognition_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

