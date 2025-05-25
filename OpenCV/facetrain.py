import cv2
import os
from io import BytesIO
import requests
import numpy as np

haar_face_url = "https://robotics.hochschule-rhein-waal.de/gitlab/23496/Python/-/raw/ad1246a3858b31471dbb183aaaf770c253ae85b0/OpenCV/haar_face.xml"
response = requests.get(haar_face_url)

# Save the content to a local file
with open('haar_face.xml', 'wb') as f:
    f.write(response.content)

# training
people = ['Ben Afflek', 'Elton John', 'Jerry Seinfield', 'Madonna', 'Mindy Kaling']
DIR = r'/workspaces/depractice/OpenCV/train'

haar_cascade = cv2.CascadeClassifier('haar_face.xml')

features = []
labels = []

def create_train():
    for person in people:
        path = os.path.join(DIR, person)
        label = people.index(person)

        for img in os.listdir(path):
            img_path = os.path.join(path, img)

            img_array = cv2.imread(img_path)
            if img_array is None:
                continue

            gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

            faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

            for (x, y, w, h) in faces_rect:
                faces_roi = gray[y:y+h, x:x+w]
                features.append(faces_roi)
                labels.append(label)

create_train()
print('Training done ---------------')

features = np.array(features, dtype='object')
labels = np.array(labels)

face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Train the Recognizer on the features list and the labels list
face_recognizer.train(features, labels)

face_recognizer.save('face_trained.yml')
np.save('features.npy', features)
np.save('labels.npy', labels)