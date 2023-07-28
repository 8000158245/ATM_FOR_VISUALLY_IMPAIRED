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

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)
#IMPORT USER-DEFINED FUNCTIONS
from feature_extraction import get_embedding, get_embeddings_from_list_file
from preprocess import get_fft_spectrum
import parameters as p



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
    try:
        file = "enroll1.wav"
        with open(file, "wb") as f:
            f.write(audio.get_wav_data())
        # recognize(file)
        print("Audio saved to {}".format(file))
        
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
        engine.say("Sorry, I didn't catch that. Please try again.")
        engine.runAndWait()
        time.sleep(10)
    #     return
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        engine.say("Could not request results from Google Speech Recognition service.")
        engine.runAndWait()
        time.sleep(10)
    #     return


    recognize(file)


# 
# 
def recognize(file):
    """Recognize the input audio file by comparing to saved users' voice prints
        inputs: str (Path to audio file of unknown person to recognize)
        outputs: str (Name of the person recognized)"""
    engine = pyttsx3.init()
    
    
    if os.path.exists(p.EMBED_LIST_FILE):
        embeds = os.listdir(p.EMBED_LIST_FILE)
    # if len(embeds) == 0:
    #     #print("No enrolled users found")
    #     exit()
    #print("Loading model weights from [{}]....".format(p.MODEL_FILE))
    try:
        model = load_model(p.MODEL_FILE)

    except:
        #print("Failed to load weights from the weights file, please ensure *.pb file is present in the MODEL_FILE directory")
        exit()
        
    distances = {}
    #print("Processing test sample....")
    #print("Comparing test sample against enroll samples....")
    test_result = get_embedding(model, file, p.MAX_SEC)
    test_embs = np.array(test_result.tolist())
    for emb in embeds:
        enroll_embs = np.load(os.path.join(p.EMBED_LIST_FILE,emb))
        speaker = emb.replace(".npy","")
        distance = euclidean(test_embs, enroll_embs)
        distances.update({speaker:distance})
    if min(list(distances.values()))<p.THRESHOLD:
        print("Recognized: ",min(distances, key=distances.get))
        engine.say(min(distances, key=distances.get))
        engine.runAndWait()
        

        
    else:
        # print("Could not identify the user, try enrolling again with a clear voice sample")
        # print("Score: ",min(list(distances.values())))
        exit()


# 
# 
# 

recognize_from_voice()


    
