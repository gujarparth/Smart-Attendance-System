import cv2
import face_recognition
import numpy as np
import os
import pyttsx3
from datetime import datetime

# --- Voice Engine Setup ---
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Index 1 is usually 'Microsoft Zira' (Female). If you have others, change this number!
engine.setProperty('voice', voices[1].id) 

# Speed and Volume tuning
engine.setProperty('rate', 175)  # Slightly faster for a "cuter" tone
engine.setProperty('volume', 1.0) 

def markAttendance(name):
    if not os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'w') as f:
            f.writelines('Name,Date,Time')

    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        today_date = datetime.now().strftime('%d-%m-%Y')
        
        for line in myDataList:
            entry = line.split(',')
            if len(entry) > 1:
                nameList.append(f"{entry[0]}_{entry[1]}")
        
        if f"{name}_{today_date}" not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{today_date},{dtString}')
            
            print(f"[LOG] Attendance marked for: {name}")
            
            # --- THE GREETING ---
            engine.say(f"Thank you, {name} , Your Attendance has been marked!")
            engine.runAndWait()

print("[INFO] Initializing VIT Smart Attendance System...")

# 1. Load and Encode (Using the NumPy 1.x fix we did earlier)
image_path = "Known_Faces/Shivang.jpeg"
try:
    raw_bgr = cv2.imread(image_path)
    raw_rgb = cv2.cvtColor(raw_bgr, cv2.COLOR_BGR2RGB)
    shivang_image = np.ascontiguousarray(raw_rgb, dtype=np.uint8)
    shivang_encoding = face_recognition.face_encodings(shivang_image)[0]
    print("[SUCCESS] Reference face encoded!")
except Exception as e:
    print(f"[ERROR] {e}")
    exit()

known_face_encodings = [shivang_encoding]
known_face_names = ["Shivang"]

# 2. Start Webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success: break

    small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    rgb_small_frame = np.ascontiguousarray(rgb_small_frame, dtype=np.uint8)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            markAttendance(name)

        top *= 4; right *= 4; bottom *= 4; left *= 4
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(img, (left, top), (right, bottom), color, 2)
        cv2.putText(img, name, (left, bottom + 25), cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 1)

    cv2.imshow("VIT Smart Attendance", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()