import os
import cv2
import time
import pickle
import face_recognition
from datetime import datetime


def isAuthenticated():
    print("[INFO] Loading training data...")
    data = pickle.loads(open('encoder.pickle', "rb").read())

    encodings = data["encodings"]
    labels = data["labels"]

    basePath = os.getcwd()
    testPath = os.path.join(basePath, 'test')

    predicts = {}
    count = 1

    cam = cv2.VideoCapture(0)
    time.sleep(1)

    try:
        while(count <= 5):
            ret, image = cam.read()
            if(ret):
                image = cv2.flip(image, 1)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
                faces = face_recognition.face_locations(rgb, model="hog")
                if(len(faces)==0):
                    continue
                
                imagePath = os.path.join(testPath, "img-"+str(count)+".jpg")
                cv2.imwrite(imagePath, image)
                count += 1
                encodes = face_recognition.face_encodings(rgb, faces)
                for encode in encodes:
                    matches = face_recognition.compare_faces(encodings, encode, tolerance=0.5)
                    
                    label = "Unknown"
                    if True in matches:
                        matchedInds = [ i for (i, b) in enumerate(matches) if b]
                        counts = {}
                        for i in matchedInds:
                            label = labels[i]
                            counts[label] = counts.get(label, 0) + 1
                        label = max(counts, key=counts.get)
                    predicts[label] = predicts.get(label, 0)+1
    except:
        print("[Error] Found exception case...")
    
    cam.release()
    cv2.destroyAllWindows()
    
    label = max(predicts, key=predicts.get) 
    if(label == "Unknown"):
        return False, "Unknown"
    return True, label

if __name__ == "__main__":
    print(isAuthenticated())

