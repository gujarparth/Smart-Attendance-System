# 🤖 Smart Attendance System (Face Recognition)

A high-performance, real-time attendance logging system developed as a **CO5 Case Study at VIT Bhopal**. This project leverages Deep Learning to identify authorized faces, log attendance with precise timestamps in a CSV format, and provide personalized auditory feedback.

---

## ✨ Key Features
* **Real-Time Identification:** Fast face detection and matching using HOG (Histogram of Oriented Gradients) and 128-dimensional ResNet embeddings.
* **Automated CSV Logging:** Generates a daily attendance report (Attendance.csv) compatible with Microsoft Excel.
* **Smart Duplicate Prevention:** Logic ensures a person is only logged once per day to maintain data integrity.
* **Voice Alerts:** Integrated "Microsoft Zira" female voice for personalized "Thank You" greetings upon successful marking.
* **Optimized Performance:** Frame scaling (0.25x) allows for smooth processing even on standard laptop hardware.

---

## 🛠️ Tech Stack
* **Language:** Python 3.11
* **Computer Vision:** OpenCV (cv2)
* **AI Engine:** face_recognition (built on dlib)
* **Data Handling:** NumPy (v1.x)
* **Voice Engine:** pyttsx3
* **Image Processing:** Pillow (PIL)

---

## 🚀 Installation & Setup

### 1. Clone the repository
git clone https://github.com/your-username/Face-Recognition-Attendance.git
cd Face-Recognition-Attendance

### 2. Install specific dependencies
This project requires specific versions to bypass common Windows/Dlib compatibility issues.

**Install the AI Engine:**
pip install cmake
pip install https://github.com/z-mahmud22/Dlib_Windows_Python3.x/raw/main/dlib-19.24.1-cp311-cp311-win_amd64.whl
pip install face_recognition

**Install helper libraries & fix the Numpy 2.0 bug:**
pip install "numpy<2"
pip install opencv-python Pillow pyttsx3

---

## 📂 Project Structure
* Known_Faces/ : Store .jpg or .jpeg photos of authorized users here.
* main.py : The primary logic for vision, recognition, and logging.
* Attendance.csv : Automatically generated log file.
* project_report.md : Detailed technical analysis and CO5 case study documentation.

---

## 🔧 Troubleshooting (Real-World Solutions)

During development, several critical "industry-standard" bugs were solved:
1. Dependency Management: Fixed dlib installation by using a pre-compiled wheel binary specifically for Python 3.11.
2. Memory Layout: Solved the "Unsupported image type" error by forcing images into a contiguous 8-bit RGB grid using np.ascontiguousarray.
3. Numpy 2.0 Breaking Change: Downgraded to Numpy 1.26.4 to maintain compatibility with the C++ dlib backend.

---

## 👤 Author
* **Parth Gujar**
