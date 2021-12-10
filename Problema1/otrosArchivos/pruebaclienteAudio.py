# Welcome to PyShine
# This is client code to receive video and audio frames over TCP

import socket,os
import threading, wave, pyaudio, pickle,struct
host_name = socket.gethostname()
host_ip = '127.0.0.1'#  socket.gethostbyname(host_name)
print(host_ip)
port = 12345

CHUNK = 1024
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "Problema1/serverAudio/recibido.wav"




def audio_stream():
	
	p = pyaudio.PyAudio()
	CHUNK = 1024
					
	# create socket
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	socket_address = (host_ip,port-1)
	print('server listening at',socket_address)
	client_socket.connect(socket_address) 
	print("CLIENT CONNECTED TO",socket_address)
	data = b""
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	frames=[]
	try:
		while True:
			packet = client_socket.recv(4144) # 4K
			if not packet: 
				print("Terminado")
				break
			frame = pickle.loads(packet)
			if frame==[]:
				break
			print(len(frame))
			print(type(frame))
			frames.append(frame)
	except Exception as e:
			print(e)
	print(frame)
	wf.writeframes(b''.join(frames))
	wf.close()
	client_socket.close()
	print('Audio closed')
	os._exit(1)
	
t1 = threading.Thread(target=audio_stream, args=())
t1.start()

