
import socket, sys
BUFFERSIZE=1024 
HOST="127.0.0.1"            
PORT=50061+int(sys.argv[1])           
bufferSize = 1024


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as UDPServerSocket:
    UDPServerSocket.bind((HOST, PORT))
    print("Servidor Final 1, esperando peticiones:")
    # Listen for incoming datagrams
    while (True):
        mensaje, address = UDPServerSocket.recvfrom(bufferSize)
        mensaje=mensaje.decode()
        print("Nombre del cliente: ",mensaje)
        mensaje="Hola "+mensaje+", te saluda F"+ str(sys.argv[1])
        print("Mensaje a  enviar al cliente: ",mensaje)
        dataToSend=str.encode(mensaje)
        UDPServerSocket.sendto(dataToSend, address)