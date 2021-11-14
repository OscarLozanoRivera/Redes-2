# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"

import pathlib
import json

"""
directorio = pathlib.Path('Practica4/ServerAutoritativo/13245')
ls=[]
for fichero in directorio.iterdir():
    ls.append(fichero.name)
ls2=[]
for f in ls:
    splits=f.split(".")
    ls2.append(splits[0]+"."+splits[1])
print(ls2)
"""
buscar=[]
PORT=15243
data='ipn.mx'
ipsEncontradas=[]
with open("Practica4/ServerAutoritativo/"+str(PORT)+"/"+str(data)+".json","r") as archivo:
    datos=json.load(archivo)
    for ip in datos['Master']:
        print(ip['Type'])
        if ip['Type']=="A":
            ipsEncontradas.append(ip['Address'])
print(ipsEncontradas)