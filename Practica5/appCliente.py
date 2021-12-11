# !/usr/bin/env python3
# https://github.com/PySimpleGUI/PySimpleGUI

import logging
from tkinter import Button, Entry, IntVar, Tk, PhotoImage, Radiobutton, Label, Text, messagebox
from tkinter.constants import E, END, GROOVE,NORMAL, DISABLED, W
import grpc, distribuidos_pb2, distribuidos_pb2_grpc
from re import search
root = None
ultimaOpcion = None
channel = None
stub = None
usuario = "Admin"


def conectar(ip,port,usu,contra):
    global channel
    global stub
    global root
    global usuario
    try:
        channel=grpc.insecure_channel(ip+':'+port)
        stub = distribuidos_pb2_grpc.ArchivosStub(channel)  
        #Iniciar sesión
        response = stub.logging(distribuidos_pb2.autenticacion(usuario=usu, contrasena=contra))
        mensaje=""
        if response.estado == -1:
            mensaje="Usuario no registrado"
        elif response.estado == 0:
            mensaje="Contraseña incorrecta"
        else:
            usuario=usu
            root.destroy()
            return
        continuar = messagebox.askretrycancel(
        message=mensaje, title="Error de Inicio de Sesión")
        if not continuar:
            root.destroy()
  
    except Exception as e:
        print("")
    
        #continuar = messagebox.askretrycancel(
        #    message="Dirección o Puerto Erróneo", title="Error")
        #if not continuar:
        #    root.destroy()



def conexion():
    global root
    root = Tk()
    # Icono Aplicación
    ancho_ventana = 210
    alto_ventana = 180
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + \
        "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.resizable(False, False)
    root.config(background="orange")
    root.title("Conexión")

    Label(root, text="Escribe IP y Puerto para conectarte").grid( row=0, columnspan=4, sticky="ew", padx=5, pady=10)
    Label(root, text="IP:", background="orange").grid(row=1, column=0, pady=5)
    Label(root, text="Puerto:", background="orange").grid(row=2, column=0, pady=5)
    Label(root, text="Usuario:", background="orange").grid(row=3, column=0, pady=5)
    Label(root, text="Contraseña:", background="orange").grid(row=4, column=0, pady=5)
    ip = Entry(root)
    ip.grid(row=1, column=1, columnspan=3, pady=5)
    port = Entry(root)
    port.grid(row=2, column=1, columnspan=3, pady=5)
    usuario = Entry(root)
    usuario.grid(row=3, column=1, columnspan=3, pady=5)
    passw = Entry(root)
    passw.grid(row=4, column=1, columnspan=3, pady=5)
    
    #Button(root,command=lambda:getIPHOST(ip.get(),port.get(),nombre.get(),root),text="Conectar").grid(row=3,columnspan=3,column=2,pady=5)
    #Button(root, command=lambda: getIPHOST('127.0.0.1', '50051',nombre.get(), root),text="Conectar").grid(row=4, columnspan=3, column=2, pady=5)
    #Button(root, command=lambda: conectar(ip.get(),port.get(),usuario.get(),passw.get()),text="Conectar").grid(row=5, columnspan=3, column=2, pady=5)
    Button(root, command=lambda: conectar('127.0.0.1', '50051',"Admin","assadmin"),text="Conectar").grid(row=5, columnspan=3, column=2, pady=5)

    root.mainloop()

def interfaz():
    global ultimaOpcion

    def crearArchivo(nombreArchivo):
        global usuario
        mensaje=""
        response = stub.create(distribuidos_pb2.peticion(usuario=usuario,nombreArchivo=nombreArchivo))
        if response.estado==0:
            mensaje="El archivo "+nombreArchivo+" ya existe"
        elif response.estado==1:
            mensaje="Archivo creado satisfactoriamente"
        else:
            mensaje="No se pudo crear el archivo "+nombreArchivo
        monitor.insert(END,"\n"+mensaje)

    def renombrarArchivo(nombreArchivo,nuevoNombre):
        global usuario
        mensaje=""
        response = stub.rename(distribuidos_pb2.renombre(usuario=usuario,nombreArchivo=nombreArchivo,nombreNuevoArchivo=nuevoNombre))
        if response.estado==0:
            mensaje="No existe el archivo:  "+nombreArchivo
        elif response.estado==1:
            mensaje="Archivo renombrado satisfactoriamente"
        elif response.estado==-1:
            mensaje="Ya existe un archivo :"+nuevoNombre
        elif response.estado==-2:
            mensaje="No se pudo renombrar el archivo:"+nombreArchivo
        monitor.insert(END,"\n"+mensaje)

    def eliminarArchivo(nombreArchivo):
        global usuario
        mensaje=""
        response = stub.remove(distribuidos_pb2.peticion(usuario=usuario,nombreArchivo=nombreArchivo))
        if response.estado==1:
            mensaje="El archivo "+nombreArchivo+" se eliminó satisfactoriamente"
        elif response.estado==0:
            mensaje="El archivo "+nombreArchivo+" no existe"
        else:
            mensaje="No se pudo borrar el archivo "+nombreArchivo
        monitor.insert(END,"\n"+mensaje)

    def crearCarpeta(nombreCarpeta):
        global usuario
        mensaje=""
        response = stub.mkdir(distribuidos_pb2.peticion(usuario=usuario,nombreArchivo=nombreCarpeta))
        if response.estado==1:
            mensaje="La carpeta "+nombreCarpeta+" se creó satisfactoriamente"
        elif response.estado==0:
            mensaje="La carpeta "+nombreCarpeta+" ya existe"
        else:
            mensaje="No se pudo crear la carpeta "+nombreCarpeta
        monitor.insert(END,"\n"+mensaje)
        
    def eliminarCarpeta(nombreCarpeta):
        global usuario
        mensaje=""
        response = stub.rmdir(distribuidos_pb2.peticion(usuario=usuario,nombreArchivo=nombreCarpeta))
        if response.estado==1:
            mensaje="La carpeta "+nombreCarpeta+" se eliminó satisfactoriamente"
        elif response.estado==0:
            mensaje="La carpeta "+nombreCarpeta+" no existe"
        else:
            mensaje="No se pudo eliminar la carpeta "+nombreCarpeta
        monitor.insert(END,"\n"+mensaje)
    
    def cd(nombreCarpeta):
        global usuario
        mensaje=""
        response = stub.cd(distribuidos_pb2.peticion(usuario=usuario,nombreArchivo=nombreCarpeta))
        if response.estado==1:
            if nombreCarpeta=="..":
                mensaje="Se movió la dirección actual correctamente a la carpeta anterior"
            else:
                mensaje="Se movió la dirección actual correctamente a "+nombreCarpeta
        elif response.estado==0:
            mensaje="La carpeta "+nombreCarpeta+" no existe"
        else:
            mensaje="No se pudo cambiar la ubicación a la carpeta anterior "
        monitor.insert(END,"\n"+mensaje)

    def select():
        global ultimaOpcion
        if ultimaOpcion != None:
            if ultimaOpcion==3:
                nombres[ultimaOpcion][0].config(state=DISABLED)
                nombres[ultimaOpcion][1].config(state=DISABLED)
            else:
                nombres[ultimaOpcion].config(state=DISABLED)
        ultimaOpcion = opcion.get()
        if ultimaOpcion==3:
            nombres[ultimaOpcion][0].config(state=NORMAL)
            nombres[ultimaOpcion][1].config(state=NORMAL)
        else:
            nombres[ultimaOpcion].config(state=NORMAL)

    def reiniciar():
        global ultimaOpcion
        if ultimaOpcion != None:
            if ultimaOpcion==3:
                nombres[ultimaOpcion][0].config(state=DISABLED)
                nombres[ultimaOpcion][1].config(state=DISABLED)
            else:
                nombres[ultimaOpcion].config(state=DISABLED)
        ultimaOpcion = None
        opcion.set(None)

    def limpiar():
        monitor.delete("1.0",END)
        reiniciar()

    def enviar():
        global ultimaOpcion
        try:
            if ultimaOpcion==3:
                nombre=nombres[3][0].get()
            else:
                nombre=nombres[ultimaOpcion].get()
        except:
            monitor.insert(END,"\nNo se seleccionó una acción")
            return
        if ultimaOpcion==0:
            if search(r".+[.].+$",nombre) is not None:
                crearArchivo(nombre)
            else:
                monitor.insert(END,"\nNombre de archivo incorrecto")
        elif ultimaOpcion==1:
            pass
        elif ultimaOpcion==2:
            pass
        elif ultimaOpcion==3:
            if search(r".+[.].+$",nombre) is not None:
                nombreNuevo=nombres[3][1].get()
                if search(r".+[.].+$",nombreNuevo) is not None:
                    renombrarArchivo(nombre,nombreNuevo)
                else:
                    monitor.insert(END,"\nNombre de archivo nuevo incorrecto") 
            else:
                monitor.insert(END,"\nNombre de archivo original incorrecto")
        elif ultimaOpcion==4:
            if search(r".+[.].+$",nombre) is not None:
                eliminarArchivo(nombre)
            else:
                monitor.insert(END,"\nNombre de archivo incorrecto")
        elif ultimaOpcion==5:
            if nombre!="":
                crearCarpeta(nombre)
            else:
                monitor.insert(END,"\nNombre de carpeta incorrecto")
        elif ultimaOpcion==6:
            if nombre!="":
                eliminarCarpeta(nombre)
            else:
                monitor.insert(END,"\nNombre de carpeta incorrecto")
        elif ultimaOpcion==7:
            if nombre!="":
                cd(nombre)
            else:
                monitor.insert(END,"\nNombre de carpeta incorrecto")
        elif ultimaOpcion==-1:
            monitor.insert(END,"\nError. No se ha seleccionada una opción válida")   
        

        #monitor.insert(END,"Enviando")

    root = Tk()
    # Icono Aplicación
    root.call('wm', 'iconphoto', root._w, PhotoImage(
        file='Problema1/media/icono.png'))
    ancho_ventana = 800
    alto_ventana = 450
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + \
        "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.resizable(False, False)

    root.title("Sistema de Archivos Distribuidos")

    opciones = ['Create', 'Read', 'Write',
                'Rename', 'Remove', 'MkDir', 'RmDir', 'CD']
    opcion = IntVar()
    opcion.set(None)
    opcion
    i = 0
    e=1
    Label(root, text="Opción").grid(row=i, column=0, sticky=W, padx=15, pady=5)
    Label(root, text="Nombre del Archivo").grid(row=0, column=1, sticky=W, padx=15, pady=5)
    Label(root, text="Selecciona una opción a realizar:").grid(row=0, column=2, sticky=W)
    nombres = []
    for i, op in enumerate(opciones):
        Radiobutton(root, text=op, variable=opcion, value=i,
                    command=select).grid(row=i+e, sticky=W, padx=15, pady=5)
        if i==3:
            nombre = Entry(root, state=DISABLED)
            nombre.grid(row=i+e, column=1, sticky=W, padx=20)
            e+=1
            Label(root, text="Nuevo:").grid(row=i+e, column=0, sticky=E, padx=15, pady=5)
            nuevo = Entry(root, state=DISABLED)
            nuevo.grid(row=i+e, column=1, sticky=W, padx=20)
            nombres.append([nombre,nuevo])
        else:
            nombre = Entry(root, state=DISABLED)
            nombre.grid(row=i+e, column=1, sticky=W, padx=20)
            nombres.append(nombre)    
        
        

    monitor = Text(root, height=15, width=60, relief=GROOVE)
    monitor.grid(row=1, column=2, rowspan=8,columnspan=2, sticky=W)

    Button(root, text="Reiniciar", command=reiniciar).grid(row=i+e+2, padx=15, pady=5)
    Button(root, text="Enviar", command=enviar).grid(row=i+e+2, column=1, padx=15, pady=15)
    Button(root, text="Limpiar", command=limpiar).grid(row=i+e+2,column=2, padx=15, pady=5)

    root.mainloop()


if __name__ == "__main__":
    conectar('127.0.0.1', '50051',"Admin","passadmin")
    #conexion()
    interfaz()
