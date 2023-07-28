import serial
import pyttsx3
import serial
import time 

engine = pyttsx3.init()

# set the properties of the voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # set the voice to the second one

def say(text):
    engine.say(text)
    engine.runAndWait()

#reading tag from serial monitor
def fingerPrint():
    serial_port = serial.Serial('COM8', 9600)
    data = serial_port.readline().decode('utf-8').rstrip()
    if int(data) == 1:
        return 1
    else:
        return 0
    
def fingerPrintRec():
    if(fingerPrint()):
        return 1
    else:
        say("FingerPrint Not verified. Please Try Again")
        if(fingerPrint()):
            return 1
        else:
            say("FingerPrint Not verified. Please Try Again")
            if(fingerPrint()):
                return 1
    return 0
