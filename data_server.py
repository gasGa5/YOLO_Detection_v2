import socket

HOST = '192.168.1.121'  # PC의 IP 주소
PORT = 8888  # 포트 번호

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print('Server started.')

conn, addr = s.accept()
print('Client Connected.', addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print('receive data:', data.decode())
    conn.sendall('done'.encode())

conn.close()
