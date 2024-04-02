'''
THIS NODE IS NONFUNCTIONAL - NOT IN USE

I'm keeping this node as an archive for future work. Currently the end effector state tracking is handled in the ee_state_tracker.py script in the root of the git repo.
This code generated a simple GUI using TKinter which would attempted to display the EE state coordinates. I was not able to get it to read the coordinates
in realtime however because the TKinter mainloop() is a blocking call meaning that it was preventing the node listenter callback from occuring.
'''
import rclpy
from rclpy.node import Node
from gesture_interfaces.msg import Pose
import tkinter as tk
from tkinter import *
from tkinter import ttk
import math
from interbotix_xs_modules.xs_robot.locobot import InterbotixLocobotXS
import threading
import multiprocessing
import socket


class EEStateTracker(Node):
    def __init__(self):
        super().__init__('ee_state_tracker')
        #self.root = tk.Tk()
        #self.root.title("EE State Tracker")

        #self.frm = ttk.Frame(self.root, padding=10)
        #self.frm.grid(row=0, column=0, padx=10, pady=10)

        # Label title
        #ttk.Label(self.frm, text="EE State Tracker", font=("Arial", 16)).grid(column=0, row=0, columnspan=2)

        # Button to update value
        #update_button = ttk.Button(self.frm, text="Update Value", command=self.update_value)
        #update_button.grid(row=2, column=3, columnspan=2, pady=10)

        # Label to display value
        #self.value_label_x = ttk.Label(self.frm, text='X: ', font=('Arial', 24))
        #self.value_label_x.grid(row=1, column=0, columnspan=2, pady=10)

        #self.value_label_y = ttk.Label(self.frm, text='Y: ', font=('Arial', 24))
        #self.value_label_z = ttk.Label(self.frm, text='Z: ', font=('Arial', 24))

        #self.value_label_y.grid(row=2, column=0, columnspan=2, pady=10)
        #self.value_label_z.grid(row=3, column=0, columnspan=2, pady=10)

        # Set an initial value
        #self.x = tk.DoubleVar()
        #self.x.set(0.0)
        #self.y = tk.DoubleVar()
        #self.y.set(0.0)
        #self.z = tk.DoubleVar()
        #self.z.set(0.0)

        #self.locobot = LocobotThread()
        #self.locobot = LocobotProcess()
        #self.locobot.start()
        #self.locobot.join()


        self.x = 0
        self.y = 0
        self.z = 0


        '''
        self.get_logger().info("Creating socket server")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 12345)
        self.server_socket.connect(self.server_address)
        '''
        # Subscribe to pose command topic
        self.subscriber = self.create_subscription(Pose, 'gesture_cmd', self.listener_callback, 10)
        self.publisher = self.create_publisher(Pose, 'cmd_pose', 10)
        self.get_logger().info("PUBLISHER CREATED")
        #self.publisher = self.create_publisher(Pose, 'cmd_pose', 10)

        # Window while true loop
        #self.root.mainloop()


    #def update_value(self):
        #self.value_label_x.config(text='X: {}'.format(self.x)
        #self.value_label_y.config(text='Y: {}'.format(self.y)
        #self.value_label_z.config(text='Z: {}'.format(self.z)
    

    def listener_callback(self, msg):
        #self.x.set(self.x.get() + msg.x)
        #self.y.set(self.y.get() + msg.y)
        #self.z.set(self.z.get() + msg.z)
        self.x += msg.x
        self.y += msg.y
        self.z += msg.z

        self.get_logger().info("command: {}, {}, {}".format(self.x, self.y, self.z))

        if msg.reset == True:
            self.get_logger().info('Publishing execution command')
            pose_msg = Pose()
            pose_msg.x = self.x
            pose_msg.y = self.y
            pose_msg.z = self.z
            self.publisher.publish(pose_msg)
            #self.locobot.arm.set_ee_pose_components(x=self.x, y=self.y, z=self.z)
            data = '{}, {}, {}'.format(self.x, self.y, self.z)
            self.conection.sendall(data.encode())
        
            
        # Not implemented
        x_rotation = msg.x_rotation
        y_rotation = msg.y_rotation
        z_rotation = msg.z_rotation

        #self.update_value()

    def run(self):
        # Placeholder for main loop
        self.get_logger().info("EE State Tracker running...")
        self.get_logger().warn("This is a placeholder main loop.")

def main(args=None):
    rclpy.init(args=args)
    ee_state_tracker_node = EEStateTracker()
    rclpy.spin(ee_state_tracker_node)
    ee_state_tracker_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
