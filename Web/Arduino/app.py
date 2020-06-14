from flask import Flask
import simpleaudio as sa
import serial
import mingus.extra.lilypond as lilypond
import mingus
import threading
from multiprocessing import Process

app = Flask(__name__)
app.config["DEBUG"] = True

path = "./Assets/Notes/"
ser = serial.Serial('COM3')

pianoNotes = {
    "C": path + "C.wav",
    "D": path + "D.wav",
    "E": path + "E.wav",
    "F": path + "F.wav",
    "G": path + "G.wav",
    "A": path + "A.wav",
    "B": path + "B.wav",
    "H": path + "C1.wav"
}

guitarNotes = {
    "C": path + "C_Guitar.wav",
    "D": path + "D_Guitar.wav",
    "E": path + "E_Guitar.wav",
    "F": path + "F_Guitar.wav",
    "G": path + "G_Guitar.wav",
    "A": path + "A_Guitar.wav",
    "B": path + "B_Guitar.wav",
}

xylophoneNotes = {
    "C": path + "C_Drum.wav",
    "D": path + "D_Drum.wav",
    "E": path + "E_Drum.wav",
    "F": path + "F_Drum.wav",
    "G": path + "G_Drum.wav",
    "A": path + "A_Drum.wav",
    "B": path + "B_Drum.wav",
    "H": path + "C1_Drum.wav"
}
def serial_input():
    t = threading.currentThread()
    while True:
        if(not getattr(t, "do_run")):
            continue
        try:
            ser_bytes = ser.readline()
            ser_bytes = ser_bytes.decode()
            ser_bytes.rstrip()
            ser_bytes = str(ser_bytes)
            if(len(ser_bytes) >= 1):
                ser_bytes = ser_bytes[0]
            else:
                continue
            instrument = getattr(t, "instrument", "Piano")
            if instrument == "Piano":
                wave_obj = sa.WaveObject.from_wave_file(pianoNotes.get(ser_bytes[0]))
                play_obj = wave_obj.play()  
            elif instrument == "Xylophone":
                wave_obj = sa.WaveObject.from_wave_file(xylophoneNotes.get(ser_bytes[0]))
                play_obj = wave_obj.play()
            else:
                wave_obj = sa.WaveObject.from_wave_file(guitarNotes.get(ser_bytes[0]))
                play_obj = wave_obj.play()

        except KeyboardInterrupt:
            break

x = threading.Thread(target=serial_input)

@app.before_first_request
def startThread():
    x.do_run = False
    x.start()
    
@app.route('/stop')
def stopPlaying():
    ser.flushInput()
    print(x.isAlive())
    x.do_run = False
    print(x.isAlive())
    return "stopped"

@app.route("/<instrument>")
def startNotes(instrument):
    print(instrument)
    ser.flushInput() 
    x.do_run = True   
    x.instrument = instrument
    return "playing"



