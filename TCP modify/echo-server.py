#!/usr/bin/env python3

import socket
import time
import random
import json
import pickle
from tkinter.constants import FALSE
from datetime import datetime
from typing import List
HOST = "192.168.0.17"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024
horaComienzo= None
horaFinalizado= None
tablero=[[0,0,0],[0,0,0],[0,0,0]]
estatus=0



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
        posiblesLineas.append(tab)
        for i,val in enumerate(tab):
            lineas[i].append(val)
    lineas.append([])
    for a in range(0,len(tablero)):
        lineas[-1].append(tablero[a][a])
    lineas.append([])
    for a in reversed(range(0,len(tablero))):
        lineas[-1].append(tablero[a][a])       
    for l in lineas:
        posiblesLineas.append(l)

    #Se revisa si hay linea de 3

    for pl in posiblesLineas:
        result=[]
        for item in pl:
            if item not in result:
                result.append(item)
        if len(result)==1 and 0 not in result:  #1 Gana Jugador //  2 Gana Servidor
            if 1 in result:
                return 1
            else:
                return 2
      
            return 0

    #Busca si aún hay espacios para jugar   // -1 No hay espacios
    i=0

    for i,tab in enumerate(tablero):
        print(0 in tab,end="\t ")
        print(i, len(tablero))
        if 0 in tab:
            break
        elif i==len(tablero)-1: 
            return -1
    #0 Seguir jugando
    return 0

def actualizarTablero(posicion,valor):
    tablero[posicion[0]][posicion[1]]=valor

def jugar():
    while True:
        i=random.randint(0,len(tablero)-1)
        e=random.randint(0,len(tablero)-1) 
        if tablero[i][e]==0:
            break
    actualizarTablero([i,e],2)

def enviarDatos():
    array=[estatus,tablero]
    if estatus!=0:  array.append(str(horaFinalizado-horaComienzo))
    Client_conn.send(pickle.dumps(array))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    #Escuchando
    TCPServerSocket.listen()
    print("El servidor TCP está disponible y en espera de solicitudes")
    Client_conn, Client_addr = TCPServerSocket.accept()
    with Client_conn:
        #Inicia conexión
        print("Conectado a", Client_addr)
        while True:
            #Recibe la dificultad
            while True:
                print("Esperando a recibir datos para dificultad... ")
                data = Client_conn.recv(buffer_size)
                if data!=None:
                    print ("Recibido,", data,"   de ", Client_addr)
                    data= data.decode('utf-8')
                    print(type(data),"   ---  ",data)
                    print("Enviando respuesta a", Client_addr)
                    #    0 = Principiante               1 = Avanzado -> Añadir dos 
                    if data != '0':
                        #Agregando row
                        for tab in tablero:
                            for a in range(0,2):
                                tab.append(0)
                        #Agregando col
                        for a in range(0,2):
                            tablero.append([0,0,0,0,0])
                    #   Convirtiendo datos y mandandolos   //  Se toma la hora de inicio
                    horaComienzo=datetime.now()
                    enviarDatos()
                    break
                else:
                    print ("Recibido,", data,"   de ", Client_addr)
                    print("Enviando respuesta a", Client_addr)
                    Client_conn.send(b"No se mando un entero")    
            #Recibe los intentos de gato
            while True:
                print("Esperando a recibir datos para jugar... ")
                data = Client_conn.recv(buffer_size)
                databArray=bytearray(data)
                posicion=list(databArray)
                print("Data recibida ", posicion)
                if casillaValida(posicion):
                    actualizarTablero(posicion,1)
                    #El servidor realiza su jugada
                    estatus=validarJuego()
                    if estatus == 0:
                        jugar()
                        estatus=validarJuego()
                        if estatus==0:
                            #regresarNuevoTablero
                            enviarDatos()
                        else:
                            # Se toma la hora de finalizado
                            horaFinalizado=datetime.now()
                            #regresarNuevoTablero   //  Con Status
                            enviarDatos()   
                            break 
                    
                    #mandar tiempo y resultado de juego
                    else:
                        # Se toma la hora de finalizado
                        horaFinalizado=datetime.now()
                        #regresarNuevoTablero   //  Con Status
                        enviarDatos()   
                        break 
                        #mandar tiempo y resultado de juego
            break


                
                

                


