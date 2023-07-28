import pyrebase
import datetime
import serial
import pyttsx3

engine = pyttsx3.init()

# set the properties of the voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # set the voice to the second one

def say(text):
    engine.say(text)
    engine.runAndWait()

ser = serial.Serial('COM9', 9600) # replace with the appropriate port and baud rate for your setup
counter=  0
loc_atm = []
while counter < 2:
    data = ser.readline().decode('utf-8').rstrip()
    loc_atm.append(data)
    counter += 1

#reading location of person from database
config = {
    
  "apiKey": "AIzaSyB8arSwun3MckMN7osm-PTQRcEBqY-MYNQ",
  "authDomain": "locationtrack-2bb6b.firebaseapp.com",
  "databaseURL": "https://locationtrack-2bb6b-default-rtdb.firebaseio.com",
  "projectId": "locationtrack-2bb6b",
  "storageBucket": "locationtrack-2bb6b.appspot.com",
  "messagingSenderId": "731673908946",
  "appId": "1:731673908946:web:c365ad21bd9458d1a7ff0b",
  "measurementId": "G-0TTTTJLC7S"

}

loc = []
firebase = pyrebase.initialize_app(config)
db = firebase.database()
latitude = db.child("Location").child("latitude").get()
longitude = db.child("Location").child("longitude").get()
timestamp = db.child("Location").child("timestamp").get()
latitude = next(reversed(latitude.val().values()))
longitude = next(reversed(longitude.val().values()))
timestamp = next(reversed(timestamp.val().values()))
loc.append(latitude)
loc.append(longitude)


present_time = datetime.datetime.now().timestamp()
date_string = timestamp
date_object = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
date_object = date_object.timestamp()

seconds = int(date_object - present_time)

def verify_location():

    if seconds >  20:
        say("You didn't open the app on time. Please try again later")
        return 0
    else:
        if(loc_atm[0][:4] == loc[0][:4] and loc_atm[1][:4] == loc[1][:4]):
            return 1
        else:
            return 0