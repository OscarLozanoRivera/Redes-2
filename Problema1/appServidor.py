# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"


import logging
import socket
import threading
import pickle
import time
from datetime import datetime
import queue

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

def sendData(conn):
    global estatus
    global listaConexiones
    global horaComienzo
    global horaFinalizado
    global turno
    array=[estatus,tablero,False,None]                   #Estatus,Tablero,Turno,TiempoJuegoa
    if estatus!=0:  
        array[3]=(str(horaFinalizado-horaComienzo))      #Si acabó el juego se manda el tiempo que duró el juego
        turno=1
    #   logging.debug("Se envían datos tablero")                          
    for hilo in listaConexiones:
        if hilo==conn or estatus>0:
            if turno%2==0:
                array[2]=1
            else: 
                array[2]=2  
        else:
            array[2]=0
        #logging.debug("Enviando a %s - [%s -%s -%s]",str(hilo),array[0],array[1],array[2])
        hilo.send(pickle.dumps(array))
        if estatus>0:
            turno=turno+1

#Validar que se puede tirar en la casilla
def casillaValida(posicion):
    if tablero[posicion[0]][posicion[1]]==0:
        return True
    return False

def validarJuego() -> int:
    posiblesLineas=[]
    lineas=[]
    for tab in tablero:
        lineas.append([])
    for tab in tablero:
        #Horizontales
        posiblesLineas.append(tab)
        #Verticales
        for i,val in enumerate(tab):
            lineas[i].append(val)
    lineas.append([])
    lineas.append([])
    #Cruces
    for a in range(0,len(tablero)):
        lineas[-2].append(tablero[a][a])
        lineas[-1].append(tablero[a][len(tablero)-1-a])

    for l in lineas:
        posiblesLineas.append(l)
    ##
    # (posiblesLineas)
    #Se revisa si hay linea de k

    for pl in posiblesLineas:
        result=[]
        for item in pl:
            if item not in result:
                result.append(item)
        if len(result)==1 and 0 not in result:  #1 Gana X //  2 Gana O
            if 1 in result:
                return 2
            else:
                return 1
      
            return 0

    #Busca si aún hay espacios para jugar   // -1 No hay espacios
    i=0

    for i,tab in enumerate(tablero):
        #print(0 in tab,end="\t ")
        #print(i, len(tablero))
        if 0 in tab:
            break
        elif i==len(tablero)-1: 
            return -1
    #0 Seguir jugando
    return 0

#Modificar tablero
def actualizarTablero(posicion,valor):
    tablero[posicion[0]][posicion[1]]=valor 

def alwaysOn(socketTcp,listaConexiones,barrier,lock):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            logging.debug("Contectado a %s - %s",client_addr,client_conn)
            listaConexiones.append(client_conn)
            thread_read = threading.Thread(target=recibirMandarDatos, args=([client_conn, client_addr],(barrier,lock)))
            thread_read.start()
    except Exception as e:
        logging.debug("%s",e)

def recibirMandarDatos(conexion,multithread):
    global turno
    global horaComienzo
    global horaFinalizado
    global estatus
    barrier=multithread[0]
    lock=multithread[1]
    conn=conexion[0]
    addr=conexion[1]
    barrier.wait()
    logging.debug("Superó la barrera")
    horaComienzo=datetime.now()
    try:
        while True:
            while True:
                lock.acquire()
                #logging.debug("TRATANDO,Turno %s,%s,%s",turno,listaConexiones[turno],conn)
                if estatus!=0:
                    return
                if listaConexiones[turno]==conn:
                    #logging.debug("Entró")
                    if turno==3:
                        turno=0 
                    else:
                        turno=turno+1
                    break
                else:
                    lock.release()
                    time.sleep(.1) 
            sendData(conexion[0])
            logging.debug("Recibiendo datos del cliente %s",addr)
            data = conn.recv(BUFFERSIZE)
            if not data:
                logging.debug("Fin de %s",addr)
                break
            posicion=pickle.loads(data)
            logging.debug("Se leyó: %s",posicion)           #No es necesario validar casilla marcada
            actualizarTablero(posicion,2) if turno%2==0 else actualizarTablero(posicion,1)
            estatus=validarJuego()
            if estatus == 0:
                    sendData(conn)                #regresa Tablero
            else:
                logging.debug("El juego terminó")
                # Se toma la hora de finalizado
                horaFinalizado=datetime.now()
                #regresarNuevoTablero   //  Con Status actualizado
                sendData(conn)    
                lock.release()
                return
            lock.release()
            time.sleep(0.1)

    except Exception as e:
        logging.debug("%s",e)
        lock.release()
    finally:
        conn.close()
        #lock.release()

if __name__ == "__main__":
    listaConexiones=[]
    HOST="192.168.0.15"            # Direccion del servidor
    PORT=12345                  # Puerto que usa el servidor para conexión
    BUFFERSIZE=1024             # Tamaño máximo por mensaje
    NUMCON=5                    # Número máximo de conexiones
    NUM_THREADS = 4             # Número de hilos para comenzar
    turno=0                     
    horaComienzo= None
    horaFinalizado= None
    tablero=[[0,0,0],[0,0,0],[0,0,0]]       #Tablero
    estatus=0                   #0 En juego         |1 Ganador      |2 Perdedor     |-1 Empate
    barrier = threading.Barrier(NUM_THREADS)    #Barrera
    lock = threading.Lock()                     #Candado
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #Habilita que se use un puerto para multipes conexiones
        TCPServerSocket.bind((HOST, int(PORT)))
        TCPServerSocket.listen(int(NUMCON))
        logging.debug("El servidor TCP está disponible y en espera de solicitudes")
        alwaysOn(TCPServerSocket,listaConexiones,barrier,lock)
