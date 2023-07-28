import cv2
import os
import numpy as np
import face_recognition as faceRegLib

def faceRecognition(imgLoc):
    demo_img_bgr = faceRegLib.load_image_file(imgLoc)
    demo_img_rgb = cv2.cvtColor(demo_img_bgr,cv2.COLOR_BGR2RGB)
    demo_faceCurFrame = faceRegLib.face_locations(demo_img_rgb)
    demo_train_encode = faceRegLib.face_encodings(demo_img_rgb, demo_faceCurFrame)


    face_cascade = cv2.CascadeClassifier(r"C:\Users\LENOVO\OneDrive\Desktop\idp\haarcascade_frontalface_default.xml")
    # cam = cv2.VideoCapture(0)
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    counter = 0
    result = False

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Video", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break

        if counter == 150:
            os.chdir(r'C:\Users\LENOVO\OneDrive\Desktop\idp\images')
            cv2.imwrite('check.jpg', frame) 
            img_bgr = faceRegLib.load_image_file('check.jpg')
            img_rgb = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2RGB)
            faceCurFrame = faceRegLib.face_locations(img_rgb)
            train_encode = faceRegLib.face_encodings(img_rgb, faceCurFrame)[0]
            result = faceRegLib.compare_faces([demo_train_encode],train_encode)
            os.remove('check.jpg')
            return result


        counter += 1

    cam.release()
    cv2.destroyAllWindows()
