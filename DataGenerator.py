import cv2
import numpy as np
import os

class DataGenerator:

    def __init__(self):
        try:
            os.makedirs('people/')
        except:
            pass

    def generate(self, username):
        pic_no = 0
        number = len(os.listdir('people/'))
        name = username  + str(number)
        os.makedirs('people/' + name)
        fa = cv2.CascadeClassifier('faces.xml')
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret = True
        while ret:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = fa.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cropped = frame[y:y + h, x:x + w]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2, cv2.LINE_AA)
                pic_no = pic_no + 1
                cv2.imwrite('people/' + name + '/' + str(pic_no) + '.jpg', cropped)
            cv2.imshow('frame', frame)
            cv2.waitKey(100)

            if (pic_no > 50):
                break

        cap.release()
        cv2.destroyAllWindows()