# This web browser connects to my_server

import socket

def browse_localhost():

    my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    my_socket.connect(('localhost',9000))
    cmd = 'GET http://localhost:9000 HTTP/1.0\r\n\r\n'.encode()
    my_socket.send(cmd)

    while True:
        data = my_socket.recv(512)
        if len(data) < 1:
            break
        print(data.decode(), end=' ')

    my_socket.close()