import os
import pickle

import cv2
import cvzone
import face_recognition
import numpy as np

cap=cv2.VideoCapture(0)
cap.set(3,620)
cap.set(4,493)

imgBackground = cv2.imread('Resources/Background2.png')

#importation des images modes dans une liste
folderModePath='Resources/Modes'
modelPathList=os.listdir(folderModePath)
imgModeList = []

for path in modelPathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))


#lancer le fichier encoder
print("chargement du fichier encoder...")
file=open("EncodeFile.p",'rb')
encodeListKnownWithIds=pickle.load(file)
file.close()
encodeListKnown,superAdminIds=encodeListKnownWithIds
print("fichier encoder charger")


while True:
    success, img = cap.read()
    imgS=cv2.resize(img,(0,0),None,0.25,0.25)
    imgS=cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)

    imgBackground[178:178 + 493, 62:62 + 620] = cv2.resize(img, (620, 493))

    # Testez différentes positions
    mode_img = cv2.resize(imgModeList[1], (451, 512))  # Redimensionner aux dimensions exactes
    imgBackground[158:158 + 512, 781:781 + 451] = mode_img


    for encodeFace,faceLoc in zip(encodeCurFrame,faceCurFrame):
        matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
        print("matches:",matches)
        print("faceDis:",faceDis)

        matchIndex=np.argmin(faceDis)

        if matches[matchIndex]:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 65 + x1, 180 + y1, x2 - x1, y2 - y1  # Changé de 62,178 à 65,180
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)


    cv2.imshow("webcam", img)
    cv2.imshow("imgBackground", imgBackground)
    cv2.waitKey(1)