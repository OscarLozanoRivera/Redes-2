#!/usr/bin/env python3

import socket

HOST = "192.168.0.17"  # El hostname o la IP del servidor
PORT = 65432  # El puerto que usa el servidor
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print("Enviando mensaje...")
    TCPClientSocket.sendall(b"Hello TCP server")
    print("Esperando una respuesta...")
    data = TCPClientSocket.recv(buffer_size)
    print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())






    #                   192.168.0.17
    #                       65432




    #------------------------------
    #Falta poner las cruces y validar que aún haya espacio