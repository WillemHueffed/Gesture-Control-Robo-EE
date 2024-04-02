import socket
import json
import time
from interbotix_xs_modules.xs_robot.locobot import InterbotixLocobotXS

def main():
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to port 12345 (creative I know) 
    server_address = ('localhost', 12345)  # Change to the desired IP address and port number
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)

    print("Waiting for a connection...")
    connection, client_address = server_socket.accept()

    # Initialize the Locobot
    locobot = InterbotixLocobotXS(
        robot_model='locobot_wx250s',
        arm_model='mobile_wx250s'
    )

    try:
        print("Connection established with:", client_address)
        while True:
            # Receive data from the client
            data = connection.recv(1024)
            if data:
                # BUG - works the first time then the socket buffer becomes backed up
                # the json loader doesn't like reading in multiple messages at once
                # -> need to add some kind of input processing
                data = data.decode()
                extracted_data = json.loads(data)
                print(extracted_data)

                # Extract the goal position from the JSON message
                goal_x = extracted_data['x']
                y = extracted_data['y']
                goal_z = extracted_data['z']

                # Command the arm to the desired position
                # This may fail if the goal coordinates are invalid
                # TODO: Z is implemented through base rotation not cartesian translation
                # -> convert to a call to rotate() method.
                locobot.arm.set_ee_pose_components(x=goal_x, z=goal_z)

                # Sleep the process for 5 seconds to demonstrate where the arm moved to
                time.sleep(5)

                # Go back to the arm's sleep pose
                # -> ensures arm ends in a safe position
                locobot.arm.go_to_sleep_pose()
    finally:
        # Clean up the connection
        connection.close()
        server_socket.close()

if __name__ == '__main__':
    main()
