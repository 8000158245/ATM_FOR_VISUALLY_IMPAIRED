from flask import Flask, render_template, request, redirect, url_for
import speech_recognition as sr
import pyttsx3
import serial
import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",template_folder='template')

@app.route("/speech", methods=["POST"])
def speech():
    # Get speech input from the user
    time.sleep(5)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        # Perform speech recognition on the audio data
        text = r.recognize_google(audio)
        # Speak the output using text-to-speech
        engine = pyttsx3.init()
        engine.say("Thank you for banking with us. We are processing your transaction for amount " + text)
        engine.runAndWait()

        ser = serial.Serial('COM10', 9600)  # Change 'COM3' to the appropriate serial port
        time.sleep(2)  # Wait for the serial connection to be established
        if (1<=int(text)<=1000):
            angle = 180  # Set the desired angle of the servo motor
            ser.write(str(angle).encode())
        elif (1000<int(text)<=2000):
            angle = 180
            for i in range(2):
                ser.write(str(angle).encode())
                time.sleep(5)

        elif (2000<int(text)<=3000):
            angle = 180
            for i in range(3):
                ser.write(str(angle).encode())
                time.sleep(5)

        elif (3000<int(text)<=4000):
            angle = 180
            for i in range(4):
                ser.write(str(angle).encode())
                time.sleep(5)

        elif (4000<int(text)<=5000):
            angle = 180
            for i in range(5):
                ser.write(str(angle).encode())
                time.sleep(5)

        return redirect(url_for('final_transaction'))
        return render_template("success.html",template_folder='template')
    except:
        # Return an error message if there was a problem with speech recognition
        return "Error: Unable to recognize speech."
    
@app.route('/final_transaction')
def final_transaction():
    return 'success.html'

if __name__ == "__main__":
    app.run(debug=True)
