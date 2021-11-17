from tkinter import Tk, TOP, BOTH, X, LEFT, BOTTOM, W, SUNKEN, RIGHT, DISABLED, NORMAL, Widget, messagebox,Button,PhotoImage
import tkinter
from tkinter.ttk import Frame, Label
#https://omes-va.com/tkinter-opencv-imagen/


def interfaz():
    root = Tk()
    ancho_ventana = 785
    alto_ventana = 700
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    root.call('wm', 'iconphoto', root._w, PhotoImage(file='Problema1/icono.png'))
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.resizable(False,False)

    root.title("Problema 1")
    #Distribución de Frames
    Frame1=Frame(root).grid(row=0)
    Frame2=Frame(root, borderwidth=3, relief="raised").grid(row=1)
    botones=[]
    for num in range(10):
        botones.append(boton(Frame1,(num//5,num-(num//5*5))))
    Label1=Label(Frame2,text="Hola", borderwidth=num//2, relief="raised").grid(column=0)
    Label2=Label(Frame2,text="Hola2", borderwidth=num//2, relief="raised").grid(column=1)
    Label3=Label(Frame2,text="Hola3", borderwidth=num//2, relief="raised").grid(column=2)
    root.mainloop()


class boton:
    botonn=None
    BORDER_ENCENDIDO = 8
    BORDER_APAGADO = 2
    
    def __init__(self,Frame1,posicion) -> None:
        photo = PhotoImage(file = r"Problema1/persona.png") 
        photoimage = photo.subsample(100, 100) 
        self.botonn=Button(Frame1,text="Hola!",width=15,height=10, borderwidth=8,relief='groove')
        self.botonn.grid(row=posicion[0],column=posicion[1],padx=15, pady=10)
        self.botonn.config(command=self.modificarBoton,image=photoimage,compound = LEFT)
        
    def modificarBoton(self) ->None:
        if self.botonn['borderwidth']==self.BORDER_ENCENDIDO:
            self.botonn.config(borderwidth=self.BORDER_APAGADO)
        else:
            self.botonn.config(borderwidth=self.BORDER_ENCENDIDO)
    def limpiarBoton(self) ->None:
        self.botonn.config(text=" ")
        self.botonn.config(state=NORMAL)


if __name__ == "__main__":
    interfaz()
    