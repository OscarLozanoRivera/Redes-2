#!/usr/bin/env python3

import pickle
import socket
from tkinter import Tk, Text, TOP, BOTH, X, LEFT, BOTTOM, W, SUNKEN, RIGHT, DISABLED, NORMAL, Widget, messagebox,Button
import tkinter
from tkinter.ttk import Frame, Label, Entry
from warnings import catch_warnings


#Clase Botón
class boton:
    botonnuevo=None
    def __init__(self,posicion) -> None:
        self.botonnuevo=Button(frame6,text=" ",width=5,height=3)
        self.botonnuevo.grid(row=posicion[0],column=posicion[1])
        self.botonnuevo.config(command=lambda:Mensajes(pickle.dumps(posicion)))
    def modificarBoton(self,texto,enable) ->None:
        self.botonnuevo.config(text=texto)
        if enable:
            self.botonnuevo.config(state=NORMAL)
        self.botonnuevo.config(state=DISABLED)
    def limpiarBoton(self) ->None:
        self.botonnuevo.config(text=" ")
        self.botonnuevo.config(state=NORMAL)

#Dibujar Tablero

def getIP():
        return entryIP1.get()+"."+entryIP2.get()+"."+entryIP3.get()+"."+entryIP4.get()

def dibujarTablero(gridGato,enable):
    
    for i,tab in enumerate(gridGato):
        if 1 in tab or 2 in tab:
            ceros=0
            print("Cero")
            break
        elif i==len(gridGato)-1: 
            ceros=1
    if ceros==1:             
        print("Nuevo tablero")
        for a in range(len(botones)-1,-1,-1):
            botones[a].botonnuevo.grid_forget()
            botones[a].botonnuevo.destroy
            botones.pop(a)
        for i,a in enumerate(gridGato):
            for e,b in enumerate(a):
                botones.append(boton([i,e]))
    else:                     
        print("Modificar tablero")
        for i,a in enumerate(gridGato):
            for e,b in enumerate(a):
                if b==1 or b==2:
                    botones[i*len(gridGato)+e].modificarBoton("X",False) if b==1 else botones[i*len(gridGato)+e].modificarBoton("T",False)
    print("Se terminó de dibujar")
    

#Juego Terminado
def estadoJuego(estado,tiempo):
    MENSAJE=diccionario[estado]+"\n"+"Tiempo de Juego:\t"+tiempo[3:-4]
    if estado==-1:
        status="Juego Empatado :)"
    elif estado==1:
        status="¡Felicidades haz ganado! :D"
    else:
        status="Una lástima, haz perdido :C"
    statusbar.config(text="\t"+status+"        Tiempo Jugado:"+tiempo[3:-4]+" seg")
    continuar=messagebox.askyesno(message=MENSAJE, title="Juego Terminado")
    #print("Cont",continuar)
    if continuar:
        Mensajes(pickle.dumps(0))     
        frame5.pack(fill=X)
        frame5.pack_forget()
        frame6.pack_forget()
    else:
        TCPClientSocket.send(pickle.dumps(-1))
        cerrarConexion()    

#Socket SEND  
def Mensajes(mensaje):
    print("Enviando mensaje")
    TCPClientSocket.send(mensaje)
    data = TCPClientSocket.recv(buffer_size)
    print("Se recibió información")
    info=pickle.loads(data)
    print(info[1])
    dibujarTablero(info[1],True) if info[2]==1 else dibujarTablero(info[1],False)
    if info[0]!=0:
        estadoJuego(info[0],info[3])

    esperarTablero()
    
def esperarTablero():
    while True:
        print("Esperando tablero")
        data=TCPClientSocket.recv(buffer_size)
        if not data:
            print("No hay datos")
        else:
            data=pickle.loads(data)
        print(data)
        if data[0]!=0:
            print("El juego terminó")
            estadoJuego(data[0],data[3])
        if data[2]==1:              #Es su turno
            dibujarTablero(data[1],True)
            return
        else:
            dibujarTablero(data[1],False)
        print("Regreso de dibujarse")

#Socket CONCECT
def conectar(HOST,PORT):
    try:                #print("{},{},{},{}".format(HOST,type(HOST),PORT,type(PORT)))
        PORT=int(PORT)
        print("Conectando con {} mediante el puerto: {}".format(HOST,PORT))
        TCPClientSocket.connect((HOST,PORT))
    except socket.error as e:
        messagebox.showerror(message="No se pudo conectar, intenta otra vez",title="Error de conexión")
        return
    except:
        print("Puerto inválido")
    else:
        frame0.pack_forget()
        frame5.pack(fill=X)
    frame6.pack(anchor="center",side=TOP, padx=5, pady=5)
    esperarTablero()
    

#Socket CLOSE
def cerrarConexion():
    print("Cerrando conexión")
    TCPClientSocket.close
    root.destroy()

#main

TCPClientSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HEIGHT  = 10        #Botones
WIDTH = 5           #Botones
diccionario={1:"Ganador",2:"Perdedor",-1:"Empate"}
buffer_size = 1024
botones=[]

#Interfaz Gráfica

root = Tk()
ancho_ventana = 400
alto_ventana = 400
x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2

posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
root.geometry(posicion)
root.resizable(False,False)

root.title("Practica 2")
#Frame Conexión
frame0 = Frame(root)
frame0.pack(fill=X)

frame1 = Frame(frame0)
frame1.pack(fill=X)

lbl1 = Label(frame1, text="IP", width=8)
lbl1.pack(side=LEFT, padx=5, pady=5)

#Frame IP
entryIP1 = Entry(frame1,width=3)
entryIP1.pack(side=LEFT,expand=False)

lablePunto= Label(frame1,text=".")
lablePunto.pack(side=LEFT)

entryIP2 = Entry(frame1,width=3)
entryIP2.pack(side=LEFT)

lablePunto= Label(frame1,text=".")
lablePunto.pack(side=LEFT)

entryIP3 = Entry(frame1,width=3)
entryIP3.pack(side=LEFT)

lablePunto= Label(frame1,text=".")
lablePunto.pack(side=LEFT)

entryIP4 = Entry(frame1,width=3)
entryIP4.pack(side=LEFT)


#Frame Puerto
frame2 = Frame(frame0)
frame2.pack(fill=X)

lbl2 = Label(frame2, text="Puerto", width=8)
lbl2.pack(side=LEFT, padx=5, pady=5)


entry2 = Entry(frame2)
entry2.pack(fill=X, padx=5, expand=True)

frame3 = Frame(frame0)
frame3.pack(fill=BOTH, expand=True)    

#Boton Iniciar Conexión

#button = Button(frame3, text="Obtener IP y Puerto",command=lambda:conectar(getIP(),entry2.get()) )
button = Button(frame3, text="Obtener IP y Puerto",command=lambda:conectar("127.0.0.1",12345) )
button.pack(side=LEFT, padx=5, pady=5)


#Frame Juego

frame5 = Frame(root)

lbl4 = Label(frame5, text="Selecciona la casilla que quieres marcar")
lbl4.pack(side=TOP, padx=5, pady=5)

frame6 = Frame(root)

#Barra de estado
statusbar = Label(root,relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

#Boton Salir
frame7 = Frame(root)
frame7.pack(side=BOTTOM,fill=X)

button3 = Button(frame7, text="Terminar conexión y juego",command= cerrarConexion)
button3.pack(side=RIGHT, padx=5, pady=5)

root.mainloop()



