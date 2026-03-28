# 🤖 Smart Attendance System (Face Recognition)

A high-performance, real-time attendance logging system developed as a **VITyarthi Capstone Project**. This project leverages Deep Learning to identify authorized faces, log attendance with precise timestamps in a CSV format, and features an automated email reporting pipeline with personalized auditory feedback.

---

## ✨ Key Features
* **Real-Time Identification:** Fast face detection and matching using HOG (Histogram of Oriented Gradients) and 128-dimensional ResNet embeddings.
* **Dynamic Roster Loading:** Automatically scans the `Known_Faces` directory on startup to encode any new personnel, eliminating the need for hardcoded image paths.
* **Asynchronous Audio Queue:** Utilizes Python's `threading` and `queue` modules to handle simultaneous multi-face recognition without freezing the camera feed.
* **Automated Email Reporting:** Includes a secure, built-in SMTP script (`send_report.py`) to dispatch the daily CSV attendance log directly to administrators.
* **Smart Duplicate Prevention:** Logic ensures a person is only logged once per day to maintain data integrity, using an in-memory `Set` for lightning-fast verification.
* **Precision Tuning:** Implements a strictness threshold using Euclidean distance to differentiate between highly similar faces.

---

## 🛠️ Tech Stack
* **Language:** Python 3.11
* **Computer Vision:** OpenCV (`cv2`)
* **AI Engine:** `face_recognition` (built on `dlib`)
* **Data Handling:** NumPy (v1.x)
* **Voice Engine:** `pyttsx3`
* **Security & Automation:** `python-dotenv`, `smtplib`, `threading`

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/gujarparth/Smart-Attendance-System.git
cd Face-Recognition-Attendance
```

### 2. Install dependencies
This project uses a custom `requirements.txt` to bypass common Windows/C++ build errors and enforce library compatibility.

```powershell
pip install -r requirements.txt
```

### 3. Environment Security Setup (For Automated Emails)
To use the automated email reporter without exposing your credentials:
1. Copy the `.env.example` file and rename it to `.env`.
2. Add your Google App Password and target emails inside the `.env` file:
   ```text
   SENDER_EMAIL=your_email@gmail.com
   APP_PASSWORD=your_16_letter_app_password
   RECEIVER_EMAIL=professor_email@vitbhopal.ac.in
   ```

### 4. Add Your Biometric Data (Crucial Step)
For privacy reasons, this repository does not include real facial data. To make the system work:
1. Open the `Known_Faces/` folder.
2. Drop in clear, well-lit `.jpg` or `.jpeg` photos of the people you want to recognize.
3. Name the file exactly what you want the system to call them (e.g., `Parth.jpg` or `Professor_Smith.jpg`).

---

## 📂 Project Structure
* `Known_Faces/` : Store `.jpg` or `.jpeg` photos of authorized users here. The system dynamically loads these.
* `main.py` : The primary multithreaded logic for vision, recognition, and CSV logging.
* `send_report.py` : The SMTP script to securely email the daily log.
* `Attendance.csv` : Automatically generated log file.
* `requirements.txt` : Dependency manager enforcing Python 3.11 + Numpy 1.x compatibility.
* `.env.example` : Template for local credential management.

---

## 🔧 Troubleshooting & Engineering Solutions

During development, several critical "industry-standard" bugs were solved:
1. **Dlib Compilation/Memory Layout:** Bypassed Windows C++ build tools via a pre-compiled `.whl` and forced raw images into a contiguous 8-bit RGB grid (`np.ascontiguousarray`).
2. **SAPI5 COM Object Lock:** Solved the `pyttsx3` threading crash by implementing a "Build & Destroy" worker queue, allowing the AI to announce multiple names simultaneously without locking the audio thread.
3. **The "First Match" Flaw:** Upgraded the recognition logic from a basic Boolean match to an `np.argmin` distance calculator, ensuring the system strictly selects the *best* mathematical match when scanning crowded frames.

---

## 👤 Author
* **Parth Gujar**