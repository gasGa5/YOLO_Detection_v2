import socket
import os
import subprocess
import threading

class SocketServer():
    def __init__(self):
        self.host = '192.168.1.146'  # Server IP address
        self.port = 8888  # Port number
        self.server_socket = None
        self.client_socket = None
        self.addr = None
        
    def Open_TCP_server(self,) -> None:
        print('start TCP server')
        command = f"libcamera-vid -n -t 0 --width {self.frame_width} --height {self.frame_height} --framerate {self.framerate} --inline --listen -o {self.tcp_path}"
        subprocess.call(command, shell=True)
    
    def handle_client(self):
        while True:
            # Receive data from the client
            data = self.client_socket.recv(1024)
            if not data:
                break

            # Print the received data
            print('Received data:', data.decode())

            # Check if the received data is 'q'
            if data.decode().strip() == 'q':
                # Call your specific function here
                tcp_thread = threading.Thread(target=self.Open_TCP_server)
                tcp_thread.start()

            # Send a response to the client
            self.client_socket.sendall('Done.'.encode())

        self.client_socket.close()
        print('Connection with the client has been terminated:', self.addr)
        self.server_socket.close()
        print('Server is shutting down')
        self.release_port()
        self.restart_server()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)  # Maximum number of waiting clients
        print('Server has started.')
        while True:
            self.client_socket, self.addr = self.server_socket.accept()
            print('Client has connected:', self.addr)
            self.handle_client()

    def restart_server(self):
        # Function to restart the server after it's shut down
        print('Restarting the server')
        self.start_server()

    def release_port(self):
        command = f"lsof -ti:{self.port} | xargs kill"
        os.system(command)

if __name__ == '__main__':
    socket_server = SocketServer()
    socket_server.start_server()
