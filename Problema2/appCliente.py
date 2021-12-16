
import logging
from tkinter.constants import INSERT

import grpc
import balanceador_pb2
import balanceador_pb2_grpc
from tkinter import StringVar, Text, Tk, Entry, Label, Button, END

def mensaje(stub,textEntry):
    response = stub.recibirOrden(balanceador_pb2.peticion(mensaje=textEntry.get()))
    print(response.mensajeRespuesta)
    textEntry.set(response.mensajeRespuesta)

def GUI():
    channel = grpc.insecure_channel('192.168.0.24:50051')
    stub = balanceador_pb2_grpc.BalanceoStub(channel)
    global root
    root = Tk()
    # Icono Aplicación
    ancho_ventana = 250
    alto_ventana = 160
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + \
        "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.resizable(False, False)
    root.title("Conexión")

    def limpiar():
        textEntry.set('')

    textEntry= StringVar()
    Label(root, text="Escribe tu nombre").grid(row=0, columnspan=4, sticky="ew", padx=5, pady=10)
    texto = Entry(root, textvariable=textEntry, width=38)
    texto.grid(row=1, columnspan=4, sticky="ew", padx=5, pady=10)
    Button(root, command=lambda: mensaje(stub,textEntry),text="Enviar mensaje").grid(row=2, column=0, columnspan=2, padx=5, pady=10)
    Button(root, command=limpiar ,text="Limpiar").grid(row=2, column=3, columnspan=2, padx=5, pady=10)
    root.mainloop()
    




if __name__ == '__main__':
    logging.basicConfig()
    GUI()
