from flask import Flask
#import simpleaudio as sa
import serial

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/<instrument>")
def startNotes(instrument):
    print(instrument)
    path = "./Assets/Notes/"
    pianoNotes = {
        "C4": path + "C.wav",
        "D4": path + "D.wav",
        "E4": path + "E.wav",
        "F4": path + "F.wav",
        "G4": path + "G.wav",
        "A4": path + "A.wav",
        "B4": path + "B.wav",
        "C5": path + "C1.wav",
    }

    #Start reading serial

    wave_obj = sa.WaveObject.from_wave_file(pianoNotes.get("C4"))
    play_obj = wave_obj.play()
    wave_obj = sa.WaveObject.from_wave_file(pianoNotes.get("D4"))
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing


def serial_input():
    ser = serial.Serial('COM3')
    ser.flushInput()

    while True:
        try:
            ser_bytes = ser.readline()
            ser_bytes = ser_bytes.decode()
            print(ser_bytes)
        except:
            print("Keyboard Interrupt")
            break

serial_input()
