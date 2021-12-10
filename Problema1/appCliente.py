# !/usr/bin/env python3
# https://github.com/PySimpleGUI/PySimpleGUI

__author__ = "Oscar Lozano Rivera"
import tkinter as tk
from tkinter import BooleanVar, Entry, Image, Tk, PhotoImage, messagebox, Label , Text , END
from tkinter.constants import INSERT, TOP
from tkinter.ttk import Frame, Label, Button 
from PIL import ImageTk, Image
from itertools import count, cycle
from re import T, search
import pathlib, threading, pyaudio, wave, logging, grpc, audio_pb2, audio_pb2_grpc, tkinter as tk

CHUNK = 1024
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "Problema1/audio/output.wav"
NOMBRE = None
NUMJUGADOR = None

juegoNuevo = True
panelizquierdo = None
botongrabar = None
botonSiguiente = None
indicacion = None
lock = threading.Lock()                     #Candado
root = None
botones=[]

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',)

class ImageLabel(Button):  # https://pythonprogramming.altervista.org/animate-gif-in-tkinter/?doing_wp_cron=1637124258.4672770500183105468750
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    estado = False
    img = None

    def inicializar(self, grabar) -> None:
        self.img = grabar
        self.config(image=self.img, command=self.cambiarEstado)
        self.grid(row=4, column=2, pady=10)

    def cambiarEstado(self) -> None:
        if self.estado:
            self.estado = False
            self.unload()
        else:
            self.estado = True
            self.load('Problema1/media/grabando.gif')
            datos=threading.Thread(target=self.grabar,args=( None, ), name="Grabando")
            datos.start()
        

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)

        frames = []

        try:
            for i in count(1):
                imag = ImageTk.PhotoImage(im.copy())
                frames.append(imag)
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 0

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.frames = None
        self.config(image=self.img)

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

    def grabar(self,algo):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        logging.debug("* recording")
        frames = []
        while(self.estado):
            data = stream.read(CHUNK)
            frames.append(data)
        logging.debug("* done recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        if enviarAudio(stub):
            botonSiguiente.grid(row=5, column=2, pady=10)
        else:
            indicacion.config(text="Espera tu turno . . .")
            botongrabar.config(state="disabled")
            actualizar(stub)

class botonImagen:
    botonn = None
    BORDER_ENCENDIDO = 8
    BORDER_APAGADO = 2
    imagen = None
    imagenNot = None
    estado = True

    def __init__(self, Frame1, posicion, photoimage, photoimageNot, nombre) -> None:
        self.imagen = photoimage
        self.imagenNot = photoimageNot
        self.botonn = Button(Frame1, width=22)
        self.botonn.grid(
            row=posicion[0], column=posicion[1], padx=18, pady=10, sticky="nesw")
        self.botonn.grid_columnconfigure(posicion[1], weight=1)
        self.botonn.config(command=self.modificarBoton,
                           image=photoimage, compound=TOP, text=nombre,)

    def modificarBoton(self) -> None:
        if self.estado:
            self.estado = False
            self.botonn.config(image=self.imagenNot, compound=TOP)
        else:
            self.estado = True
            self.botonn.config(image=self.imagen)  
    
    def reiniciarImagen(self) -> None:
        if not self.estado:
            self.estado = True
            self.botonn.config(image=self.imagen)  

def getIPHOST(ip, port, nombre ,root) -> BooleanVar:
    global HOST
    global PORT
    global NOMBRE
    if search(r'[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3} [0-9]{1,5}', ip+" "+port) is not None:
        HOST = ip
        PORT = port
        NOMBRE = nombre
        root.destroy()
    else:
        continuar = messagebox.askretrycancel(
            message="Dirección o Puerto Erróneo", title="Error")
        if not continuar:
            root.destroy()

def conexion() -> None:
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

    Label(root, text="Escribe IP y Puerto para conectarte", background="orange").grid( row=0, columnspan=4, sticky="ew", padx=5, pady=10)
    Label(root, text="IP:", background="orange").grid(row=1, column=0, pady=5)
    Label(root, text="Puerto:", background="orange").grid(row=2, column=0, pady=5)
    Label(root, text="Nombre:", background="orange").grid(row=3, column=0, pady=5)
    ip = Entry(root)
    ip.grid(row=1, column=1, columnspan=3, pady=5)
    port = Entry(root)
    port.grid(row=2, column=1, columnspan=3, pady=5)
    nombre = Entry(root)
    nombre.grid(row=3, column=1, columnspan=3, pady=5)
    
    #Button(root,command=lambda:getIPHOST(ip.get(),port.get(),nombre.get(),root),text="Conectar").grid(row=3,columnspan=3,column=2,pady=5)
    Button(root, command=lambda: getIPHOST('127.0.0.1', '50051',nombre.get(), root),text="Conectar").grid(row=4, columnspan=3, column=2, pady=5)

    root.mainloop()

def interfaz(stub):
    global NOMBRE
    global NUMJUGADOR
    global panelizquierdo
    global botongrabar
    global indicacion
    global botonSiguiente
    global root
    global botones
    root = Tk()
    # Icono Aplicación
    root.call('wm', 'iconphoto', root._w, PhotoImage(
        file='Problema1/media/icono.png'))
    ancho_ventana = 890
    alto_ventana = 890
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + \
        "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.resizable(False, False)

    root.title("Adivina Quien  -  "+NOMBRE)

    photo = PhotoImage(file=r"Problema1/media/icono.png")
    photoimage = photo.subsample(4, 4)
    grabar = PhotoImage(file=r"Problema1/media/rec.png")

    # Frame Principal
    Frame1 = Frame(root).grid(ipadx=50, sticky="nesw")

    # Indicaciones
    indicaciones = Label(Frame1, text="Eres el jugador número "+str(NUMJUGADOR), padding=20)
    indicaciones.grid(row=0, column=0, columnspan=2, sticky="nesw")
    indicacion = Label(Frame1, text="Espera tu turno . . .")
    indicacion.grid(row=0, column=3, columnspan=2, sticky="nesw")

    # Botones de Imagen
    directorio = pathlib.Path('Problema1/media/personajes')
    ls = []
    for fichero in directorio.iterdir():
        ls.append(fichero.name)
    for num in range(10):
        photo = PhotoImage(file=r"Problema1/media/Personajes/"+ls[num])
        photoNot = PhotoImage(file=r"Problema1/media/PersonajesNot/"+ls[num])
        photoimage = photo.subsample(4, 4)
        photoimageNot = photoNot.subsample(4, 4)
        grabar = PhotoImage(file=r"Problema1/media/rec.png")
        botones.append(botonImagen(Frame1, ((num//5)+1, num-(num//5*5)), photoimage, photoimageNot, ls[num][:-4]))

    # Panel Jugadores
    panelizquierdo = Text(Frame1, relief="groove", width=5 ,height=10 )
    panelizquierdo.grid(row=4, column=0,  columnspan=2, rowspan=2, sticky="ew", padx=25, pady=30)
    panelizquierdo.insert(END,"Bienvenido al juego Adivina Quien")
    panelizquierdo.config(state="disabled")

    # Label Grabando
    botongrabar = ImageLabel(Frame1)
    botongrabar.inicializar(grabar)
    if NUMJUGADOR!=1:
        botongrabar.config(state='disabled')

    #Boton Siguiente
    botonSiguiente= tk.Button(Frame1,relief="groove",text="Jugar de Nuevo", command=otroJuego)

    #Boton Finalizar
    botonFinal= tk.Button(Frame1,relief="groove",text="Terminar juego")
    botonFinal.grid(row=6, column=2, pady=10)
    botonFinal.config(command=root.destroy)
    # Panel Pistas
    panelderecho = tk.Label(Frame1, relief="groove" ,height=10)
    panelderecho.grid(row=4, column=3, columnspan=2, rowspan=2, sticky="ew" , padx=25, pady=30)
    panelderecho.config(text="Preguntas prototipo: "+
            "\n¿Tu personaje es alto/pequeño?"+
            "\n¿Tu personaje tiene [objeto] en la cabeza?"+
            "\n¿Tu personaje usa falda/pantalón?"+
            "\n¿Tu personaje usa botas/tennis/zapatos?"+
            "\n¿Tu personaje es hombre/mujer?"
    )
    #act = threading.Thread(target=actualizar, args=(stub))
    #act.start()
    actualizar(stub)
    root.mainloop()

def otroJuego():
    global stub
    global NUMJUGADOR
    global juegoNuevo
    global botones
    global botonSiguiente
    juegoNuevo = True
    NUMJUGADOR = iniciarJuego(stub)
    actualizar(stub)
    botonSiguiente.grid_forget()
    for boton in botones:   
        boton.reiniciarImagen()

def iniciarJuego(stub):
    global NOMBRE
    global indicacion
    global panelizquierdo
    try:
        indicacion.config(text="Espera tu turno . . .")        
        panelizquierdo.config(state="normal")
        panelizquierdo.delete(1.0,END)
        panelizquierdo.insert(INSERT,"Bienvenido al juego Adivina Quien")
        panelizquierdo.config(state="disabled")
    finally:
        response = stub.iniciarJuego(audio_pb2.nombre(nombreJugador=NOMBRE))
        logging.debug("Hola %s ,estas en la lista con el número: %s" , response.nombreJugador , str(response.numeroJugador) )
        return response.numeroJugador

def terminarJuego(stub):
    global NOMBRE
    response = stub.terminarJuego(audio_pb2.nombre(nombreJugador=NOMBRE))
    logging.log("Adios " + response.nombreJugador + " , gracias por jugar Adivina Quien :) ")

def actualizar(stub):
    global NOMBRE
    global NUMJUGADOR
    global panelizquierdo
    global botongrabar
    global indicacion
    resp="No"
    logging.debug('Esperando turno')
    response = stub.actualizarJuego(audio_pb2.lista(nombreJugador=NOMBRE,numeroJugador=NUMJUGADOR))
    if response.respuesta:
        resp="Si"
    if response.textoAudio !="Iniciando":
        panelizquierdo.config(state="normal")
        panelizquierdo.insert(END,"\n"+response.nombre+" preguntó: "+response.textoAudio+"\nRespuesta:"+resp)
        panelizquierdo.config(state="disabled")        
    if response.estado :
        logging.debug("Juego Terminó")
        botonSiguiente.grid(row=5, column=2, pady=10)
        botongrabar.config(state="disabled")
    else:
        botongrabar.config(state="normal")
    indicacion.config(text=response.textoPartida)
    #print('Estado: ',response.estado)
    #print('Texto Audio: ',response.textoAudio)
    #print('Respuesta: ',response.respuesta)
    #print('Nombre: ',response.nombre)
    #print('Texto Partida: ',response.textoPartida)
    return 

def mandarAudioIterator():
    #Aquí se lee el archivo de audio
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
    while True:
        data = wf.readframes(CHUNK)
        if data==b'':
            break
        saludo = audio_pb2.trozosAudio(chunk=data)
        yield saludo
            
def enviarAudio(stub):
    global panelizquierdo
    global indicacion
    global botongrabar
    resp="No"
    response = stub.recibirAudio(mandarAudioIterator())
    #Response es la respuesta del audio enviado
    if response.respuesta:
        resp="Si"
    panelizquierdo.config(state="normal")
    panelizquierdo.insert(END,"\n"+response.nombre+" preguntó: "+response.textoAudio+"\nRespuesta:"+resp)
    panelizquierdo.config(state="disabled")
    #print('Estado: ',response.estado)
    #print('Texto Audio: ',response.textoAudio)
    #print('Respuesta: ',response.respuesta)
    #print('Nombre: ',response.nombre)
    #print('Texto Partida: ',response.textoPartida)
    if response.estado :
        logging.debug("Juego Terminó")
        indicacion.config(text=response.textoPartida)
        botongrabar.config(state="disabled")
        return True

if __name__ == "__main__":
    HOST = None
    PORT = None
    conexion()
    if HOST != None and PORT != None:
        logging.debug("Conectando a %s mediante el puerto %s", HOST, PORT)
        with grpc.insecure_channel(HOST+':'+PORT) as channel:
            stub = audio_pb2_grpc.AudioStub(channel)            
            NUMJUGADOR = iniciarJuego(stub)
            interfaz(stub)
            logging.debug("Terminó la interfaz gráfica")
            terminarJuego(stub)
