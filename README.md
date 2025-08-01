# 🚦 Traffic Sign Detection  
### Bosch Future Mobility Challenge 2023

This project implements computer vision techniques to detect and classify traffic signs in real-time using image and video input. Built for the **Bosch Future Mobility Challenge 2023**, it aims to support autonomous navigation by recognizing critical road signs in various conditions.

---

## 📁 Project Structure

```plaintext
Traffic-Signs-BFMC/
│
├── color_calibration.py        # HSV calibration for color-based segmentation
├── TrafficSigns.py             # Main logic for sign detection using images
├── Traffic_signs_video.py      # Detection logic applied to video streams
│
├── image data/                 # Sample images of traffic signs
├── video data/                 # Recorded driving videos for detection testing
├── testing scripts/            # Evaluation and helper scripts
├── README.md                   # Project documentation
```


---

## Features

- Color-based segmentation and shape analysis  
- Detection and classification of signs like stop, yield, turn, etc.  
- Real-time video stream processing  
- Calibration tool for HSV thresholds  
- Modular codebase for quick testing on different inputs  

---

## 🛠️ Getting Started

### Requirements

- Python 3.7+  
- OpenCV  
- NumPy  
- (Optional) Matplotlib for debugging  

---

### ▶️ Run detection on images

```bash
python3 TrafficSigns.py
```
### ▶️ Run detection on video

```bash
python3 Traffic_signs_video.py
```

### 🎛️ Calibrate color thresholds

```bash
python3 color_calibration.py
```


### 📊 Dataset

Images and videos used for testing are located in:

    image data/

    video data/

### 👥 Contributors

Developed by AggelikiZ and team iRASional for the Bosch Future Mobility Challenge 2023.

