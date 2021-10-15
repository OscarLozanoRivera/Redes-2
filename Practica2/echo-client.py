#!/usr/bin/env python3

import os
import socket
import pickle


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 12345  # The port used by the server
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    while True:
        mensaje=input("Escribe el mensaje:      ")
        TCPClientSocket.sendall(pickle.dumps([mensaje]))
        print("Esperando una respuesta...")
        while True:
            data = TCPClientSocket.recv(buffer_size)
            data=pickle.loads(data)
            if data[0]!="En espera":
                print("turno")
                break
            print(data)
        os.system("pause")