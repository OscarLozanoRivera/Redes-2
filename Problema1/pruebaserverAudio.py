import socket
import threading, wave, pyaudio,pickle,struct

host_name = socket.gethostname()
host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
print(host_ip)
port = 12345

def audio_stream():
    server_socket = socket.socket()
    server_socket.bind((host_ip, (port-1)))

    server_socket.listen(5)
    CHUNK = 1024
    wf = wave.open("Problema1/audioprueba.wav", 'rb')
    
    p = pyaudio.PyAudio()
    print('server listening at',(host_ip, (port-1)))
   
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    input=True,
                    frames_per_buffer=CHUNK)

             

    client_socket,addr = server_socket.accept()
 
    data = None
    while True:
        data = wf.readframes(CHUNK)
        if data==b'':
            print(type(data2))
            message = pickle.dumps([])
            client_socket.sendall(message)
            break
        data2=data
        
        message = pickle.dumps(data)
        print(type(message))
        print(len(message))
        client_socket.sendall(message)
                
t1 = threading.Thread(target=audio_stream, args=())
t1.start()
