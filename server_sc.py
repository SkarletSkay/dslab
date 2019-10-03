#!/usr/bin/env python3
import os
import socket
import sys

HOST = '127.0.0.1'
PORT = int(sys.argv[1])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)

        data = conn.recv(1024)
        n = 0
        if "copy_" + data.decode():
            n = 1
        while True:
            if os.path.exists("copy_" + str(n) + "_" + data.decode()):
                n = n + 1
            else:
                break
        if n == 0:
            file = open("copy_" + data.decode(), 'wb')
        else:
            file = open("copy_" + str(n) + "_" + data.decode(), 'wb')
        conn.sendall(data)
        d = conn.recv(8)
        m = int.from_bytes(d, byteorder='big')
        conn.sendall(d)
        chunk_num = int(m / 1024)
        for i in range(chunk_num):
            d = conn.recv(1024)
            file.write(d)
            conn.sendall(d)
            print(str(int((i * 1024*100) / m)) + "%")

        d = conn.recv(1024)
        file.write(d)
        conn.sendall(d)
        print("100% DONE")
        file.close()
        conn.close()
