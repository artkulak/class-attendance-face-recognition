import cv2
from face_detection import face
from keras.models import load_model
import numpy as np
from embedding import emb
import os
import re
import keras

CAM_CONSTANT = 0


class Recognizer:

    def __init__(self):
        self.label = None

        self.a = dict()
        for i in range(len(os.listdir('people/'))):
            self.a[i] = 0
        self.people = dict()
        for value in os.listdir('people/'):
            name = re.sub(r'[0-9]+', '', value)
            number = int(re.findall('\d+', value)[0])
            self.people[number] = name

        print(self.people.items())
        self.abhi = None

    def recognize(self, get_attendance = False, FRAMES = 30):
        with keras.backend.get_session().graph.as_default():
            e = emb()
            fd = face()
            model = load_model('face_reco2.MODEL')

            n_frames = 0
            attendance = dict()
            ret  = True
            cap = cv2.VideoCapture(CAM_CONSTANT, cv2.CAP_DSHOW)

            WindowName = 'StudentDetector'
            cv2.namedWindow(WindowName, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(WindowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.setWindowProperty(WindowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)


            for person in self.people.values():
                attendance[person] = 0

            print(attendance.items())
            for i in range(FRAMES):
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                try:
                    det, coor = fd.detectFace(frame)
                except:
                    det, coor = None, None

                if (det is not None):
                    for i in range(len(det)):
                        detected = det[i]
                        k = coor[i]
                        f = detected
                        detected = cv2.resize(detected, (160, 160))
                        # detected=np.rollaxis(detected,2,0)
                        detected = detected.astype('float') / 255.0
                        detected = np.expand_dims(detected, axis=0)
                        feed = e.calculate(detected)
                        feed = np.expand_dims(feed, axis=0)
                        prediction = model.predict(feed)[0]

                        result = int(np.argmax(prediction))
                        if get_attendance:
                            if (np.max(prediction) > .70):
                                for i in self.people:
                                    if (result == i):
                                        self.label = self.people[i]
                                        attendance[self.label] += 1
                                        if (self.a[i] == 0):
                                            print("a")
                                        self.a[i] = 1
                                        abhi = i
                            else:
                                self.label = 'unknown'

                        cv2.putText(frame, self.label, (k[0], k[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        cv2.rectangle(frame, (k[0], k[1]), (k[0] + k[2], k[1] + k[3]), (252, 160, 39), 3)
                n_frames += 1
                cv2.imshow(WindowName, frame)
                if (cv2.waitKey(1) & 0XFF == ord('q')):
                    break
            for person in attendance.keys():
                attendance[person] /= n_frames
            cap.release()
            cv2.destroyAllWindows()
            return attendance

    def Stream(self):
        ret = True
        cap = cv2.VideoCapture(CAM_CONSTANT, cv2.CAP_DSHOW)
        while ret:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, dsize=(500, 300))
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
