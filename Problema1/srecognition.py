import speech_recognition as sr
archivoAudio="Problema1/audioprueba.wav"
r = sr.Recognizer() 

with sr.AudioFile(archivoAudio) as source:
    print('Leyendo archivo de audio : ')
    info_audio=r.record(source)
    try:
        text = r.recognize_google(info_audio,language="es-ES")
        print('Dijiste: {}'.format(text))
    except:
        print('Sorry could not hear')