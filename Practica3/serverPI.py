# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"


import logging
from os import system
import os
from re import T
import socket
import threading
import pickle
from pyftpdlib.authorizers import DummyAuthorizer


comandos={
    'USER',
    'PASS',
    'QUIT',
    'PORT',
    'RETR',
    'LIST'
}

respuestas={
    "Abriendo" : 150  , 
    "Correcto" : 200  , 
    "Nuevo" : 220  , 
    "CerrandoControl" : 221  , 
    "CerrandoDatos" : 226  , 
    "Continue" : 230  , 
    "Contraseña" : 331  , 
    "interrumpida" : 426  , 
    "Argumento" : 501  , 
    "NoComando" : 502  , 
    "NoRealizadado" : 550  
}

usuarios={
    "Admin" : "passadmin",
    "user1" : "contra1",
    "user2" : "contra2",
    "user3" : "contra3",
    "user4" : "contra4",
    "user5" : "contra5",
}


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

def revisiónSintaxis(data,length):
    if data=='USER':
        if length>1 and length<4:
            return True
    if data=='QUIT' or data=='LIST':
        if length==1:
            return True
    if data=='PASS' or data=='PORT' or data=='RETR':
        if length==2:
            return True
    return False

def revisionEstado(data,estado):
    global usuarios
    if data[0]=='USER':
        if estado['user']==None:
            return True
        else:
            return False
    if data[0]=='PASS':
        if estado['user']!=None :
            return True
        else: 
            return False
    if data[0]=='QUIT':
        if estado['user']!=None:
            return True
        else: 
            return False
    if data[0]=='LIST':
        pass
    if data[0]=='PORT':
        pass
    if data[0]=='RETR':
        pass

def proceso(data,estado):
    if data[0]=='USER':
        if data[1] in usuarios:
            logging.debug("Usario encontrado")
            estado['user']=data[1]
            if len(data)==3:
                estado['password']=data[2]
        else:
            logging.debug("Usario no encontrado")
            return False
    if data[0]=='PASS':
        estado['password']=data[1]


    return True
        
        


    pass

def alwaysOn(socketTcp,listaConexiones):
    try:
        while True:
            logging.debug("El servidor TCP está en espera de solicitudes")
            client_conn, client_addr = socketTcp.accept()
            logging.debug("Contectado a %s - %s",client_addr,client_conn)
            listaConexiones.append(client_conn)
            thread_read = threading.Thread(target=inOut, args=(client_conn, client_addr))
            thread_read.start()
    except Exception as e:
        logging.debug("%s",e)

def inOut(ClientConn,ClientAddr):
    estado={'user':None, 'password':None, 'port':None }
    with ClientConn:
        while True:
            data=ClientConn.recv(BUFFERSIZE)
            try:
                data=pickle.loads(data)
            except Exception as e:                                         #No se recibió información
                logging.debug("%s",e)
                break
            else:
                logging.debug("%s",data)
                if data[0] in comandos:
                    logging.debug("Comando Reconocido")
                    if revisiónSintaxis(data[0],len(data)):
                        logging.debug("Sintaxis Correcta")
                        #ClientConn.send(pickle.dumps([respuestas["Correcto"]]))    
                        if revisionEstado(data,estado):
                            proceso(data)
                        else:
                            ClientConn.send(pickle.dumps([respuestas["NoRealizadado"]))                           
                    else:
                        logging.debug("Sintaxis Inorrecta")
                        ClientConn.send(pickle.dumps([respuestas["Argumento"]]))    

                else:
                    logging.debug("Comando Reconocido")
                    ClientConn.send(pickle.dumps([502]))    

if __name__ == "__main__":
    listaConexiones=[]
    HOST="127.0.0.1"            # Direccion del servidor
    PORT=12345                  # Puerto que usa el servidor para conexión
    BUFFERSIZE=1024             # Tamaño máximo por mensaje
    NUMCON=5                    # Número máximo de conexiones


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #Habilita que se use un puerto para multipes conexiones
        TCPServerSocket.bind((HOST, int(PORT)))
        TCPServerSocket.listen(int(NUMCON))
        logging.debug("El servidor TCP está disponible")
        alwaysOn(TCPServerSocket,listaConexiones)
