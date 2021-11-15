# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"

import pathlib
import pickle
import socket

HOST = "192.168.0.17"  # El hostname o IP del servidor
PORT = 54321  # El puerto que usa el servidor
bufferSize = 1024

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    UDPServerSocket.bind((HOST, PORT))
    print("Servidor Raiz activo, esperando peticiones")
    # Listen for incoming datagrams
    while (True):
        data, address = UDPServerSocket.recvfrom(bufferSize)
        data=data.decode()
        print("Mensaje del cliente {}:   {}".format(address,data))
        tld=data.split('.') #Top Level Domain
        servidoresTLD=[]
        buscar=[]
        with open("Practica4/ServerRoot/rootTDLs.txt","r") as archivo:
            for linea in archivo:
                ln=linea.split(" ")
                if ln[0][:-1]==tld[1] and ln[3]=='NS':
                    buscar.append(ln[4][:-2])
        with open("Practica4/ServerRoot/rootTDLs.txt","r") as archivo:
            for linea in archivo:
                ln=linea.split(" ")
                if ln[3]=='A' and ln[0][:-1] in buscar:
                    servidoresTLD.append(ln[4])
        print("Servidores TDL encontrados:",servidoresTLD)
        # Enviando una respuesta al cliente
        dataToSend=pickle.dumps(servidoresTLD)
        UDPServerSocket.sendto(dataToSend, address)
