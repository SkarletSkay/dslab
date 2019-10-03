import os
import socket
import sys

FILE_NAME = sys.argv[1]
HOST = sys.argv[2] 
PORT = int(sys.argv[3])

file = open(FILE_NAME, 'rb')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(str.encode(FILE_NAME))
    print('Send ')
    data = s.recv(1024)
    print('Received ', repr(data))

    m = os.path.getsize(FILE_NAME)
    s.sendall(m.to_bytes(8, byteorder='big', signed=True))
    print('Send ', m)
    data = s.recv(1024)
    print('Received ', repr(data))

    chunk_num = int(m/1024)
    for i in range(chunk_num):
        d = file.read(1024)
        s.send(d)
        data = s.recv(1024)
        print(str(int((i*1024*100)/m)) + "%")

    d = file.read(1024)
    s.send(d)
    data = s.recv(1024)
    print("100% DONE")
    file.close()
