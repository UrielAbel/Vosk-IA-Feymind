#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import json
import glob
from tqdm import tqdm

SetLogLevel(0)

# Corroboramos que exista el modelo.
if not os.path.exists("modelo"):
    print ("Hubo un error con el modelo, fijate que esté cargado bien.")
    exit (1)

# Inicializamos el modelo.
model = Model("modelo")

# Definimos función de transcripción
def transcribe_wav(full_filename):
    # Abrimos el audio para extraer la información
    wf = wave.open(full_filename, "rb")
    # Verificamos que esté correcto para empezar.
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("El audio tiene que ser en formato WAV mono PCM.")
        exit (1)
    
    # Le damos inicio a la IA
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    # Solamente crea o revisa si está el archivo en donde quedará la transcripción.
    filename = os.path.join('resultados',os.path.splitext(os.path.basename(full_filename))[0] + ".txt")
    filename = filename.replace('\\', '/')

    # Acá va palabra por palabra transcribiendo lo que escucha.
    with open(filename, 'w+') as f:
        line_no = 0
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                
                line = json.loads(rec.Result())["text"]
                f.write(line + "\n")
                print(f"Se escribió linea número {line_no} en {filename}")
                line_no += 1
                
            else:
                pass
        f.write(json.loads(rec.FinalResult())["text"])

if __name__=='__main__':
    # Esto nomás es para agarrar todos los archivos Wav dentro de la carpeta Interview_audio
    filenames = glob.glob("audios/*.wav")
    filenames = [f.replace('\\', '/') for f in filenames]
    filenames.sort()
    if len(filenames) == 0:
        print("Fijate que no hay un audio WAV en la carpeta ./audios")
    else:
        print(filenames)
        for f in tqdm(filenames):
            transcribe_wav(f)
        print("finished")
