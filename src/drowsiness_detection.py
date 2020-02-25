import cv2
import time
import math
import dlib
import pygame
import numpy as np
from imutils import face_utils

def getEuclideanDistance(p1, p2):
    dist = math.sqrt(sum([ (x-y)**2 for x, y in zip(p1,p2)]))
    return dist

def eye_aspect_ratio(eye):
    A = getEuclideanDistance(eye[1], eye[5])
    B = getEuclideanDistance(eye[2], eye[4])
    C = getEuclideanDistance(eye[0], eye[3])
    return ((A+B)/C)


def drawPoints(image, eye):
	for cent in eye:
		cv2.circle(image,tuple(cent), 1, (255,222,225))

def drowsyCheck():
    pygame.mixer.init() #Initialize Pygame and load music
    pygame.mixer.music.load('files/red_alert.wav')

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('files/shape_predictor_68_face_landmarks.dat')

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

    EAR_THRESHOLD = 0.58
    EAR_FRAMES = 5
    COUNTER = 0
    
    cam = cv2.VideoCapture(0)
    time.sleep(1)
    try:
        while(True):
            EAR = ''
            ret, image = cam.read()
            if ret:
                image = cv2.flip(image,1)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                faces = detector(gray, 0) #Detect facial points through detector function
                if(len(faces) > 1):
                    continue

                for face in faces:
                    shape = predictor(gray, face)
                    shape = face_utils.shape_to_np(shape)
                    leftEye = shape[lStart:lEnd] #Get array of coordinates of leftEye and rightEye
                    rightEye = shape[rStart:rEnd]
                    drawPoints(image, leftEye)
                    drawPoints(image, rightEye)
                    
                    l_EAR = eye_aspect_ratio(leftEye)
                    r_EAR = eye_aspect_ratio(rightEye)
                    EAR = (l_EAR + r_EAR) / 2

                    if(EAR < EAR_THRESHOLD):
                        COUNTER += 1
                        if COUNTER >= EAR_FRAMES:
                            pygame.mixer.music.play(-1)  
                            cv2.putText(image, "Drowsiness Detected Alert", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,222), 3)                  
                    else:
                        pygame.mixer.music.stop()
                        COUNTER = 0

                cv2.putText(image, ("Eye Aspect Ratio:"+(str(EAR)[:4])), (10,420), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.6, (200,200,200), 1)
                cv2.putText(image, f'Press "q" to QUIT', (10,450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

                cv2.imshow('Drowsiness Detection', image)
                if(cv2.waitKey(1) & 0xFF == ord('q')):
                    break
    except:
        print("[Error] Error occured.")
    
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    drowsyCheck()