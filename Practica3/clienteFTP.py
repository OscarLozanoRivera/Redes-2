# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"


import socket
import re
import pickle
import logging
import os
import threading



TCPClientSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
BUFFERSIZE=1024             # Tamaño máximo por mensaje
usuario=">"

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

respuestas={
    150: "Estado del fichero correcto; va a abrirse la conexión de datos",
    200: "Orden Correcta",
    201: "Puerto actualizado",
    220: "Servicio preparado para nuevo usuario",
    221: "Cerrando la conexión de control",
    226: "Cerrando la conexión de datos",
    230: "Usuario conectado, continue",
    331: "Usuario OK, necesita contraseña",
    426: "Conexión cerrada, transferencia interrumpida",
    450: "Fichero no disponible",
    500: "Error de sintáxis. Comando no reconocido",
    501: "Error de sintáxis en parámetro o argumento",
    502: "Orden no implementada / Orden no reconocida",
    530: "Error de autenticación.",
    550: "Acción no realizadada"
}

def conectar(HOST,PORT):
    try:                #print("{},{},{},{}".format(HOST,type(HOST),PORT,type(PORT)))
            PORT=int(PORT)
            #print("Conectando con {} mediante el puerto: {}".format(HOST,PORT))
            TCPClientSocket.connect((HOST,PORT))
    except Exception as e:
            print(e)
            print("No se pudo conectar, intenta otra vez.")
    else:
        #print("Conexión exitosa.")
        data=TCPClientSocket.recv(BUFFERSIZE)
        data=pickle.loads(data)
        key=data[0]
        print("\t",key, respuestas[key])



def conexionDatos(port,config):
    HOSTDatos="127.0.0.1"            # Direccion del servidor datos
    PORTDatos=port                  # Puerto que usa el servidor para conexión datos
    NUMCON=5                    # Número máximo de conexiones
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPDatosSocket:
        TCPDatosSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #Habilita que se use un puerto para multipes conexiones
        TCPDatosSocket.bind((HOSTDatos, int(PORTDatos)))
        TCPDatosSocket.listen(int(NUMCON))
        #logging.debug("El servidor Cliente DTP está disponible en el puerto: %s",PORTDatos)
        #logging.debug("El servidor Cliente DTP está en espera de solicitudes")
        client_conn, client_addr = TCPDatosSocket.accept()
        #logging.debug("Nueva conexión")
        thread_read = threading.Thread(target=entradaArchivos, args=(client_conn,config), name="Datos")
        thread_read.start()
        thread_read.join()
    #logging.debug("Finalizó with")
        
        

def entradaArchivos(TCPDatosSocket,config):
    data=None
    if config[0]:
        data=TCPDatosSocket.recv(BUFFERSIZE)
        data=pickle.loads(data)
        for a in data:
            print("- ",a)
        
    else:

        file = open("f:/Oscar/Documentos/ESCOM/7mo Semestre/Redes 2/PracticasGit/Practica3/ClientData/"+config[1],"w")
        while data!=[]:
            data=TCPDatosSocket.recv(BUFFERSIZE)
            try:
                data=pickle.loads(data)
            except Exception as e:
                logging.debug("%s",e)
                break
            else:
                for a in data:
                    file.write(a)
        file.close()
    #logging.debug("Listones")
    TCPDatosSocket.close()
    return


if __name__ == "__main__":
    PORTDatos=None
    mostrar=False
    print("|||   Terminal Cliente   |||")
    while True:
        while True:
            print(">>",end="")
            orden=input()
            if re.search(r'ftp',orden) is not None:
            #if re.search(r'ftp [0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3} [0-9]{1,5}',orden) is not None:
                #splits=re.split(r' ',orden)
                #splits[2]=int(splits[2])
                #print("Conectanding*")
                conectar("127.0.0.1",12345)
                #conectar(splits[1],splits[2])
                
                break
            else:
                print("No se reconoce comando")
            
        while True:
            print(usuario,">",end="")
            orden=input()
            splits=re.split(r' ',orden)
            TCPClientSocket.send(pickle.dumps(splits))
            data=TCPClientSocket.recv(BUFFERSIZE)
            #print(data)
            data=pickle.loads(data)
            key=data[0]
            print("\t",key, respuestas[key])
            if key==201:
                #logging.debug("%s",splits[1])
                PORTDatos=splits[1]
            if key==150:
                if splits[0]=='RETR':
                    if len(splits)==3:
                        config=[False,splits[2]]
                    else:
                        config=[False,splits[1]]
                if splits[0]=='LIST':
                    config=[True,]
                conexionDatos(PORTDatos,config)
                data=TCPClientSocket.recv(BUFFERSIZE)
                data=pickle.loads(data)
                key=data[0]
                print("\t",key, respuestas[key])
            if key==221:
                break
        TCPClientSocket.close()



    




