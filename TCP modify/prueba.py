#!/usr/bin/env python3
"""
# Define the list
listdata = [1,0,0]
for a in range(0,2):
  listdata.append(0)
# Print the content of the list
print("\nThe dictionary values are :\n", listdata)
 
# Initialize bytearray object with list
byteArrayObject = bytearray(listdata)
# Print bytearray object value
print("\nThe output of bytearray() method :\n", byteArrayObject)
 
# Convert the bytearray object into  bytes object
byteObject = bytes(byteArrayObject)
# Print bytes object value
print("\nThe output of bytes() method :\n", byteObject)
 
print("\nThe ASCII values of bytes")
# Iterate the bytes object using loop
for val in byteObject:
  print(val,' ', end='')
 
print("\nThe string values of bytes")
# Iterate the bytes object using loop
for val in byteObject:
  print(chr(val),' ', end='')

"""
"""
gridGato=[[0,0,1],[1,0,1],[1,0,0]]

import tkinter 
from tkinter import Tk

def sendPosition(i,e):
    print(i,e)

class boton:
  def __init__(self,i,e) -> None:
      botonnuevo=tkinter.Button(frame,text=" ")
      botonnuevo.grid(row=i,column=e)
      botonnuevo.config(command=lambda:sendPosition(i,e))

root = Tk()
root.geometry("400x400+300+300")

root.title("Practica 1")
frame=tkinter.Frame(root)
frame.pack()
botones=[]
for i,a in enumerate(gridGato):
    for e,b in enumerate(a):
        botones.append(boton(i,e))
        
root.mainloop()
"""

tablero=[[1,1,2],[1,1,2],[3,1,2]]
for i,tab in enumerate(tablero):
  print(0 in tab,end="\t ")
  print(i, len(tablero))
  if 0 in tab:
      break
  elif i==len(tablero):
      print("No hay ceros")
      break
print("Hay ceros")