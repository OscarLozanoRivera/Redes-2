# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"

import logging, grpc, distribuidos_pb2, distribuidos_pb2_grpc,shutil
from threading import Lock
import os
from tkinter import EXCEPTION
from tkinter.constants import E
from concurrent import futures


logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)

usuarios={
    "Admin" : "passadmin",
    "user1" : "contra1",
    "user2" : "contra2",
    "user3" : "contra3",
}
raiz="Practica5/Archivos/"
carpetaActual={
    "Admin" : "Admin/",
    "user1" : "user1/",
    "user2" : "user2/",
    "user3" : "user3/",
}
usuarioEscritura = None
archivoEscritura = None
opcionEscritura = None
lock = Lock()                    

class Archivos(distribuidos_pb2_grpc.ArchivosServicer):

    def logging(self, request, context):
        logging.debug("%s solicitó el servicio iniciar sesión",request.usuario)
        global usuarios
        #Respuestas: -1 No existe usuario 0 Contraseña incorrecta  1 Acceso concedido
        for us in usuarios:
            if request.usuario == us:
                if request.contrasena == usuarios[us]:
                    logging.debug("%s inició sesión",request.usuario)
                    return distribuidos_pb2.respuesta(estado=1)
                logging.debug("Contraseña incorrecta de %s",request.usuario)
                return distribuidos_pb2.respuesta(estado=0)            
        return distribuidos_pb2.respuesta(estado=-1)

    def create(self, request, context):
        logging.debug("%s solicitó el servicio create",request.usuario)
        try:
            with open(raiz+carpetaActual[request.usuario]+request.nombreArchivo, 'r') as f:
                logging.debug("Ya existe el archivo")
                return distribuidos_pb2.respuesta(estado=0)
        except FileNotFoundError:
            file = open(raiz+carpetaActual[request.usuario]+request.nombreArchivo, "w")
            file.close()
            logging.debug("Archivo creado correctamente")
            return distribuidos_pb2.respuesta(estado=1)
        except IOError:
            logging.debug("No se pudo crear el archivo")
            return distribuidos_pb2.respuesta(estado=-1)

    def preread(self, request, context):
        try:
            with open(raiz+carpetaActual[request.usuario]+request.nombreArchivo, 'r'):  
                logging.debug("Si existe el archivo")
                return distribuidos_pb2.respuesta(estado=1)
        except FileNotFoundError:
            logging.debug("No existe el archivo")
            return distribuidos_pb2.respuesta(estado=0)
        except IOError:
            logging.debug("No se pudo abrir el archivo")
            return distribuidos_pb2.respuesta(estado=-1)

    def read(self, request, context):
        logging.debug("%s solicitó el servicio read",request.usuario)
        try:
            with open(raiz+carpetaActual[request.usuario]+request.nombreArchivo, 'r') as archivo:
                for line in archivo.readlines():
                    yield distribuidos_pb2.peticionDatos(datos=line)
        except:
            logging.debug("Error al leer el archivo")

    def prewrite(self, request, context):
        logging.debug("%s solicitó el servicio write",request.usuario)
        global usuarioEscritura
        global archivoEscritura
        global opcionEscritura
        lock.acquire()
        try:
            with open(raiz+carpetaActual[request.usuario]+request.nombreArchivo, 'r'):
                logging.debug("Si existe el archivo")
                usuarioEscritura=request.usuario
                archivoEscritura=request.nombreArchivo
                opcionEscritura=request.opcionEscritura
            return distribuidos_pb2.respuesta(estado=1)
        except FileNotFoundError:
            logging.debug("No existe el archivo")
            lock.release()
            return distribuidos_pb2.respuesta(estado=0)
        except IOError:
            logging.debug("No se pudo abrir el archivo")
            lock.release()
            return distribuidos_pb2.respuesta(estado=-1)

    def write(self, request_iterator, context):
        global usuarioEscritura
        global archivoEscritura
        try:
            with open(raiz+carpetaActual[usuarioEscritura]+archivoEscritura, opcionEscritura) as archivo:
                for request in request_iterator:
                    archivo.write(request.datos)
            logging.debug("Se escribió correctamente")        
            return distribuidos_pb2.respuesta(estado=1)
        except FileNotFoundError:
            logging.debug("No existe el archivo")
            return distribuidos_pb2.respuesta(estado=0)
        except:
            logging.debug("No se pudo escribir el archivo")
            return distribuidos_pb2.respuesta(estado=-1)
        finally:
            lock.release()

    def rename(self, request, context):
        logging.debug("%s solicitó el servicio rename",request.usuario)
        try:
            os.rename(raiz+carpetaActual[request.usuario]+request.nombreArchivo, raiz+carpetaActual[request.usuario]+request.nombreNuevoArchivo)
            logging.debug("Archivo renombrado satisfactoriamente")
            return distribuidos_pb2.respuesta(estado=1)
        except FileNotFoundError:
            logging.debug("No existe el archivo")
            return distribuidos_pb2.respuesta(estado=0)
        except IOError:
            logging.debug("Ya existe un archivo con ese nombre")
            return distribuidos_pb2.respuesta(estado=-1)
        except Exception:
            logging.debug("No se pudo crear")
            return distribuidos_pb2.respuesta(estado=-2)

    def remove(self, request, context):
        logging.debug("%s solicitó el servicio remove",request.usuario)
        try:
            os.remove(raiz+carpetaActual[request.usuario]+request.nombreArchivo)
            logging.debug("Se eliminó el archivo satisfactoriamente")
            return distribuidos_pb2.respuesta(estado=1)
        except FileNotFoundError:
            logging.debug("No existe el archivo que se quiere eliminar")
            return distribuidos_pb2.respuesta(estado=0)
        except Exception:
            logging.debug("No se pudo eliminar")
            return distribuidos_pb2.respuesta(estado=-1)

    def mkdir(self, request, context):
        logging.debug("%s solicitó el servicio mkdir",request.usuario)
        try:
            os.makedirs(raiz+carpetaActual[request.usuario]+request.nombreArchivo)
            return distribuidos_pb2.respuesta(estado=1)
        except FileExistsError as e:
            logging.debug("El directorio ya existe")
            return distribuidos_pb2.respuesta(estado=0)
        except :
            logging.debug("No se pudo crear el directorio")
            return distribuidos_pb2.respuesta(estado=-1)

    def rmdir(self, request, context):
        logging.debug("%s solicitó el servicio rmdir",request.usuario)
        try:
            shutil.rmtree(raiz+carpetaActual[request.usuario]+request.nombreArchivo)
            logging.debug("La carpeta se eliminó correctamente")
            return distribuidos_pb2.respuesta(estado=1)
        except FileNotFoundError as e:
            logging.debug("La carpeta no existe")
            return distribuidos_pb2.respuesta(estado=0)
        except :
            logging.debug("No se pudo eliminar la carpeta")
            return distribuidos_pb2.respuesta(estado=-1)

    def readdir(self, request, context):
        logging.debug("%s solicitó el servicio readdir",request.usuario)
        archivo= os.listdir(raiz+carpetaActual[request.usuario])
        for arch in archivo:
            yield distribuidos_pb2.lista(nombre=arch,
                                            isArchivo=  not os.path.isdir(os.path.join(raiz, carpetaActual[request.usuario],arch))  )

    def cd(self, request, context):
        logging.debug("%s solicitó el servicio cd",request.usuario)
        global carpetaActual
        if request.nombreArchivo=="..":
            if carpetaActual[request.usuario]==request.usuario+"/":
                logging.debug("No se puede retroceder más")
                return distribuidos_pb2.respuesta(estado=-1)
            else:
                carpetas=carpetaActual[request.usuario].split("/")
                carpetas.pop(-1)
                carpetas.pop(-1)
                carpetaActual[request.usuario]=""
                for carpeta in carpetas:
                    carpetaActual[request.usuario]=carpetaActual[request.usuario]+carpeta+"/"
                logging.debug("Nueva ubicación actual: %s",carpetaActual[request.usuario])
                return distribuidos_pb2.respuesta(estado=1)

        carpetas= os.listdir(raiz+carpetaActual[request.usuario])
        for carpeta in carpetas:
            if os.path.isdir(os.path.join(raiz, carpetaActual[request.usuario],carpeta)):
                if carpeta==request.nombreArchivo:
                    carpetaActual[request.usuario]+=request.nombreArchivo+"/"
                    logging.debug("Nueva ubicación actual: %s",carpetaActual[request.usuario])
                    return distribuidos_pb2.respuesta(estado=1)
        logging.debug("No se pudo mover la ubicación actual")
        return distribuidos_pb2.respuesta(estado=0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    distribuidos_pb2_grpc.add_ArchivosServicer_to_server(Archivos(), server)
    server.add_insecure_port('192.168.0.24:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.debug("Sistema de Archivos Distribuidos")
    logging.debug("Servidor RPC Activo")
    serve()

