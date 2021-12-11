# !/usr/bin/env python3
# https://github.com/PySimpleGUI/PySimpleGUI

from tkinter import Button, Entry, IntVar, StringVar, Tk, PhotoImage, Radiobutton, Label, Text, messagebox
from tkinter.constants import E, END, GROOVE, NORMAL, DISABLED, W
import grpc, distribuidos_pb2, distribuidos_pb2_grpc
from re import search
root = None
ultimaOpcion = None
channel = None
stub = None
usuario = "Admin"
texto = ""


def conectar(ip,port,usu,contra):
    global channel
    global stub
    global root
    global usuario
    mensaje="Error de inicio de sesión"
    try:
        channel=grpc.insecure_channel(ip+':'+port)
        stub = distribuidos_pb2_grpc.ArchivosStub(channel)  
        #Iniciar sesión
        response = stub.logging(distribuidos_pb2.autenticacion(usuario=usu, contrasena=contra))
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
        continuar = messagebox.askretrycancel(
        message=mensaje, title="Error de Inicio de Sesión")
    
        #continuar = messagebox.askretrycancel(
        #    message="Dirección o Puerto Erróneo", title="Error")
        #if not continuar:
        #    root.destroy()

def conexion():
    global root
    root = Tk()
    # Icono Aplicación
    ancho_ventana = 210
    alto_ventana = 210
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + \
        "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.resizable(False, False)
    root.title("Conexión")

    Label(root, text="Escribe IP y Puerto para conectarte").grid( row=0, columnspan=4, sticky="ew", padx=5, pady=10)
    Label(root, text="IP:" ).grid(row=1, column=0, pady=5)
    Label(root, text="Puerto:" ).grid(row=2, column=0, pady=5)
    Label(root, text="Usuario:" ).grid(row=3, column=0, pady=5)
    Label(root, text="Contraseña:" ).grid(row=4, column=0, pady=5)
    ip = Entry(root)
    ip.grid(row=1, column=1, columnspan=3, pady=5)
    port = Entry(root)
    port.grid(row=2, column=1, columnspan=3, pady=5)
    usuario = Entry(root)
    usuario.grid(row=3, column=1, columnspan=3, pady=5)
    passw = Entry(root)
    passw.grid(row=4, column=1, columnspan=3, pady=5)

    Button(root, command=lambda: conectar(ip.get(),port.get(),usuario.get(),passw.get()),text="Conectar").grid(row=5, columnspan=3, column=2, pady=5)
    #Button(root, command=lambda: conectar('127.0.0.1', '50051',"Admin","assadmin"),text="Conectar").grid(row=5, columnspan=3, column=2, pady=5)

    root.mainloop()

def interfaz():
    global ultimaOpcion
    global usuario
    def crearArchivo(nombreArchivo):
        mensaje=""
        response = stub.create(distribuidos_pb2.peticion(usuario=usuario,nombreArchivo=nombreArchivo))
        if response.estado==0:
            mensaje="El archivo "+nombreArchivo+" ya existe"
        elif response.estado==1:
            mensaje="Archivo "+nombreArchivo+" creado satisfactoriamente"
        else:
            mensaje="No se pudo crear el archivo: "+nombreArchivo
        monitorRegistro.insert(END,"\n"+mensaje)

    def leerArchivo(nombreArchivo):
        response = stub.preread(distribuidos_pb2.peticion(usuario=usuario,nombreArchivo=nombreArchivo))
        if response.estado==1:
            monitorDatos.delete("1.0",END)
            for response in stub.read(distribuidos_pb2.peticion(usuario=usuario,nombreArchivo=nombreArchivo)):
                monitorDatos.insert(END,response.datos)
            monitorRegistro.insert(END,"\nArchivo "+nombreArchivo+" leído satisfactoriamente")
        elif response.estado==0:
            monitorRegistro.insert(END,"\nNo existe el archivo: "+nombreArchivo)
        else:
            monitorRegistro.insert(END,"\nNo se pudo acceder al archivo: "+nombreArchivo)

    def escribirIterator():
        global texto
        lineas=texto.split("\n")
        for linea in lineas:
            response=distribuidos_pb2.peticionDatos(datos=linea+"\n")
            yield response

    def escribirArchivo(nombreArchivo):
        global texto
        response = stub.prewrite(distribuidos_pb2.peticionEscritura(usuario=usuario,nombreArchivo=nombreArchivo,opcionEscritura=opcionEscritura.get()))
        if response.estado==1:
            texto=monitorDatos.get("1.0",END)
            response=stub.write(escribirIterator())
            if response.estado==1:
                if opcionEscritura.get()=='a':
                    monitorRegistro.insert(END,"\nSe escribió el archivo "+ nombreArchivo +" satisfactoriamente ")
                elif opcionEscritura.get()=='w':
                    monitorRegistro.insert(END,"\nSe sobreescribió el archivo "+ nombreArchivo +"  satisfactoriamente")
            elif response.estado==0:
                monitorRegistro.insert(END,"\nNo se escribió el archivo"+ nombreArchivo +"  correctamente ")
            else:
                monitorRegistro.insert(END,"\nNo se pudo acceder al archivo: "+ nombreArchivo)
        elif response.estado==0:
            monitorRegistro.insert(END,"\nNo existe el archivo: "+ nombreArchivo)
        else:
            monitorRegistro.insert(END,"\nNo se pudo acceder al archivo: "+ nombreArchivo)

    def renombrarArchivo(nombreArchivo,nuevoNombre):
        mensaje=""
        response = stub.rename(distribuidos_pb2.renombre(usuario=usuario,nombreArchivo=nombreArchivo,nombreNuevoArchivo=nuevoNombre))
        if response.estado==0:
            mensaje="No existe el archivo:  "+nombreArchivo
        elif response.estado==1:
            mensaje="Archivo: "+ nombreArchivo +"renombrado satisfactoriamente a:"+nuevoNombre
        elif response.estado==-1:
            mensaje="No se puede renombrar por que ya existe el archivo :"+nuevoNombre
        elif response.estado==-2:
            mensaje="No se pudo renombrar el archivo:"+nombreArchivo
        monitorRegistro.insert(END,"\n"+mensaje)

    def eliminarArchivo(nombreArchivo):
        mensaje=""
        response = stub.remove(distribuidos_pb2.peticion(usuario=usuario,nombreArchivo=nombreArchivo))
        if response.estado==1:
            mensaje="El archivo "+nombreArchivo+" se eliminó satisfactoriamente"
        elif response.estado==0:
            mensaje="El archivo "+nombreArchivo+" no existe"
        else:
            mensaje="No se pudo borrar el archivo "+nombreArchivo
        monitorRegistro.insert(END,"\n"+mensaje)

    def crearCarpeta(nombreCarpeta):
        mensaje=""
        response = stub.mkdir(distribuidos_pb2.peticion(usuario=usuario,nombreArchivo=nombreCarpeta))
        if response.estado==1:
            mensaje="La carpeta "+nombreCarpeta+" se creó satisfactoriamente"
        elif response.estado==0:
            mensaje="La carpeta "+nombreCarpeta+" ya existe"
        else:
            mensaje="No se pudo crear la carpeta "+nombreCarpeta
        monitorRegistro.insert(END,"\n"+mensaje)
        
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
        monitorRegistro.insert(END,"\n"+mensaje)
    
    def cd(nombreCarpeta):
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
        monitorRegistro.insert(END,"\n"+mensaje)

    def listarCarpeta():
        monitorRegistro.insert(END,"\n")
        a=0
        for response in stub.readdir(distribuidos_pb2.peticion(usuario=usuario,nombreArchivo="")):
            a+=1
            if  response.isArchivo:
                monitorRegistro.insert(END,"Archivo")
            else :
                monitorRegistro.insert(END,"Carpeta")
            monitorRegistro.insert(END,"   :   "+response.nombre+"\n")
        if a==0: monitorRegistro.insert(END,"La carpeta está vacía\n")
              
    def seleccionarEntry():
        global ultimaOpcion
        if ultimaOpcion==8:
            ultimaOpcion = opcion.get()
            if ultimaOpcion==8:
                return
        else:
            if ultimaOpcion != None:
                if ultimaOpcion==3:
                    nombres[ultimaOpcion][0].config(state=DISABLED)
                    nombres[ultimaOpcion][1].config(state=DISABLED)
                else:
                    if ultimaOpcion==1 or ultimaOpcion==2:
                            labelDatos.grid_forget()
                    if ultimaOpcion==2:
                        escrituraOpcion.grid_forget()
                        escrituraOpcion2.grid_forget()
                    monitorDatos.grid_forget()
                    monitorRegistro.grid(rowspan=8)
                    monitorRegistro.config(height=15)
                    nombres[ultimaOpcion].config(state=DISABLED)
            ultimaOpcion = opcion.get()
            if ultimaOpcion==8:
                return
        if ultimaOpcion==3:
            nombres[ultimaOpcion][0].config(state=NORMAL)
            nombres[ultimaOpcion][1].config(state=NORMAL)
        else:
            if ultimaOpcion==1 or ultimaOpcion==2:
                labelDatos.grid(row=5,column=2,sticky=W)
                if ultimaOpcion==1:
                    labelDatos.config(text="Datos de lectura")
                else:
                    labelDatos.config(text="Escribe los datos de escritura")
                    if ultimaOpcion==2:
                        escrituraOpcion.grid(row=4, column=0, sticky=E, padx=15, pady=5)
                        escrituraOpcion2.grid(row=4, column=1, sticky=E, padx=15, pady=5)
                monitorRegistro.grid(rowspan=4)
                monitorRegistro.config(height=8)
                monitorDatos.grid(row=6, column=2, rowspan=4,columnspan=2, sticky=W)
                
            nombres[ultimaOpcion].config(state=NORMAL)
        
    def reiniciar():
        global ultimaOpcion
        if ultimaOpcion != None and ultimaOpcion!=8:
            if ultimaOpcion==3:
                nombres[ultimaOpcion][0].config(state=DISABLED)
                nombres[ultimaOpcion][1].config(state=DISABLED)
            else:
                if ultimaOpcion==2:
                    escrituraOpcion.grid_forget()
                    escrituraOpcion2.grid_forget()
                    opcionEscritura.set("a")
                nombres[ultimaOpcion].config(state=DISABLED)
        ultimaOpcion = None
        opcion.set(None)

    def limpiarRegistro():
        monitorRegistro.config(state=NORMAL)
        monitorRegistro.delete("1.0",END)
        reiniciar()
        monitorRegistro.config(state=DISABLED)

    def limpiarDatos():
        monitorDatos.delete("1.0",END)

    def enviar():
        global ultimaOpcion
        monitorRegistro.config(state=NORMAL)
        try:
            if ultimaOpcion!=8:
                if ultimaOpcion==3:
                    nombre=nombres[3][0].get()
                else:
                    nombre=nombres[ultimaOpcion].get()
        except:
            monitorRegistro.insert(END,"\nNo se seleccionó una acción")
            return
        if ultimaOpcion==0:
            if search(r".+[.].+$",nombre) is not None:
                crearArchivo(nombre)
            else:
                monitorRegistro.insert(END,"\nNombre de archivo incorrecto")
        elif ultimaOpcion==1:
            if search(r".+[.].+$",nombre) is not None:
                leerArchivo(nombre)
            else:
                monitorRegistro.insert(END,"\nNombre de archivo incorrecto")
        elif ultimaOpcion==2:
            if search(r".+[.].+$",nombre) is not None:
                escribirArchivo(nombre)
            else:
                monitorRegistro.insert(END,"\nNombre de archivo incorrecto")
        elif ultimaOpcion==3:
            if search(r".+[.].+$",nombre) is not None:
                nombreNuevo=nombres[3][1].get()
                if search(r".+[.].+$",nombreNuevo) is not None:
                    renombrarArchivo(nombre,nombreNuevo)
                else:
                    monitorRegistro.insert(END,"\nNombre de archivo nuevo incorrecto") 
            else:
                monitorRegistro.insert(END,"\nNombre de archivo original incorrecto")
        elif ultimaOpcion==4:
            if search(r".+[.].+$",nombre) is not None:
                eliminarArchivo(nombre)
            else:
                monitorRegistro.insert(END,"\nNombre de archivo incorrecto")
        elif ultimaOpcion==5:
            if nombre!="":
                crearCarpeta(nombre)
            else:
                monitorRegistro.insert(END,"\nNombre de carpeta incorrecto")
        elif ultimaOpcion==6:
            if nombre!="":
                eliminarCarpeta(nombre)
            else:
                monitorRegistro.insert(END,"\nNombre de carpeta incorrecto")
        elif ultimaOpcion==7:
            if nombre!="":
                cd(nombre)
            else:
                monitorRegistro.insert(END,"\nNombre de carpeta incorrecto")
        elif ultimaOpcion==8:
            listarCarpeta()
        elif ultimaOpcion==-1:
            monitorRegistro.insert(END,"\nError. No se ha seleccionada una opción válida")   
        
        monitorRegistro.config(state=DISABLED)
        #monitorRegistro.insert(END,"Enviando")

    root = Tk()
    # Icono Aplicación
    root.call('wm', 'iconphoto', root._w, PhotoImage(
        file='Problema1/media/icono.png'))
    ancho_ventana = 800
    alto_ventana = 530
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + \
        "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.resizable(False, False)

    root.title("Sistema de Archivos Distribuidos")

    opciones = ['Create', 'Read', 'Write',
                'Rename', 'Remove', 'MkDir', 'RmDir', 'CD', 'ReadDir']
    opcion = IntVar()
    opcion.set(None)
    opcionEscritura = StringVar()
    opcionEscritura.set("a")
    i = 0
    e=1
    Label(root, text="Opción").grid(row=i, column=0, sticky=W, padx=15, pady=5)
    Label(root, text="Nombre del Archivo").grid(row=0, column=1, sticky=W, padx=15, pady=5)
    Label(root, text="Selecciona una opción a realizar:").grid(row=0, column=2, sticky=W)
    nombres = []
    for i, op in enumerate(opciones):
        Radiobutton(root, text=op, variable=opcion, value=i,
                    command=seleccionarEntry).grid(row=i+e, sticky=W, padx=15, pady=5)
        if i==8:
            break
        if i==3:
            nombre = Entry(root, state=DISABLED)
            nombre.grid(row=i+e, column=1, sticky=W, padx=20)
            e+=1
            Label(root, text="Nuevo nombre:").grid(row=i+e, column=0, sticky=E, padx=15, pady=5)
            nuevo = Entry(root, state=DISABLED)
            nuevo.grid(row=i+e, column=1, sticky=W, padx=20)
            nombres.append([nombre,nuevo])
        else:
            nombre = Entry(root, state=DISABLED)
            nombre.grid(row=i+e, column=1, sticky=W, padx=20)
            nombres.append(nombre)    
            if i==2:
                e+=1
                escrituraOpcion=Radiobutton(root, text="Añadir", variable=opcionEscritura, value="a")
                escrituraOpcion2=Radiobutton(root, text="Sobreescribir", variable=opcionEscritura, value="w")
        

        
        

    monitorRegistro = Text(root, height=15, width=60, relief=GROOVE, state=DISABLED)
    monitorRegistro.grid(row=1, column=2, rowspan=7,columnspan=2, sticky=W)

    labelDatos=Label(root)
    monitorDatos = Text(root, height=8, width=60, relief=GROOVE)
    

    Button(root, text="Reiniciar", command=reiniciar).grid(row=i+e+2, padx=15, pady=5)
    Button(root, text="Enviar", command=enviar).grid(row=i+e+2, column=1, padx=15, pady=15)
    Button(root, text="Limpiar Registro", command=limpiarRegistro).grid(row=i+e+3,column=0, padx=15, pady=5)
    Button(root, text="Limpiar Datos", command=limpiarDatos).grid(row=i+e+3,column=1, padx=15, pady=5)

    root.mainloop()


if __name__ == "__main__":
    #conectar('127.0.0.1', '50051',"Admin","passadmin")
    conexion()
    interfaz()
