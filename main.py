import cv2
import face_recognition
import numpy as np
import os
import pyttsx3
from datetime import datetime
import threading
import queue

# Create a waiting line for the names
speech_queue = queue.Queue()

# --- THE AUDIO WORKER ---
def tts_worker():
    while True:
        text = speech_queue.get()
        if text is None: break # Stop signal
        
        try:
            # THE FIX: Build and destroy the engine every single time
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id) # Index 1 for female voice
            engine.setProperty('rate', 175) 
            
            engine.say(text)
            engine.runAndWait()
            
            # Delete the engine to unlock the Windows audio thread for the next person
            del engine 
            
        except Exception as e:
            print(f"[AUDIO ERROR] Could not play voice: {e}")
            
        speech_queue.task_done()

# Start the background worker thread ONCE
threading.Thread(target=tts_worker, daemon=True).start()

# --- In-Memory Attendance Tracker ---
marked_today = set()
today_date = datetime.now().strftime('%d-%m-%Y')

if os.path.exists('Attendance.csv'):
    with open('Attendance.csv', 'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            entry = line.strip().split(',')
            if len(entry) > 1 and entry[1] == today_date:
                marked_today.add(entry[0])

def markAttendance(name):
    if name in marked_today:
        return 

    if not os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'w') as f:
            f.write('Name,Date,Time\n')

    with open('Attendance.csv', 'a') as f:
        now = datetime.now()
        dtString = now.strftime('%H:%M:%S')
        f.write(f'{name},{today_date},{dtString}\n')
        
    marked_today.add(name)
    print(f"[LOG] Attendance marked for: {name}")
    
    # Send the name to the waiting line
    speech_queue.put(f"Thank you")

print("[INFO] Initializing Smart Attendance System...")
print("[INFO] Scanning 'Known_Faces' folder for students...")

# 1. DYNAMICALLY LOAD ALL FACES
path = 'Known_Faces'
known_face_encodings = []
known_face_names = []
myList = os.listdir(path)

for cl in myList:
    if cl.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = f'{path}/{cl}'
        current_name = os.path.splitext(cl)[0] 
        try:
            raw_bgr = cv2.imread(img_path)
            if raw_bgr is None: continue
            raw_rgb = cv2.cvtColor(raw_bgr, cv2.COLOR_BGR2RGB)
            clean_image = np.ascontiguousarray(raw_rgb, dtype=np.uint8)
            encodings = face_recognition.face_encodings(clean_image)
            
            if len(encodings) > 0:
                known_face_encodings.append(encodings[0])
                known_face_names.append(current_name)
                print(f"[SUCCESS] Loaded profile for: {current_name}")
            else:
                print(f"[WARNING] No face found in {cl}. Skipping...")
        except Exception as e:
            print(f"[ERROR] Could not process {cl}: {e}")

print(f"[INFO] Total faces loaded into memory: {len(known_face_names)}")

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
        name = "Unknown"

        # Calculate exactly how similar the face is to all known faces
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        
        # --- THE PRECISION UPGRADE ---
        # 0.6 is default (generous). 0.5 is strict. 0.45 is very strict.
        STRICTNESS_THRESHOLD = 0.48 

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            
            # ONLY accept the match if the mathematical distance is lower than our strict threshold
            if face_distances[best_match_index] < STRICTNESS_THRESHOLD:
                name = known_face_names[best_match_index]
                markAttendance(name)

        # Scale back up for display
        top *= 4; right *= 4; bottom *= 4; left *= 4
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        
        cv2.rectangle(img, (left, top), (right, bottom), color, 2)
        cv2.putText(img, name, (left, bottom + 25), cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 1)

    cv2.imshow("Smart Attendance System", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()