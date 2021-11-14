# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"

import pickle
import socket

HOST = "127.0.0.1"  # El hostname o IP del servidor
PORT = 12345  # El puerto que usa el servidor
bufferSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    UDPServerSocket.bind((HOST, PORT))
    print("Servidor TDL ",PORT," activo, esperando peticiones")
    # Listen for incoming datagrams
    while (True):
        data, address = UDPServerSocket.recvfrom(bufferSize)
        data=data.decode()
        print("Mensaje del cliente {}:{}".format(address,data))
        tdl=data.split('.') #Top Domain Lever
        servidoresAutoritativos=[]
        buscar=[]
        with open("Practica4/ServerTDL/TDL-Server-Registrars MX.txt","r") as archivo:
            for linea in archivo:
                ln=linea.split(" ")
                if ln[3]=='NS':
                    buscar.append(ln[4][:-1])
        #print(buscar)
        with open("Practica4/ServerTDL/TDL-Server-Registrars MX.txt","r") as archivo:
            for linea in archivo:
                ln=linea.split(" ")
                if ln[3]=='A' and ln[0] in buscar:
                    servidoresAutoritativos.append(ln[4])
        print("Servidores autoritarios encontrados:",servidoresAutoritativos)
        # Enviando una respuesta al cliente
        dataToSend=pickle.dumps(servidoresAutoritativos)
        UDPServerSocket.sendto(dataToSend, address)
