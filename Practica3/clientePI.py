# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"


import socket
import re
import pickle
import logging
import os

TCPClientSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
buffer_size = 128
usuario=">"

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

respuestas={
    150: "Estado del fichero correcto; va a abrirse la conexión de datos",
    200: "Orden Correcta",
    220: "Servicio preparado para nuevo usuario",
    221: "Cerrando la conexión de control",
    226: "Cerrando la conexión de datos",
    230: "Usuario conectado, continue",
    331: "Usuario OK, necesita contraseña",
    426: "Conexión cerrada, transferencia interrumpida",
    500: "Error de sintáxis. Comando no reconocido",
    501: "Error de sintáxis en parámetro o argumento",
    502: "Orden no implementada / Orden no reconocida",
    550: "Acción no realizadada"
}

def conectar(HOST,PORT):
    try:                #print("{},{},{},{}".format(HOST,type(HOST),PORT,type(PORT)))
            PORT=int(PORT)
            print("Conectando con {} mediante el puerto: {}".format(HOST,PORT))
            TCPClientSocket.connect((HOST,PORT))
    except Exception as e:
            print(e)
            print("No se pudo conectar, intenta otra vez.")
    else:
            print("Conexión exitosa.")

def controladorKeys(key):
    pass


print("|||   Terminal Cliente   |||")
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
    data=TCPClientSocket.recv(buffer_size)
    #print(data)
    data=pickle.loads(data)[0]
    key=data[0]
    print("\t",key, respuestas[key])



TCPClientSocket.close()




    




