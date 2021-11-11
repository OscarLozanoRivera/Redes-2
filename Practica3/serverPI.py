# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"


import logging
import time
from re import L, T
import socket
import threading
import pickle
import pathlib



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
    "Puerto" : 201  ,
    "Nuevo" : 220  , 
    "CerrandoControl" : 221  , 
    "CerrandoDatos" : 226  , 
    "Continue" : 230  , 
    "Contraseña" : 331  , 
    "interrumpida" : 426  , 
    "noFichero" : 450 ,
    "Argumento" : 501  , 
    "NoComando" : 502  , 
    "ErrorAutenticación": 530,
    "NoRealizadado" : 550  
}

usuarios={
    "Admin" : "passadmin",
    "user1" : "contra1",
    "user2" : "contra2",
    "user3" : "contra3",
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
    if data=='PASS' or data=='PORT' :
        if length==2:
            return True
    if data=='RETR':
        if length==2 or length==3:
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
        if estado['password']==None :
            return True
        else: 
            return False
    if data[0]=='QUIT':
        if estado['user']!=None:
            return True
        else: 
            return False
    if data[0]=='LIST':
        if estado['port']!=None :
            return True
        else: 
            return False
    if data[0]=='PORT':
        if estado['port']==None :
            return True
        else: 
            return False
    if data[0]=='RETR':
        if estado['port']!=None :
            return True
        else: 
            return False

def proceso(ClientConn,ipCliente,data,estado):
    if data[0]=='USER':
        if data[1] in usuarios:
            logging.debug("Usario encontrado")
            estado['user']=data[1]
            if len(data)==3:
                if data[2] == usuarios[estado['user']]:
                    estado['password']=data[2]
                    ClientConn.send(pickle.dumps([respuestas["Continue"]]))
                else:
                    ClientConn.send(pickle.dumps([respuestas["Contraseña"]]))
            else:
                ClientConn.send(pickle.dumps([respuestas["Contraseña"]]))
            return True
        else:
            logging.debug("Usario no encontrado")
            ClientConn.send(pickle.dumps([respuestas["ErrorAutenticación"]]))
        return True
    if data[0]=='PASS':
        if data[1] == usuarios[estado['user']]:
            logging.debug("Contraseña Correcta")
            estado['password']=data[1]
            ClientConn.send(pickle.dumps([respuestas["Continue"]]))
        else:
            logging.debug("Contraseña Incorrecta")
            ClientConn.send(pickle.dumps([respuestas["ErrorAutenticación"]]))    
        return True
    if data[0]=='PORT':
        if estado['password']!=None:
            if len(data[1])<=5:
                estado['port']=data[1]
                ClientConn.send(pickle.dumps([respuestas["Puerto"]]))
            else:
                ClientConn.send(pickle.dumps([respuestas["Argumento"]]))
        else:
            ClientConn.send(pickle.dumps([respuestas["NoRealizada"]]))
    if data[0]=='QUIT':
        if estado['user']!=None:
            return False
        else: 
            ClientConn.send(pickle.dumps([respuestas["NoRealizada"]]))
            return True 
    if data[0]=='LIST':
        if estado['port']!=None:
            ClientConn.send(pickle.dumps([respuestas["Abriendo"]]))  
        else:
            ClientConn.send(pickle.dumps([respuestas["NoRealizada"]]))  
            return True
        datos=threading.Thread(target=conexionDatos,args=([ipCliente,estado],'LIST'), name="Datos")
        time.sleep(2)
        datos.start()
        datos.join()
        logging.debug("Acabó el thread")
        return True
        #Crear conexión datos
    if data[0]=='RETR':
        if estado['port']!=None:
            ls=[]
            directorio = pathlib.Path('Practica3/ServerData/'+estado['user'])
            for fichero in directorio.iterdir():
                ls.append(fichero.name)
            if not data[1] in ls :
                return False
            ClientConn.send(pickle.dumps([respuestas["Abriendo"]]))  
        else:
            ClientConn.send(pickle.dumps([respuestas["NoRealizada"]]))  
            return True
        datos=threading.Thread(target=conexionDatos, args=([ipCliente,estado,data[1]],'RETR'), name="ServidorDTP")
        time.sleep(2)
        datos.start()
        datos.join()
        #logging.debug("Acabó el thread")
        return True
        #Crear conexión datos
    
    return True

def conexionDatos(estado,listoRetr):
    global  TCPDatosSocket
    TCPDatosSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:                #print("{},{},{},{}".format(HOST,type(HOST),PORT,type(PORT)))
            HOST=estado[0]
            PORT=int(estado[1]['port'])
            logging.debug("Conectando con %s mediante el puerto: %s",HOST,PORT)
            TCPDatosSocket.connect((HOST,PORT))
    except Exception as e:
            logging.debug("%s",e)
            logging.debug("No se pudo conectar, intenta otra vez")
    else:
            logging.debug("Conexión exitosa")
    data=None

    if listoRetr=='LIST':
        time.sleep(1)
        directorio = pathlib.Path('Practica3/ServerData/'+estado[1]['user'])
        ls=[]
        for fichero in directorio.iterdir():
            ls.append(fichero.name)
        TCPDatosSocket.send(pickle.dumps(ls))
    else:
        with open("Practica3/ServerData/"+estado[1]['user']+"/"+estado[2],"r") as archivo:
            for linea in archivo:
                time.sleep(.001)
                TCPDatosSocket.send(pickle.dumps([linea]))
            #logging.debug("Fin mensajes")
        logging.debug("Se cerró archivo")
        TCPDatosSocket.send(pickle.dumps([]))
        logging.debug("Fin de envio")
    TCPDatosSocket.close()
    return

    



def alwaysOn(socketTcp,listaConexiones):
    try:
        while True:
            logging.debug("El servidor TCP está en espera de solicitudes")
            client_conn, client_addr = socketTcp.accept()
            logging.debug("Contectado a %s - %s",client_addr,client_conn)
            listaConexiones.append(client_conn)
            print(client_addr)
            thread_read = threading.Thread(target=inOut, args=(client_conn,client_addr))
            thread_read.start()
    except Exception as e:
        logging.debug("%s",e)

def inOut(ClientConn,ClienteAdr):
    estado={'user':None, 'password':None, 'port':None }
    with ClientConn:
        ClientConn.send(pickle.dumps([respuestas["Nuevo"]]))   
        while True:
            logging.debug("Esperando")
            data=ClientConn.recv(BUFFERSIZE)
            try:
                data=pickle.loads(data)
            except Exception as e:                                         #No se recibió información
                logging.debug("Errorts %s",e)
                break
            else:
                logging.debug("%s",data)
                if data[0] in comandos:
                    logging.debug("Comando Reconocido")
                    if revisiónSintaxis(data[0],len(data)):
                        logging.debug("Sintaxis Correcta")
                        #ClientConn.send(pickle.dumps([respuestas["Correcto"]]))    
                        if revisionEstado(data,estado):
                            logging.debug("Estado Corecto")
                            if not proceso(ClientConn,ClienteAdr[0],data,estado):
                                #QUIT
                                if data[0]=='QUIT':
                                    logging.debug("Quit")
                                    ClientConn.send(pickle.dumps([respuestas["CerrandoControl"]]))                               
                                    break
                                elif data[0]=='RETR' or data[0]=='LIST':
                                    ClientConn.send(pickle.dumps([respuestas["noFichero"]]))               
                            elif data[0]=='RETR' or data[0]=='LIST':
                                ClientConn.send(pickle.dumps([respuestas["CerrandoDatos"]]))               
                        else:
                            logging.debug("Error de estado")
                            if data[0]=='RETR':
                                ClientConn.send(pickle.dumps([respuestas["noFichero"]]))                           
                            else:
                                ClientConn.send(pickle.dumps([respuestas["NoRealizadado"]]))                           
                    else:
                        logging.debug("Sintaxis Inorrecta")
                        ClientConn.send(pickle.dumps([respuestas["Argumento"]]))    
                else:
                    logging.debug("Comando No Reconocido")
                    ClientConn.send(pickle.dumps([respuestas["NoComando"]]))    
    logging.debug("Cerrando Conexión Datos")
            

if __name__ == "__main__":
    listaConexiones=[]
    HOST="127.0.0.1"            # Direccion del servidor
    PORT=12345                  # Puerto que usa el servidor para conexión
    BUFFERSIZE=1024             # Tamaño máximo por mensaje
    NUMCON=5                    # Número máximo de conexiones
    TCPDatosSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #Habilita que se use un puerto para multipes conexiones
        TCPServerSocket.bind((HOST, int(PORT)))
        TCPServerSocket.listen(int(NUMCON))
        logging.debug("El servidor TCP está disponible")
        alwaysOn(TCPServerSocket,listaConexiones)
