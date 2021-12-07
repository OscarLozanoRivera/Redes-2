# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"
import pathlib
import threading
from tkinter import BooleanVar, Entry, Image, Tk, PhotoImage, messagebox, Label
from tkinter.constants import ALL, E, N, TOP, LEFT, X
from tkinter.ttk import Frame, Label, Button, Style
from typing import Text, Tuple
from PIL import ImageTk, Image
from itertools import count, cycle
from re import search
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "Problema1/audio/output.wav"


# https://github.com/PySimpleGUI/PySimpleGUI


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
        self.grid(row=5, column=2, pady=10)

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

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


def getIPHOST(ip, port, root) -> BooleanVar:
    global HOST
    global IP
    if search(r'[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3} [0-9]{1,5}', ip+" "+port) is not None:
        HOST = ip
        IP = int(port)
        root.destroy()
    else:
        continuar = messagebox.askretrycancel(
            message="Dirección o Puerto Erróne", title="Juego Terminado")
        if not continuar:
            root.destroy()


def conexion() -> None:
    root = Tk()
    # Icono Aplicación
    ancho_ventana = 210
    alto_ventana = 120
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + \
        "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.resizable(False, False)
    root.config(background="orange")

    Label(root, text="Escribe IP y Puerto para conectarte", background="orange").grid(
        row=0, columnspan=4, sticky="ew", padx=5, pady=10)
    Label(root, text="IP:", background="orange").grid(row=1, column=0, pady=5)
    Label(root, text="Puerto:", background="orange").grid(
        row=2, column=0, pady=5)

    ip = Entry(root)
    ip.grid(row=1, column=1, columnspan=3, pady=5)
    port = Entry(root)
    port.grid(row=2, column=1, columnspan=3, pady=5)
    # Button(root,command=lambda:getIPHOST(ip.get(),port.get(),root)).grid(row=3,columnspan=3,column=2,pady=5)
    Button(root, command=lambda: getIPHOST('127.0.0.1', '12345', root)).grid(
        row=3, columnspan=3, column=2, pady=5)

    root.mainloop()


def interfaz():
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

    root.title("Problema 1")

    photo = PhotoImage(file=r"Problema1/media/icono.png")
    photoimage = photo.subsample(4, 4)
    grabar = PhotoImage(file=r"Problema1/media/rec.png")

    botones = []
    # Frame Principal
    Frame1 = Frame(root).grid(ipadx=50, sticky="nesw")

    # Indicaciones
    indicaciones = Label(Frame1, text="Indicaciones", padding=20)
    indicaciones.grid(row=0, column=0, columnspan=2, sticky="nesw")
    indicaciones = Label(Frame1, text="Indicaciones2")
    indicaciones.grid(row=0, column=3, columnspan=2, sticky="nesw")

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
        botones.append(botonImagen(
            Frame1, ((num//5)+1, num-(num//5*5)), photoimage, photoimageNot, ls[num][:-4]))

    # Panel Jugadores
    izquierda = Label(Frame1, relief="groove")
    izquierda.grid(row=4, column=0, columnspan=2,
                   sticky="nesw", padx=25, pady=30)
    izquierda.config(text="Sas")
    # Label Grabando
    labelrecord = ImageLabel(Frame1)
    labelrecord.inicializar(grabar)

    # Panel Pistas
    derecha = Label(Frame1, relief="groove")
    derecha.grid(row=4, column=3, columnspan=2,
                 sticky="nesw", padx=25, pady=30)
    derecha.config(text="Sis")

    # StatusBar

    root.mainloop()


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


if __name__ == "__main__":
    HOST = None
    IP = None
    conexion()
    if HOST != None and IP != None:
        interfaz()
