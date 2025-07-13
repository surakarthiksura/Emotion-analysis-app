# Predictive Emotion Analysis System for Justice & Rehabilitation

## Overview
This system analyzes facial and voice inputs to detect emotions, predict behavioral risks, and visualize emotional trends for legal and rehabilitation professionals.

## Features
- Facial emotion detection (DeepFace)
- Voice emotion analysis (SpeechRecognition, Librosa)
- Predictive modeling (Scikit-learn)
- Real-time dashboard (Streamlit, Matplotlib, Seaborn)
- Secure deployment (HTTPS, no personal data stored)

## Folder Structure
```
/project
  ├── app.py
  ├── emotion_model.pkl
  ├── emotion_log.csv
  ├── audio.wav
```

## How to Run Locally
1. Install dependencies:
   ```
   pip install streamlit opencv-python deepface SpeechRecognition librosa scikit-learn matplotlib seaborn pandas
   ```
2. Start the app:
   ```
   streamlit run app.py
   ```

## Deployment
- Push to GitHub and connect to Streamlit Cloud or Hugging Face
- Enable HTTPS

## Security
- No personal data stored
- Use environment variables for configuration
- Two-factor authentication recommended for GitHub/cloud

## Authors
Karthik, Revathi, Pravi, Abhtej, Bhagyadeep

## Date
11/07/2025
