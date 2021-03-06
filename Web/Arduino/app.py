from flask import Flask
from flask import send_file, send_from_directory, safe_join, abort
from flask_cors import CORS
import simpleaudio as sa
import serial
import mingus.extra.lilypond as lilypond
import mingus
import threading
from multiprocessing import Process
import time

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)
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
    while True:
        if(not getattr(x, "do_run")):
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
            instrument = getattr(x, "instrument", "Piano")
            if(ser_bytes == "H"):
                x.notes.append("C-5")
            else:
                x.notes.append(ser_bytes)
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
    x.do_run = False
    n = getattr(x, "notes")
    b = mingus.containers.Bar()
    track = mingus.containers.Track()
    if(len(n) == 0): 
        return "No file"
    for i in n:
        track.add_notes(i)
    trackString = lilypond.from_Track(track)
    lilypond.to_png(trackString, "MasterPiece" + str(len(n)))
    time.sleep(3)
    filename = 'MasterPiece' + str(len(n)) + '.png'
    return send_file(filename, mimetype='image/PNG') 

@app.route("/<instrument>")
def startNotes(instrument):
    print(instrument)
    ser.flushInput() 
    x.do_run = True   
    x.instrument = instrument
    x.notes = []
    return "playing"



def testingLilypond():
    n = ["A", "B", "C","A", "B", "D","D", "D", "E","A", "B", "C","A", "B", "C","A", "B", "C","A", "B", "C","A", "B", "C", "C-5"]
    b = mingus.containers.Bar()
    track = mingus.containers.Track()
    for i in n:
        track.add_notes(i)
    trackString = lilypond.from_Track(track)
    lilypond.to_pdf(trackString, "Piece")
