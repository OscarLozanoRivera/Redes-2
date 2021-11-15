# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"

import pickle
import socket
import sys
import pathlib
import json

HOST = "127.0.0.1"  # El hostname o IP del servidor
bufferSize = 1024

PORT=int(sys.argv[1])

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    UDPServerSocket.bind((HOST, PORT))
    print("Servidor Autoritativo ",PORT," activo, esperando peticiones")
    # Listen for incoming datagrams
    while (True):
        data, address = UDPServerSocket.recvfrom(bufferSize)
        data=data.decode()
        print("Mensaje del cliente {}:{}".format(address,data))
        ipsEncontradas=[]
        buscar=[]
        directorio = pathlib.Path('Practica4/ServerAutoritativo/'+str(PORT))
        ls=[]
        for fichero in directorio.iterdir():
            ls.append(fichero.name)
        ls2=[]
        for f in ls:
            splits=f.split(".")
            ls2.append(splits[0]+"."+splits[1])
        if data in ls2:
            with open("Practica4/ServerAutoritativo/"+str(PORT)+"/"+str(data)+".json","r") as archivo:
                datos=json.load(archivo)
                for ip in datos['Master']:
                    if ip['Type']=="A":
                        ipsEncontradas.append(ip['Address'])
        print("IP's encontradas:",ipsEncontradas)
        # Enviando una respuesta al cliente
        dataToSend=pickle.dumps(ipsEncontradas)
        UDPServerSocket.sendto(dataToSend, address)
        
