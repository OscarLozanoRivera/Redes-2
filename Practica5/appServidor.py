# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"

import logging, grpc, distribuidos_pb2, distribuidos_pb2_grpc
import re
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
usuarioLectura = None
archivoLectura = None
lock = Lock()                    

class Archivos(distribuidos_pb2_grpc.ArchivosServicer):

    def logging(self, request, context):
        global usuarios
        #Respuestas: -1 No existe usuario 0 Contraseña incorrecta  1 Acceso concedido
        for us in usuarios:
            if request.usuario == us:
                if request.contrasena == usuarios[us]:
                    return distribuidos_pb2.respuesta(estado=1)
                return distribuidos_pb2.respuesta(estado=0)            
        return distribuidos_pb2.respuesta(estado=-1)

    def create(self, request, context):
        try:
            with open(raiz+carpetaActual[request.usuario]+request.nombreArchivo, 'r') as f:
                print("Ya existe el archivo")
                return distribuidos_pb2.respuesta(estado=0)
        except FileNotFoundError:
            file = open(raiz+carpetaActual[request.usuario]+request.nombreArchivo, "w")
            file.close()
            print("Archivo creado correctamente")
            return distribuidos_pb2.respuesta(estado=1)
        except IOError:
            print("No se pudo crear el archivo")
            return distribuidos_pb2.respuesta(estado=-1)

    def preread(self, request, context):
        try:
            with open(raiz+carpetaActual[request.usuario]+request.nombreArchivo, 'r'):
                print("Si existe el archivo")
                return distribuidos_pb2.respuesta(estado=1)
        except FileNotFoundError:
            print("No existe el archivo")
            return distribuidos_pb2.respuesta(estado=0)
        except IOError:
            print("No se pudo abrir el archivo")
            return distribuidos_pb2.respuesta(estado=-1)

    def read(self, request, context):
        print("Solicitud")
        try:
            with open(raiz+carpetaActual[request.usuario]+request.nombreArchivo, 'r') as archivo:
                for line in archivo.readlines():
                    yield distribuidos_pb2.peticionDatos(datos=line)
        except:
            print("Error al leer el archivo")

    def prewrite(self, request, context):
        print("Solicitar prewrite")
        global usuarioLectura
        global archivoLectura
        lock.acquire()
        try:
            with open(raiz+carpetaActual[request.usuario]+request.nombreArchivo, 'r'):
                print("Si existe el archivo")
                usuarioLectura=request.usuario
                archivoLectura=request.nombreArchivo
            return distribuidos_pb2.respuesta(estado=1)
        except FileNotFoundError:
            print("No existe el archivo")
            lock.release()
            return distribuidos_pb2.respuesta(estado=0)
        except IOError:
            print("No se pudo abrir el archivo")
            lock.release()
            return distribuidos_pb2.respuesta(estado=-1)

    def write(self, request_iterator, context):
        print("Solicitar write")
        global usuarioLectura
        global archivoLectura
        try:
            with open(raiz+carpetaActual[usuarioLectura]+archivoLectura, 'a') as archivo:
                for request in request_iterator:
                    archivo.write(request.datos+"\n")
            print("Se escribió correctamente")        
            return distribuidos_pb2.respuesta(estado=1)
        except FileNotFoundError:
            print("No existe el archivo")
            return distribuidos_pb2.respuesta(estado=0)
        except:
            print("No se pudo escribir el archivo")
            return distribuidos_pb2.respuesta(estado=-1)
        finally:
            lock.release()

    def rename(self, request, context):
        try:
            os.rename(raiz+carpetaActual[request.usuario]+request.nombreArchivo, raiz+carpetaActual[request.usuario]+request.nombreNuevoArchivo)
            return distribuidos_pb2.respuesta(estado=1)
        except FileNotFoundError:
            print("No existe el archivo")
            return distribuidos_pb2.respuesta(estado=0)
        except IOError:
            print("Ya existe un archivo con ese nombre")
            return distribuidos_pb2.respuesta(estado=-1)
        except Exception:
            print("No se pudo crear")
            return distribuidos_pb2.respuesta(estado=-2)

    def remove(self, request, context):
        try:
            os.remove(raiz+carpetaActual[request.usuario]+request.nombreArchivo)
            print("Se eliminó el archivo satisfactoriamente")
            return distribuidos_pb2.respuesta(estado=1)
        except FileNotFoundError:
            print("No existe el archivo que se quiere eliminar")
            return distribuidos_pb2.respuesta(estado=0)
        except Exception:
            print("No se pudo eliminar")
            return distribuidos_pb2.respuesta(estado=-1)

    def mkdir(self, request, context):
        try:
            os.makedirs(raiz+carpetaActual[request.usuario]+request.nombreArchivo)
            return distribuidos_pb2.respuesta(estado=1)
        except FileExistsError as e:
            print("El directorio ya existe")
            return distribuidos_pb2.respuesta(estado=0)
        except :
            print("No se pudo crear el directorio")
            return distribuidos_pb2.respuesta(estado=-1)

    def rmdir(self, request, context):
        try:
            os.rmdir(raiz+carpetaActual[request.usuario]+request.nombreArchivo)
            print("La carpeta se eliminó correctamente")
            return distribuidos_pb2.respuesta(estado=1)
        except FileNotFoundError as e:
            print("La carpeta no existe")
            return distribuidos_pb2.respuesta(estado=0)
        except :
            print("No se pudo eliminar la carpeta")
            return distribuidos_pb2.respuesta(estado=-1)

    def readdir(self, request, context):
        archivo= os.listdir(raiz+carpetaActual[request.usuario])
        for arch in archivo:
            yield distribuidos_pb2.lista(nombre=arch,
                                            isArchivo=  not os.path.isdir(os.path.join(raiz, carpetaActual[request.usuario],arch))  )

    def cd(self, request, context):
        global carpetaActual
        if request.nombreArchivo=="..":
            if carpetaActual[request.usuario]==request.usuario+"/":
                print("No se puede retroceder más")
                return distribuidos_pb2.respuesta(estado=-1)
            else:
                carpetas=carpetaActual[request.usuario].split("/")
                carpetas.pop(-1)
                carpetas.pop(-1)
                carpetaActual[request.usuario]=""
                for carpeta in carpetas:
                    carpetaActual[request.usuario]=carpetaActual[request.usuario]+carpeta+"/"
                print("Nueva ubicación actual:",carpetaActual[request.usuario])
                return distribuidos_pb2.respuesta(estado=1)

        carpetas= os.listdir(raiz+carpetaActual[request.usuario])
        for carpeta in carpetas:
            if os.path.isdir(os.path.join(raiz, carpetaActual[request.usuario],carpeta)):
                if carpeta==request.nombreArchivo:
                    carpetaActual[request.usuario]+=request.nombreArchivo+"/"
                    print("Nueva ubicación actual:",carpetaActual[request.usuario])
                    return distribuidos_pb2.respuesta(estado=1)
        print("No se pudo mover la ubicación actual:")
        return distribuidos_pb2.respuesta(estado=0)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    distribuidos_pb2_grpc.add_ArchivosServicer_to_server(Archivos(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.debug("Sistema de Archivos Distribuidos")
    logging.debug("Servidor RPC Activo")
    serve()

