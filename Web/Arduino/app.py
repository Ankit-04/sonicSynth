from flask import Flask
import simpleaudio as sa
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

    guitarNotes = {
        "C4": path + "C_Guitar.wav",
        "D4": path + "D_Guitar.wav",
        "E4": path + "E_Guitar.wav",
        "F4": path + "F_Guitar.wav",
        "G4": path + "G_Guitar.wav",
        "A4": path + "A_Guitar.wav",
        "B4": path + "B_Guitar.wav",
    }

    xylophoneNotes = {
        "C4": path + "C_Drum.wav",
        "D4": path + "D_Drum.wav",
        "E4": path + "E_Drum.wav",
        "F4": path + "F_Drum.wav",
        "G4": path + "G_Drum.wav",
        "A4": path + "A_Drum.wav",
        "B4": path + "B_Drum.wav",
        "C5": path + "C1_Drum.wav",
    }

    #Start reading serial
    if(instrument == "Piano"):
        wave_obj = sa.WaveObject.from_wave_file(pianoNotes.get("C4"))
        play_obj = wave_obj.play()
        wave_obj = sa.WaveObject.from_wave_file(pianoNotes.get("D4"))
        play_obj = wave_obj.play()
    elif instrument == "Xylophone":
        wave_obj = sa.WaveObject.from_wave_file(xylophoneNotes.get("C4"))
        play_obj = wave_obj.play()
        wave_obj = sa.WaveObject.from_wave_file(xylophoneNotes.get("D4"))
        play_obj = wave_obj.play()
    else:
        wave_obj = sa.WaveObject.from_wave_file(guitarNotes.get("C4"))
        play_obj = wave_obj.play()
        play_obj = wave_obj.play()


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

