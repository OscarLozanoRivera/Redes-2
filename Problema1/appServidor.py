# !/usr/bin/env python3

__author__ = "Oscar Lozano Rivera"

import logging
import socket
import threading
import pickle
import time
from datetime import datetime
from concurrent import futures
import time
import logging

import grpc
import wave
import pyaudio
import audio_pb2
import audio_pb2_grpc
import speech_recognition as sr

listaJugadores = []
jugadorActual = None
ganador = None
horaInicio = None
horaFin = None

turno=1

state = False
transformacion= ""
resp = True
nombre = ""
texto = ""

p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt32
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "Problema1/serverAudio/recibido.wav"

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
    {'nombre':'Gunther',
     'genero':'hombre',
     'estatura':'pequeño',
     'articuloCabeza':'gorra',
     'ropa':'short',
     'zapatos':'vikingos'
    },
    {'nombre':'Helga',
     'genero':'mujer',
     'estatura':'alta',
     'articuloCabeza':['diadema','banda'],
     'ropa':'falda',
     'zapatos':'botas'
    },
    {'nombre':'Honey',
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
    {'nombre':'Kick',
     'genero':'hombre',
     'estatura':'pequeño',
     'articuloCabeza':'casco',
     'ropa':'overol',
     'zapatos':'botas'
    },
    {'nombre':'Magnus',
     'genero':'hombre',
     'estatura':'alto',
     'articuloCabeza':'casco',
     'ropa':'falda',
     'zapatos':'botas'
    },



]

def audioATexto():
    r = sr.Recognizer()
    with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
            info_audio=r.record(source)
            try:
                textoGoogle = r.recognize_google(info_audio,language="es-ES")
            except:
                textoGoogle="Sorry could not hear"
                print('')
    return textoGoogle

def encontrarCoincidencia():
    pass



class Audio(audio_pb2_grpc.AudioServicer):

    def iniciarJuego(self, request, context):
        logging.debug("Servicio iniciarJuego")
        listaJugadores.append(request.nombreJugador)
        logging.debug("%s está jugando con num %s",listaJugadores[-1],len(listaJugadores))
        return audio_pb2.lista(nombreJugador=request.nombreJugador, numeroJugador=len(listaJugadores))

    def terminarJuego(self, request, context):
        logging.debug("Servicio terminarJuego")
        print(listaJugadores)
        listaJugadores.remove(request.nombreJugador)
        print(listaJugadores)
        return audio_pb2.nombre(nombreJugador=request.nombreJugador)

    def actualizarJuego(self, request, context):
        if request.numeroJuego == turno:
            state=True

        else:
            state=False
        logging.debug("Servicio actualizarJuego")
        return audio_pb2.respuestaPersonaje(estado=state,
                                            textoAudio=transformacion,
                                            respuesta=resp,
                                            nombre=None,
                                            textoPartida=texto)

    def recibirAudio(self, request_iterator, context):
        logging.debug("Servicio recibirAudio")
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
        resp=encontrarCoincidencia()
        logging.debug(transformacion)
        return audio_pb2.respuestaPersonaje(estado=state,
                                            textoAudio=transformacion,
                                            respuesta=resp,
                                            nombre=None,
                                            textoPartida=texto)

    """def SaludaAMisAmigosEnVariosIdiomas(self, request_iterator, context):
        for request in request_iterator:
            for idiom in listaJugadores:
                yield audio_pb2.RespuestaSaludo(saludo=idiom + ', %s!' % request.nombre)
    """


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

