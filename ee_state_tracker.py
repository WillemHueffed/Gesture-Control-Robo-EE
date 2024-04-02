import rclpy
import json
from rclpy.node import Node
from gesture_interfaces.msg import Pose
import socket
import time

class SocketPublisher(Node):
    def __init__(self):
        super().__init__('socket_publisher')

        # Create a publisher to publish messages
        # This listens to the the gesture command topic, then uses the callback function to update its internal
        # end effector goal state and then publish that shate if msg.reset is True
        self.subscriber = self.create_subscription(Pose, 'gesture_cmd', self.publish_data, 10)

        # Create a socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_address = ('localhost', 12345)
        self.client_socket.connect(self.client_address)

        # Store end effector desired location as state variables
        self.x = 0
        self.y = 0
        self.z = 0

    def publish_data(self, msg):
        # Publish the message
        self.x += msg.x
        self.y += msg.y
        self.z += msg.z

        # Print the output to the console -> user needs to know this so they can determine what the current goal state is
        print("heard {}, {}, {} | state: {}, {}, {}".format(msg.x, msg.y, msg.z, self.x, self.y, self.z))
        
        # msg.reset is a vistigial name -> should be msg.execute
        if msg.reset:
            # The message needs to be serialzed since we're using a port -> Encode in JSON
            j_msg = {'x' : self.x,
                     'y' : self.y,
                     'z' : self.z,
                     'reset' : True
                    }
            json_msg = json.dumps(j_msg)
            print(json_msg)
            
            #send the JSON message over the port (localhost:12345)
            self.client_socket.sendall(json_msg.encode())

        # This time.sleep() affects how quickly the end effector state is updated
        # Lower it if you don't like having to hold a pose for long periods of time to
        # achieve a desired EE goal position
        time.sleep(0.75)


def main(args=None):
    rclpy.init(args=args)
    socket_publisher = SocketPublisher()
    rclpy.spin(socket_publisher)
    socket_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

