# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"

import threading, time, logging, grpc, wave, pyaudio, audio_pb2, audio_pb2_grpc
from tkinter.constants import NO, NONE
import speech_recognition as sr
from re import T, search
from datetime import datetime
from concurrent import futures
from tkinter import READABLE
from random import randint

listaJugadores = []
ganador = None
horaInicio = None
horaFin = None
personajeNum= None
turno=1

state = False
ultimoJugador=None
transformacion= "Iniciando"
resp = False
nombre = ""
texto = "Juego en curso"

p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "Problema1/serverAudio/recibido.wav"
NUM_THREADS = 2
barrier = threading.Barrier(NUM_THREADS)    #Barrera
lock = threading.Lock()                     #Candado

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(threadName)-10s) %(message)s',
)
 
personajes=[
    {'nombre':'Billy',
     'genero':'hombre',
     'estatura':'alto',
     'articuloCabeza':'gorra',
     'ropa':'pantalón',
     'zapatos':'botas'
    },
    {'nombre':'Brad',
     'genero':'hombre',
     'estatura':'alto',
     'ropa':'pantalón',
     'zapatos':'tennis'
    },
    {'nombre':'Briana',
     'genero':'mujer',
     'estatura':'pequeña',
     'articuloCabeza':['tiara','corona'],
     'ropa':'pantalón',
     'zapatos':'botas'
    },
    {'nombre':'odín',
     'genero':'hombre',
     'estatura':'pequeño',
     'articuloCabeza':'gorra',
     'ropa':'shorts',
     'zapatos':'vikingos'
    },
    {'nombre':'Astrid',
     'genero':'mujer',
     'estatura':'alta',
     'articuloCabeza':['diadema','banda'],
     'ropa':'falda',
     'zapatos':'botas'
    },
    {'nombre':'Adriana',
     'genero':'mujer',
     'estatura':'alto',
     'ropa':'pantalón',
     'zapatos':'zapatos'
    },
    {'nombre':'Jackie',
     'genero':'hombre',
     'estatura':'alto',
     'articuloCabeza':'gorro',
     'ropa':'pantalón',
     'zapatos':'tennis'
    },
    {'nombre':'Kendall',
     'genero':'mujer',
     'estatura':'alta',
     'articuloCabeza':['diadema','banda'],
     'ropa':'falda',
     'zapatos':'zapatos'
    },
    {'nombre':'kik',
     'genero':'hombre',
     'estatura':'pequeño',
     'articuloCabeza':'casco',
     'ropa':'overol',
     'zapatos':'botas'
    },
    {'nombre':'magnus',
     'genero':'hombre',
     'estatura':'alto',
     'articuloCabeza':'casco',
     'ropa':'falda',
     'zapatos':'botas'
    },
]

def iniciarVariables():
    global ganador
    if ganador is not None:
        global listaJugadores 
        listaJugadores = []
        
        ganador = None
        global horaInicio
        horaInicio = None
        global horaFin
        horaFin = None
        global personajeNum
        personajeNum= None
        global turno
        turno=1
        global state
        state = False
        global ultimoJugador
        ultimoJugador
        global transformacion
        transformacion= "Iniciando"
        global resp
        resp = False
        global nombre
        nombre = ""
        global texto
        texto = "Juego en curso"


def elegirPersonaje():
    global personajeNum
    global personajes
    personajeNum= randint(0, 9)
    logging.debug(personajes[personajeNum])

def audioATexto():
    r = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
            info_audio=r.record(source)
            try:
                textoGoogle = r.recognize_google(info_audio,language="es-ES")
            except:
                textoGoogle="°__°"
    if textoGoogle=="Iniciando":  return "°__°"
    return textoGoogle

def adivinaPersonaje():
    global personajes
    global personajeNum
    #logging.debug("Intentando")
    for personaje in personajes:
        #print(personaje['nombre'] , personajes[personajeNum]['nombre'])
        if search(personaje['nombre'], transformacion) is not None:
            #print(personaje['nombre'] , personajes[personajeNum]['nombre'])
            if personaje['nombre']==personajes[personajeNum]['nombre']:
                #print("Peronaje encontrado: %s",personaje['nombre'] )
                return True
    return False
def encontrarCoincidencia():
    global personajes
    característica=None
    if search('es', transformacion) is not None:
        if search('hombre', transformacion) is not None: característica='hombre'
        if search('mujer', transformacion) is not None: característica='mujer'
        #logging.debug("Genero %s",personajes[personajeNum]['genero'])
        if personajes[personajeNum]['genero']==característica:   return True
    if search('tiene', transformacion) is not None or search('usa', transformacion) is not None:
        try:
            if search('algo', transformacion) is not None and (search('cabeza', transformacion) is not None or search('pelo', transformacion) is not None ):
                if len(personajes[personajeNum]['articuloCabeza'])>0:
                    return True
        except: pass
        
        if search('gorra', transformacion) is not None: característica='gorra'
        elif search('gorro', transformacion) is not None: característica='gorro'
        elif search('casco', transformacion) is not None: característica='casco'
        elif search('diadema', transformacion) is not None or search('diadema', transformacion) is not None : característica='diadema'
        elif search('tiara', transformacion) is not None or search('corona', transformacion) is not None : característica='tiara'
        else:
            if search('pantalón', transformacion) is not None: característica='pantalón'
            elif search('falda', transformacion) is not None: característica='falda'
            elif search('shorts', transformacion) is not None: característica='shorts'
            elif search('overol', transformacion) is not None: característica='overol'
            #logging.debug("Ropa %s",personajes[personajeNum]['ropa'])
            if personajes[personajeNum]['ropa']==característica:   return True
            else: 
                if search('zapatos', transformacion) is not None: característica='zapatos'
                elif search('botas', transformacion) is not None: característica='botas'
                elif search('vikingos', transformacion) is not None: característica='vikingos'
                #logging.debug("Zapatos %s",personajes[personajeNum]['zapatos'])
                if personajes[personajeNum]['zapatos']==característica:   return True
        try:
            if len(personajes[personajeNum]['articuloCabeza'])==2:
                for articulo in personajes[personajeNum]['articuloCabeza']:
                    #logging.debug("Cabeza %s",articulo)
                    if articulo == característica: return True
            else:
                if personajes[personajeNum]['articuloCabeza'] == característica: return True
        except:
            pass
    if search('alt', transformacion) is not None or search('pequeñ', transformacion) is not None:
        if search('alt', transformacion) is not None: característica='alt'
        else: característica='pequeñ'
        logging.debug("Estatura %s",personajes[personajeNum]['estatura'])
        if personajes[personajeNum]['estatura'][:-1]==característica:   return True

    return False

class Audio(audio_pb2_grpc.AudioServicer):

    def iniciarJuego(self, request, context):
        iniciarVariables()
        global personajeNum
        logging.debug("Servicio iniciarJuego para %s",request.nombreJugador)
        listaJugadores.append(request.nombreJugador)
        barrier.wait()
        lock.acquire()
        if personajeNum == None:
            elegirPersonaje()
        lock.release()
        logging.debug("%s está jugando con num %s",request.nombreJugador,listaJugadores.index(request.nombreJugador)+1)
        return audio_pb2.lista(nombreJugador=request.nombreJugador, numeroJugador=listaJugadores.index(request.nombreJugador)+1)

    def terminarJuego(self, request, context):
        logging.debug("Servicio terminarJuego para %s",request.nombreJugador)
        listaJugadores.remove(request.nombreJugador)
        return audio_pb2.nombre(nombreJugador=request.nombreJugador)

    def actualizarJuego(self, request, context):
        global turno
        global transformacion
        global ganador
        logging.debug("%s solicita actualizacion, esta en posicion %s",request.nombreJugador,request.numeroJugador)
        while True:
            lock.acquire()
            if turno==request.numeroJugador:

                break               
            else:
                lock.release()
                time.sleep(.1) 
        logging.debug("Servicio actualizarJuego para %s",request.nombreJugador)
        lock.release()
        texto=""
        if ganador:
            texto="Lo siento perdiste , ganó: "+ ultimoJugador
            logging.debug("Partida terminada %s para ganó %s", request.nombreJugador ,ultimoJugador)
        else:
            texto="Tu turno "+str(request.numeroJugador)
        return audio_pb2.respuestaPersonaje(estado=state,
                                            textoAudio=transformacion,
                                            respuesta=resp,
                                            nombre=ultimoJugador,
                                            textoPartida=texto)

    def recibirAudio(self, request_iterator, context):
        global turno
        global transformacion
        global ultimoJugador
        global resp
        global state
        global texto
        global ganador
        ultimoJugador=listaJugadores[turno-1]
        logging.debug("Servicio recibirAudio para %s", ultimoJugador)
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        frames = []
        contador = 0
        for request in request_iterator:
            frames.append(request.chunk) 
        wf.writeframes(b''.join(frames))     
        wf.close()
        transformacion=audioATexto()
        ganador=adivinaPersonaje()
        if not ganador:
            resp=encontrarCoincidencia()
        else:
            logging.debug("Partida terminada para %s ganó %s", ultimoJugador, ultimoJugador)
            resp=ganador
            state=True
            texto="Felicidades Ganaste!" 
        if turno==2: turno-=1
        else: turno+=1
        return audio_pb2.respuestaPersonaje(estado=state,
                                            textoAudio=transformacion,
                                            respuesta=resp,
                                            nombre=ultimoJugador,
                                            textoPartida=texto)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))
    audio_pb2_grpc.add_AudioServicer_to_server(Audio(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.debug("Adivina Quien")
    logging.debug("Servidor RPC Activo")
    serve()

