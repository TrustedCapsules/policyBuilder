# used for connecting to the trusted capsule server
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 4000
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"


def connect(ip: str, port: int, request: bytes):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(request)
    print("sent")
    data = s.recv(BUFFER_SIZE)
    s.close()
    print("received data:", data)


connect(TCP_IP, TCP_PORT, bytes("Hello, World!", 'ascii'))
