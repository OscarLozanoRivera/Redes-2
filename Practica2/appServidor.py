# !/usr/bin/env python3

import logging
import socket
import threading

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-40s) %(message)s',
)

def alwaysOn(socketTcp,conexionesPendientes,conexionesActivas,barrier,lock):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            mensaje="Conectado a ", client_addr
            logging.debug(mensaje)
            with lock:
                if len(conexionesActivas)==2:           
                    conexionesPendientes.append(client_conn)
                else:
                    conexionesActivas.append(client_conn)
            thread_read = threading.Thread(target=recibirMandarDatos, args=([client_conn, client_addr],barrier))
            thread_read.start()
            gestion_conexiones(conexionesActivas,conexionesPendientes)
    except Exception as e:
        print(e)

def gestion_conexiones(conexionesActivas,conexionesPendientes):
    for conn in conexionesActivas:
        if conn.fileno() == -1:
            conexionesActivas.remove(conn)
    
    mensaje="Hilos activos: ",threading.active_count()
    logging.debug(mensaje)
    mensaje="enum", threading.enumerate()
    logging.debug(mensaje)
    mensaje="conexiones: ", len(conexionesActivas)
    logging.debug(mensaje)
    print(conexionesActivas)


def recibirMandarDatos(conexion,barrier):
    worker_id = barrier.wait()
    logging.debug("Superó la barrera")
    try:
        cur_thread = threading.current_thread()
        mensaje="Recibiendo datos del cliente ",conexion[1]
        logging.debug(mensaje)
        while True:
            data = conexion[0].recv(1024)
            response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
            if not data:
                mensaje="Fin de ",conexion[1]
                logging.debug(mensaje)
                break
            conexion[0].sendall(response)
    except Exception as e:
        print(e)
    finally:
        conexion[0].close()


if __name__ == "__main__":
    conexionesPendientes = []
    conexionesActivas=[]
    #host, port, numConn = sys.argv[1:4]
    HOST="127.0.0.1"
    PORT=12345
    NUMCON=10
    NUM_THREADS = 2
    barrier = threading.Barrier(NUM_THREADS)
    lock = threading.Lock()
    """
    if len(sys.argv) != 4:
        print("usage:", sys.argv[0], "<host> <port> <num_connections>")
        sys.exit(1)
    """
    serveraddr = (HOST, int(PORT))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPServerSocket.bind(serveraddr)
        TCPServerSocket.listen(int(NUMCON))
        logging.debug("El servidor TCP está disponible y en espera de solicitudes")

        alwaysOn(TCPServerSocket,conexionesPendientes,conexionesActivas,barrier,lock)
