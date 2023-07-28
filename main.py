import face_recognition as faceRegLib
import pyttsx3
import pyrebase
import cv2
import numpy as np
import serial
import os
import time
from faceRec import faceRecognition as fr 
from fingerRec import fingerPrintRec as fnr
from locationRec import verify_location as vl
import webbrowser
#IMPORT SYSTEM FILES
import argparse
import scipy.io.wavfile as wavfile
import traceback as tb
import os
import sys
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, euclidean, cosine 
import warnings
from keras.models import load_model
import logging
logging.basicConfig(level=logging.ERROR)
warnings.filterwarnings("ignore")
import os
import speech_recognition as sr
import pyttsx3
import time
from flask import Flask, render_template, request, redirect, url_for
import webbrowser
# from app import app


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)
#IMPORT USER-DEFINED FUNCTIONS
from feature_extraction import get_embedding, get_embeddings_from_list_file
from preprocess import get_fft_spectrum
import parameters as p
MODEL_FILE = r"C:\Users\LENOVO\OneDrive\Desktop\idp\voice_auth_model_cnn\saved_model.pb"

def recognize_from_voice():

    # initialize recognizer
    # r = sr.Recognizer()
    r = sr.Recognizer()
    mic = sr.Microphone()
    engine = pyttsx3.init()

    # Obtain voice sample for enrollment
    with mic as source:
        print("Please say a few words to recognize your voice.")
        engine.say("Please say a few words to recognize your voice")
        engine.runAndWait()
        time.sleep(1)
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        file = r"C:\Users\LENOVO\OneDrive\Desktop\idp\enroll1.wav"
        with open(file, "wb") as f:
            f.write(audio.get_wav_data())
        time.sleep(2)

        engine = pyttsx3.init()
        
        embeds = os.listdir(p.EMBED_LIST_FILE)

        model = load_model(p.MODEL_FILE)

            
        distances = {}

        test_result = get_embedding(model, file, p.MAX_SEC)
        test_embs = np.array(test_result.tolist())
        for emb in embeds:
            enroll_embs = np.load(os.path.join(p.EMBED_LIST_FILE,emb))
            speaker = emb.replace(".npy","")
            distance = euclidean(test_embs, enroll_embs)
            distances.update({speaker:distance})
        if min(list(distances.values()))<p.THRESHOLD:
            say(min(distances, key=distances.get))
            say("Your Voice has been verified")
            return 1
            
        else:
            exit()



# initialize the text-to-speech engine
engine = pyttsx3.init()

# set the properties of the voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # set the voice to the second one

def say(text):
    engine.say(text)
    engine.runAndWait()


#reading tag from serial monitor
serial_port = serial.Serial('COM7', 9600)
counter = 0 
img_name= ""

while counter < 3:
    data = serial_port.readline().decode('utf-8').rstrip()
    if counter == 0:
        say(data)

    if(counter == 1):
        img_name = data[10:12]

    if(counter == 2):
        say(data[7:])

    counter += 1

#creating list of images in the storage

dir="C:/Users/LENOVO/OneDrive/Desktop/idp/images"

images = os.listdir(dir)

img_name = img_name + ".jpg"

if img_name in images:

    say("Get ready for image verification")

    time.sleep(5)

    imgLoc = r"C:\Users\LENOVO\OneDrive\Desktop\idp\images\{}".format(img_name)

    #face verification
    if(fr(imgLoc)):
        say("Face Verified")
        
        time.sleep(5)

        #fingerprint verification
        
        say("Put your thumb on the sensor for fingerprint verification")
        ser = serial.Serial('COM8', 9600)
        time.sleep(2)
        ser.write(b'1')
        time.sleep(7)
        ser.close()
        time.sleep(2)

        if(fnr()):
            say("Fingerprint Verified")
            time.sleep(2)

            #location verification
            say("Verifying Your Location. Please Open the Location app on the phone")
            time.sleep(20)
            if(vl()):
                say("Your location has been verified")
                time.sleep(2)
                #speech - verification
                if(recognize_from_voice()):
                    url = 'http://127.0.0.1:5000'  # the URL of your Flask app
                    webbrowser.open_new(url)  # open the URL in the default web browser

                    # if __name__ == "__main__":
                    #     app.run()

                else:
                    say("Voice Not verified")
            else:
                say("Location Not Verified")

        else:
            say("You have attempted 3 times. You can try again later")

    else:
        say("Face Not Verified. Try again later")
else:
    say("User Not Found")