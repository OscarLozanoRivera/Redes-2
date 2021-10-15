# !/usr/bin/env python3

import logging
import queue
import socket
import threading
import pickle
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

def alwaysOn(socketTcp,listaConexiones,barrier,lock):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            logging.debug("Contectado a %s",client_addr)
            listaConexiones.append(client_conn)
            thread_read = threading.Thread(target=recibirMandarDatos, args=([client_conn, client_addr],(barrier,lock)))
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def gestion_conexiones(listaConexiones):
    for conn in listaConexiones:
        if conn.fileno() == -1:
            listaConexiones.remove(conn)
    logging.debug("Hilos activos: %d",threading.active_count())
    #mensaje="enum", threading.enumerate()
    #logging.debug(mensaje)
    #mensaje="conexiones: ", len(listaConexiones)
    #logging.debug(mensaje)


def recibirMandarDatos(conexion,multithread):
    global turno
    lock=multithread[1]
    multithread[0].wait()
    logging.debug("Superó la barrera")
    try:
        while True:
            while True:
                lock.acquire()
                logging.debug("TRATANDO,Turno %s,%s,%s",turno,listaConexiones[turno],conexion[0])
                if listaConexiones[turno]==conexion[0]:
                    logging.debug("Entró")
                    if turno==3:
                        turno=0 
                    else:
                        turno=turno+1
                    break
                else:
                    lock.release()
                    time.sleep(2) 
            logging.debug("Recibiendo datos del cliente %s",conexion[1])
            data = conexion[0].recv(1024)
            data=pickle.loads(data)
            logging.debug("Se leyó: %s",data)
            if not data:
                logging.debug("Fin de %s",conexion[1])
                break
            conexion[0].sendall(pickle.dumps(data))
            lock.release()
            time.sleep(0.1)

    except Exception as e:
        print(e)
        lock.release()
    finally:
        conexion[0].close()
        lock.release()




if __name__ == "__main__":
    listaConexiones=[]
    #host, port, numConn = sys.argv[1:4]
    HOST="127.0.0.1"
    PORT=12345
    NUMCON=4
    NUM_THREADS = 4
    turno=0
    barrier = threading.Barrier(NUM_THREADS)
    lock = threading.Lock()
    serveraddr = (HOST, int(PORT))
    

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPServerSocket.bind(serveraddr)
        TCPServerSocket.listen(int(NUMCON))
        logging.debug("El servidor TCP está disponible y en espera de solicitudes")

        alwaysOn(TCPServerSocket,listaConexiones,barrier,lock)
