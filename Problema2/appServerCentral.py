from concurrent import futures
import grpc, balanceador_pb2, balanceador_pb2_grpc, socket

bufferSize = 1024
ips=[
    ("127.0.0.1" ,50061),
    ("127.0.0.1" ,50062),
    ("127.0.0.1" ,50063)
]

class Balanceo(balanceador_pb2_grpc.BalanceoServicer):

    def recibirOrden(self, request, context):
        msgFromServer="No se pudo encontrar servidor disponible"
        contador=0
        errores=0
        while True:  
            ip=ips.pop(0)
            ips.append(ip)
            try:
                with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as UDPClientSocket:
                    msgToSend=str.encode(request.mensaje)     
                    UDPClientSocket.sendto(msgToSend, ip)
                    UDPClientSocket.settimeout(5)
                    msgFromServer,server = UDPClientSocket.recvfrom(bufferSize)
                    print(msgFromServer)
                    break
            except Exception as e:
                print("No se pudo contactar al servidor: ",ip)
                if contador==3: break
            finally: contador+=1
        return balanceador_pb2.respuesta(mensajeRespuesta=msgFromServer)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    balanceador_pb2_grpc.add_BalanceoServicer_to_server(Balanceo(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor Central en Operación")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
