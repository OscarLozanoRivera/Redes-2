# !/usr/bin/env python3
__author__ = "Oscar Lozano Rivera"

import pickle
from re import T
import socket
import json

#DNS Puerto 53
HOST = "192.168.0.17"  # El hostname o IP del servidor
PORT = 54321  # El puerto usado por el servidor
ipServerRaiz = [("192.168.0.17", 54321)]
bufferSize = 1024
datos=[]

def llamarRaiz(url):  
    for serverAddress in ipServerRaiz:
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as UDPClientSocket:
            # Enviando mensaje al servidor raiz (root)
                buscarIP = str.encode(url)
                try:
                    UDPClientSocket.sendto(buscarIP, serverAddress)
                    msgFromServer,server = UDPClientSocket.recvfrom(bufferSize)
                except Exception as e:
                    #print("Exception: ",e)
                    return []
                else:
                    msgFromServer=pickle.loads(msgFromServer)
                    if msgFromServer!=[]:
                        return msgFromServer                 

def llamarTDL(url,port):  #ip=port
    msgFromServer=[]
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as UDPClientSocket:
        # Enviando mensaje al servidor TDL indicado
            buscarIP = str.encode(url)
            try:
                UDPClientSocket.sendto(buscarIP, ("127.0.0.1", port))   #(ip,53)
                msgFromServer,server = UDPClientSocket.recvfrom(bufferSize)
            except Exception as e:
                #print("Exception: ",e)
                return []
            else:            
                msgFromServer=pickle.loads(msgFromServer)
                if msgFromServer!=[]:
                    return msgFromServer 
    return msgFromServer 

def llamarAutoritario(url,port):  #ip=port
    msgFromServer=[]
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as UDPClientSocket:
        # Enviando mensaje al servidor Autoritario indicado
            buscarIP = str.encode(url)
            try:
                UDPClientSocket.sendto(buscarIP, ("127.0.0.1", port))   #(ip,53)
                msgFromServer,server = UDPClientSocket.recvfrom(bufferSize)
            except Exception as e:
                print("Exception: ",e)
                return []
            else:            
               
                msgFromServer=pickle.loads(msgFromServer)
                if msgFromServer!=[]:
                    return msgFromServer 
    return msgFromServer 

def Resolver(buscar):
    ipsEncontradas=[]
    ipsTDL=llamarRaiz(buscar)
    #print("Raiz Dev:",ipsTDL)
    for ip in ipsTDL:   #ip-> port
        #print("TDL:",ip)
        ipsAut=llamarTDL(buscar,int(ip))
        #print("TDL Dev:",ipsAut)
        for ipA in ipsAut:
            #print("Aut:",int(ipA))
            ipsEncontradas=llamarAutoritario(buscar,int(ipA))
            if ipsEncontradas!=[]:
                #print("Aut Dev:",ip)
                return ipsEncontradas
    return ipsEncontradas
    
def imprimirIPs(ips):
    print("Adresses:",end="\t")
    for ip in ips:
        print(ip,end="\n\t\t")


if __name__ == "__main__":
    print("Buscador DNS:")
    #input("Comenzar?")
    while(True):
        resolver=True
        print("\n>> ",end="")
        buscar=input()
        if buscar=='exit':
            break
        splits=buscar.split('.')
        if len(splits)==2:
            print("Comando reconocido")  
        else:
            print("Comando no reconocido")
            next
        # Buscar en Caché
        with open("Practica4/CacheCliente.json","r") as cache:        
            datos=json.load(cache)
        for ip in datos:
            if ip['Dominio']==buscar:
                print("Previamente registrado")
                imprimirIPs(ip['IPs'])
                resolver=False
                break
        if resolver:
            # Resolver
            ips=Resolver(buscar)
            if ips!=[]:
                datos.append({'Dominio':buscar,'IPs':ips})
                with open("Practica4/CacheCliente.json","w") as cache:        
                    json.dump(datos,cache)
                imprimirIPs(ips)
                
            else:
                print("No se encontraron coincidencias")
        
        

