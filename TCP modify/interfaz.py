#!/usr/bin/env python3

import pickle
from tkinter import *
import socket
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, messagebox
import tkinter
from tkinter.ttk import Frame, Label, Entry



TCPClientSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HEIGHT  = 10
WIDTH = 5

diccionario={1:"Ganador",2:"Perdedor",-1:"Empate"}

class boton:
    botonnuevo=None
    def __init__(self,posicion,texto) -> None:
        self.botonnuevo=Button(frame6,text=texto,width=5,height=3)
        self.botonnuevo.grid(row=posicion[0],column=posicion[1])
        menbArray=bytearray(posicion)
        mensajeb=bytes(menbArray)
        self.botonnuevo.config(command=lambda:mandarMensaje(mensajeb))
    def modificarBoton(self,texto) ->None:
        self.botonnuevo.config(text=texto)
        self.botonnuevo.config(state=tkinter.DISABLED)



#main

buffer_size = 1024

root = Tk()
root.geometry("400x400+300+300")
root.resizable(False,False)


root.title("Practica 1")

#Frame Conexión
frame0 = Frame(root)
frame0.pack(fill=X)

frame1 = Frame(frame0)
frame1.pack(fill=X)

lbl1 = Label(frame1, text="IP", width=8)
lbl1.pack(side=LEFT, padx=5, pady=5)

#Entrada IP
entry1 = Entry(frame1)
entry1.pack(fill=X, padx=5, expand=True)

frame2 = Frame(frame0)
frame2.pack(fill=X)

lbl2 = Label(frame2, text="Puerto", width=8)
lbl2.pack(side=LEFT, padx=5, pady=5)

#Entrada Puerto
entry2 = Entry(frame2)
entry2.pack(fill=X, padx=5, expand=True)

frame3 = Frame(frame0)
frame3.pack(fill=BOTH, expand=True)
      
#Socket CONCECT
def conectar():
    #TCPClientSocket.connect((entry1.get(),int(entry2.get())))
    TCPClientSocket.connect(("192.168.0.17",65432))
    frame0.pack_forget()
    lbl3.pack(side=TOP, padx=5, pady=5)
    button2.pack(side=LEFT, padx=5, pady=5)
    button3.pack(side=RIGHT, padx=5, pady=5)
    

#Boton Iniciar Conexión

button = Button(frame3, text="Obtener IP y Puerto",command=conectar )
button.pack(side=LEFT, padx=5, pady=5)


#Frame Dificultad

frame4 = Frame(root)
frame4.pack(fill=X)

lbl3 = Label(frame4, text="Dificultad", width=10)

#Dibujar Tablero
botones=[]
def dibujarTablero(gridGato):
    if len(botones)==0:      
        for i,a in enumerate(gridGato):
            for e,b in enumerate(a):
                botones.append(boton([i,e]," "))
    else:
        for i,a in enumerate(gridGato):
            for e,b in enumerate(a):
                #print(b)
                if b==1 or b==2:
                    botones[i*3+e].modificarBoton("X") if b==1 else botones[i*3+e].modificarBoton("T")
    print("Se terminó de dibujar")
                
#Socket SEND
def mandarMensaje(mensaje):
    print(mensaje)
    tablero=[]
    TCPClientSocket.send(mensaje)
    print("Esperando una respuesta...P")
    data = TCPClientSocket.recv(buffer_size)
    info=pickle.loads(data)
    tablero=info[1]
    if info[0]!=0:
        frame7=Frame(root)
        frame7.pack(fill=X)
        lbl5 = Label(frame7, text=diccionario[info[0]], width=8)
        lbl5.pack(side=LEFT, padx=5, pady=5)        
        lbl6 = Label(frame7, text="Tiempo de Juego: \t "+info[2], width=40)
        lbl6.pack(side=BOTTOM, padx=5, pady=5)        
        
        MENSAJE=diccionario[info[0]]+"\n"+"Tiempo de Juego:\t"+info[2]
        messagebox.showinfo(message=MENSAJE, title="Juego Terminado")
        TCPClientSocket.close()
    dibujarTablero(tablero)

def dificultadP():
    dificultad='0'
    dif=dificultad.encode(encoding="utf-8")
    mandarMensaje(dif)
    #frame4.pack_forget()
    
def dificultadA():
    dificultad='1'
    dif=dificultad.encode(encoding="utf-8")
    mandarMensaje(dif)
    lbl4.pack(side=LEFT, anchor=N, padx=5, pady=5)
    #frame4.pack_forget()

button2 = Button(frame4, text="Principiante",command=dificultadP )

button3 = Button(frame4, text="Avanzado",command=dificultadA )

#Frame Juego

frame5 = Frame(root)
frame5.pack(fill=X)

lbl4 = Label(frame5, text="Selecciona la casilla que quieres marcar", width=50)

 
frame6 = Frame(root)
frame6.pack(fill=X)
        
button4 = Button(frame4, text="Avanzado",command=dificultadA )



root.mainloop()







