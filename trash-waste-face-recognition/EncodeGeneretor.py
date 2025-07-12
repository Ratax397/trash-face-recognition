import os
import face_recognition
import cv2
import pickle

#importation des images du superadmin
folderPath='Images'
pathList=os.listdir(folderPath)
imgList = []
superAdminIds=[]
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    superAdminIds.append(os.path.splitext(path)[0])

def findEncodings(imgList):
    encodeList = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("encode start....")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds=[encodeListKnown,superAdminIds]
print("encode end....")

file=open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("file saved")