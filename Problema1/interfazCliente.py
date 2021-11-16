from tkinter import Tk, Text, TOP, BOTH, X, LEFT, BOTTOM, W, SUNKEN, RIGHT, DISABLED, NORMAL, Widget, messagebox,Button,PhotoImage
import tkinter
from tkinter.ttk import Frame, Label, Entry
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
        botones.append(Button(Frame1,text="Nuevo",width=15,height=10, borderwidth=num//2, relief="raised"))
        botones[num].grid(row=num//5,column=num-(num//5*5),padx=20, pady=10)
    Label1=Label(Frame2,text="Hola", borderwidth=num//2, relief="raised").grid(column=0)
    Label2=Label(Frame2,text="Hola2", borderwidth=num//2, relief="raised").grid(column=1)
    Label3=Label(Frame2,text="Hola3", borderwidth=num//2, relief="raised").grid(column=2)


  

    root.mainloop()

if __name__ == "__main__":
    interfaz()
    