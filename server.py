import socket

class Socket_server():
    def __init__(self) -> None:
        self.host = '192.168.1.121'  # 서버 IP 주소
        self.port = 8888  # 포트 번호    
        self.server_socket = None
        self.client_socket = None
        self.addr = None
    
    def handle_client(self):
        while True:
            # 클라이언트로부터 데이터 수신
            data = self.client_socket.recv(1024)
            if not data:
                break

            # 수신한 데이터 출력
            print('수신한 데이터:', data.decode())

            # 클라이언트에게 응답 전송
            self.client_socket.sendall('Done.'.encode())

        self.client_socket.close()
        print('클라이언트와의 연결이 종료되었습니다:', self.addr)
        self.server_socket.close()
        print('서버를 종료합니다')
        # if self.quit_server() is True:
            # print('서버를 종료합니다')
            # return
        # 클라이언트와의 연결이 종료되면 서버를 종료하고 다시 시작
        # else:
        self.restart_server()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)  # 최대 대기 클라이언트 수
        print('서버가 시작되었습니다.')
        while True:
            self.client_socket, self.addr = self.server_socket.accept()
            print('클라이언트가 접속하였습니다:', self.addr)
            self.handle_client()

    def restart_server(self):
        # 서버 종료 후 다시 시작하는 함수
        print('서버를 재시작합니다')
        self.start_server()

    # def quit_server(self):
    #     user_input = input('서버를 종료하시려면 "q"를 입력하세요: ')
    #     if user_input.lower() == 'q':
    #         return True
    #     elif user_input.lower() != 'q':
    #         return False

if __name__ == '__main__':
    socket_server = Socket_server()
    socket_server.start_server()
