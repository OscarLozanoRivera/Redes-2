#!/usr/bin/env python3

import socket
import random
import pickle
from tkinter.constants import FALSE
from datetime import datetime
from typing import List


#Validar que se puede tirar en la casilla
def casillaValida(posicion):
    if tablero[posicion[0]][posicion[1]]==0:
        return True
    return False
#Validar que aún no hay ganador y aún hay casillas para tirar
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
    ##print(posiblesLineas)
    #Se revisa si hay linea de k

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
        ##print(0 in tab,end="\t ")
        ##print(i, len(tablero))
        if 0 in tab:
            break
        elif i==len(tablero)-1: 
            return -1
    #0 Seguir jugando
    return 0
#Modificar tablero
def actualizarTablero(posicion,valor):
    tablero[posicion[0]][posicion[1]]=valor 
#Turno del servidor
def jugar():
    while True:
        i=random.randint(0,len(tablero)-1)
        e=random.randint(0,len(tablero)-1) 
        if casillaValida([i,e]):
            break
    actualizarTablero([i,e],2)
#SOCKET SEND
def enviarDatos():
    array=[estatus,tablero]
    if estatus!=0:  array.append(str(horaFinalizado-horaComienzo))          #Si acabó el juego se manda el tiempo que duró el juego
    print("\tSe envía un mensaje")
    Client_conn.send(pickle.dumps(array))

#main

HOST = "127.0.0.1"  # Direccion del servidor
PORT = 65432  # Puerto que usa el cliente para conexión
buffer_size = 1024
horaComienzo= None
horaFinalizado= None
tablero=[[0,0,0],[0,0,0],[0,0,0]]
estatus=0           #0 En juego         |1 Ganador      |2 Perdedor     |-1 Empate

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:              #Socket.socket      &       Socket.close
    print("Se creo un socket")
    TCPServerSocket.bind((HOST, PORT))
    print("Se estableción IP y Puerto")
    #Escuchando
    TCPServerSocket.listen()
    print("Servidor TCP  disponible y en espera de solicitudes")
    Client_conn, Client_addr = TCPServerSocket.accept()
    print("Conexión nueva aceptada")
    with Client_conn:               #Inicia conexión
        print("Conectado a", Client_addr)
        while True:         #Se mantiene conexión    
            while True:     #print("Esperando a recibir datos para dificultad... ")
                data = Client_conn.recv(buffer_size)            #print ("Recibido,", data,"   de ", Client_addr)
                print("\tSe recibió un mensaje")
                try:
                    data=pickle.loads(data)
                except:                                         #No se recibió información
                    Client_conn.send(b"No se recibio dificultad")    
                    TCPServerSocket.close()
                    break
                #    0 = Principiante               1 = Avanzado -> Añadir dos 
                if data==0: 
                    tablero=[[0 for x in range(0,3)] for y in range(0,3)]
                else:
                    tablero=[[0 for x in range(0,5)] for y in range(0,5)]
                #   Convirtiendo datos y mandandolos   //  Se toma la hora de inicio
                horaComienzo=datetime.now()
                enviarDatos()       #print("Enviando respuesta a", Client_addr)
                break
                   
            
            while True:     #Recibe los intentos de gato
                #print("Esperando a recibir datos para jugar... ")
                data = Client_conn.recv(buffer_size)
                print("\tSe recibió un mensaje")
                posicion=pickle.loads(data)
                #print("Data recibida ", posicion)
                if casillaValida(posicion):
                    actualizarTablero(posicion,1)
                    estatus=validarJuego()
                    if estatus == 0:
                        jugar()                         #El servidor realiza su jugada
                        estatus=validarJuego()
                        if estatus==0:
                            enviarDatos()                #regresa Tablero
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

            #Continua o termina el juego
            #print("Esperando a recibir continuación... ")

            data = Client_conn.recv(buffer_size)
            continuar=pickle.loads(data)
            if continuar==-1:       #print("No continua el juego")
                break
            else:               #print("Sigue el juego")
                estatus=0
                for tab in tablero:
                    for i,a in enumerate(tab):
                        tab[i]=0
                enviarDatos()





                
                

                


