# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"
from tkinter import Image, Tk,PhotoImage
from tkinter.constants import E, N, TOP,LEFT
from tkinter.ttk import Frame, Label,Button
from PIL import ImageTk,Image
from itertools import count, cycle

class ImageLabel(Button):     #https://pythonprogramming.altervista.org/animate-gif-in-tkinter/?doing_wp_cron=1637124258.4672770500183105468750
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    estado=False
    img=None
    def inicializar(self,grabar) -> None:
        self.img=grabar
        self.config(image=self.img,command=self.cambiarEstado)
        self.grid(row=3,column=2)
    def cambiarEstado(self) ->None:
        if self.estado:
            self.estado=False
            self.unload()
        else:
            self.estado=True
            self.load('Problema1/grabando.gif')


    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)


        frames = []

        try:
            for i in count(1):
                imag=ImageTk.PhotoImage(im.copy())
                frames.append(imag)
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 150

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

def grabar():
    pass

def interfaz():
    root = Tk()

    root.call('wm', 'iconphoto', root._w, PhotoImage(file='Problema1/icono.png'))

    ancho_ventana = 880
    alto_ventana = 700
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.resizable(False,False)

    root.title("Problema 1")

    photo = PhotoImage(file = r"Problema1/icono.png") 
    photoimage = photo.subsample(4, 4) 
    grabar = PhotoImage(file =r"Problema1/rec.png") 
    


    botones=[]
    nombre="Lolo"

    #Frame Principal
    Frame1=Frame(root).grid(ipadx=50,sticky="nesw")
    
    #Botones de Imagen
    for num in range(10):
        botones.append(botonImagen( Frame1,(num//5,num-(num//5*5)),photoimage,nombre ))   

    #Panel Jugadores
    izquierda=Label(Frame1,relief="groove").grid(row=3,column=0,columnspan=2,sticky="nesw",padx=25,pady=30)
    
    #Label Grabando
    labelrecord = ImageLabel(Frame1)
    labelrecord.inicializar(grabar)
    
    #Panel Pistas
    derecha=  Label(Frame1,relief="groove").grid(row=3,column=3,columnspan=2,sticky="nesw",padx=25,pady=30)

    root.mainloop()

class botonImagen:
    botonn=None
    BORDER_ENCENDIDO = 8
    BORDER_APAGADO = 2
    imagen=None
    estado=True
    def __init__(self,Frame1,posicion,photoimage,nombre) -> None:
        self.imagen=photoimage
        self.botonn=Button(Frame1)
        self.botonn.grid(row=posicion[0],column=posicion[1],padx=18,pady=10,sticky="nesw")
        self.botonn.grid_columnconfigure(posicion[1],weight=1)
        self.botonn.config(command=self.modificarBoton,image=photoimage,compound=TOP,text=nombre,)
    def modificarBoton(self)->None:
        if self.estado:
            self.estado=False
            self.botonn.config(image="",compound=TOP)
        else:
            self.estado=True
            self.botonn.config(image=self.imagen)

if __name__ == "__main__":
    interfaz()