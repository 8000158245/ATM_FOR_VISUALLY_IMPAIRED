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
import pyttsx3
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)
#IMPORT USER-DEFINED FUNCTIONS
from feature_extraction import get_embedding, get_embeddings_from_list_file
from preprocess import get_fft_spectrum
import parameters as p

def enroll(name,file):
    """Enroll a user with an audio file
        inputs: str (Name of the person to be enrolled and registered)
                str (Path to the audio file of the person to enroll)
        outputs: None"""

    print("Loading model weights from [{}]....".format(p.MODEL_FILE))
    try:
        model = load_model(p.MODEL_FILE)
    except:
        print("Failed to load weights from the weights file, please ensure *.pb file is present in the MODEL_FILE directory")
        exit()
    
    try:
        print("Processing enroll sample....")
        enroll_result = get_embedding(model, file, p.MAX_SEC)
        enroll_embs = np.array(enroll_result.tolist())
        speaker = name
    except:
        print("Error processing the input audio file. Make sure the path.")
    try:
        np.save(os.path.join(p.EMBED_LIST_FILE,speaker +".npy"), enroll_embs)
        print("Succesfully enrolled the user")
        engine = pyttsx3.init()
        engine.say("Successfully enrolled the user")
        engine.runAndWait()
    except:
        print("Unable to save the user into the database.")

# 
# 
# 
import speech_recognition as sr

import time



def enroll_from_voice():
    """Enroll a user by transcribing their speech and processing the resulting audio file
        inputs: None
        outputs: None"""

    # Initialize recognizer and microphone instances
    r = sr.Recognizer()
    mic = sr.Microphone()
    engine = pyttsx3.init()
    
    # Obtain user name through speech
    with mic as source:
        print("Please say your name.")
        engine.say("Please say your name")
        engine.runAndWait()
        time.sleep(1)
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        name = r.recognize_google(audio)
        print("Name: {}".format(name))
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
        engine.say("Sorry, I didn't catch that, Please try again.")
        engine.runAndWait()
        time.sleep(2)
        return
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        engine.say("Could not request results from Google Speech Recognition service")
        engine.runAndWait()
        time.sleep(2)
        return

    # Obtain voice sample for enrollment
    with mic as source:
        print("Please say a few words to enroll your voice.")
        engine.say("Please say a few words to enroll your voice")
        engine.runAndWait()
        time.sleep(1)
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        file = "enroll.wav"
        with open(file, "wb") as f:
            f.write(audio.get_wav_data())
        print("Audio saved to {}".format(file))
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
        engine.say("Sorry, I didn't catch that. Please try again.")
        engine.runAndWait()
        time.sleep(2)
        return
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        engine.say("Could not request results from Google Speech Recognition service.")
        engine.runAndWait()
        time.sleep(2)
        return

    # Enroll the user using the audio file
    enroll(name, file)
#     success = enroll(name, file)
#     # Provide output by voice
    
#     with mic as source:
#         if success:
#             print("You have been successfully enrolled.")
#             engine.say("You have been successfully enrolled.")
#         else:
#             print("Enrollment failed. Please try again.")
#             engine.say("Enrollment failed. Please try again.")
#         engine.runAndWait()


# 
# 
# 
# Import necessary modules
import speech_recognition as sr

# Call the enroll_from_voice function
enroll_from_voice()
