import streamlit as st
from deepface import DeepFace
import cv2
import numpy as np
import random

st.set_page_config(page_title="Emotion Detector", layout="centered")

MOTIVATION_TEXTS = {
    'angry': [
        "Take a deep breath, let go of what you can't control.",
        "Channel your energy into something positive.",
        "It's okay to feel angry, but don't let it define you.",
        "Pause and reflect before you react.",
        "Peace begins with a single thought."
    ],
    'disgust': [
        "Focus on what uplifts you and brings joy.",
        "Let go of negativity, embrace positivity.",
        "Find beauty in the small things.",
        "You have the power to change your perspective.",
        "Choose kindness over judgment."
    ],
    'fear': [
        "Courage is not the absence of fear, but the triumph over it.",
        "Face your fears, they often disappear.",
        "You are braver than you believe.",
        "Every challenge is an opportunity to grow.",
        "Trust yourself, you can handle it."
    ],
    'happy': [
        "Keep smiling, your happiness is contagious!",
        "Enjoy the moment and spread positivity.",
        "Happiness looks great on you!",
        "Cherish these joyful times.",
        "Let your smile change the world."
    ],
    'sad': [
        "Tough times never last, but tough people do.",
        "Your smile is your superpower—let it shine!",
        "Every storm runs out of rain. Happiness is on its way.",
        "You are capable of amazing things. Believe in yourself!",
        "Let today be the start of something new and joyful."
    ],
    'surprise': [
        "Embrace the unexpected, it brings new opportunities.",
        "Let curiosity guide you through surprises.",
        "Life is full of wonderful surprises!",
        "Stay open to new experiences.",
        "Surprises keep life interesting."
    ],
    'neutral': [
        "Take a moment to relax and recharge.",
        "Balance is key to a peaceful mind.",
        "Enjoy the calm and clarity.",
        "Sometimes, neutrality is strength.",
        "Let your mind rest and reset."
    ]
}

def get_motivation(emotion):
    texts = MOTIVATION_TEXTS.get(emotion, [
        "Every feeling is valid. Take care of yourself today!"
    ])
    return random.choice(texts)

st.markdown("""
    <style>
    .result-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        margin-top: 24px;
    }
    .emotion-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 8px;
    }
    .motivation-text {
        font-size: 1.1rem;
        color: #16a085;
        margin-top: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("😊 Predictive Emotion Analysis System")
st.write("Analyze your facial emotion and get a motivational quote instantly!")

if 'emotion' not in st.session_state:
    st.session_state['emotion'] = None
if 'motivation' not in st.session_state:
    st.session_state['motivation'] = None
if 'frame' not in st.session_state:
    st.session_state['frame'] = None

col1, col2 = st.columns([1,2])
with col1:
    st.write("")
    capture = st.button("📸 Capture Emotion", use_container_width=True)
    reset = st.button("🔄 Reset", use_container_width=True)

with col2:
    if st.session_state['frame'] is not None:
        st.image(st.session_state['frame'], caption="Captured Image", use_container_width=True)

if capture:
    with st.spinner('Analyzing emotion...'):
        cap = cv2.VideoCapture(0)
        frames = []
        # Capture 5 frames for better accuracy
        for _ in range(5):
            ret, frame = cap.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(rgb_frame)
        cap.release()
        if frames:
            st.session_state['frame'] = frames[-1]
            st.image(frames[-1], caption="Captured Image", use_container_width=True)
            try:
                emotions = []
                for f in frames:
                    result = DeepFace.analyze(f, actions=['emotion'], enforce_detection=False)
                    if isinstance(result, list):
                        result = result[0]
                    emotion = result.get('dominant_emotion', None)
                    if emotion:
                        emotions.append(emotion)
                # Pick the most common emotion from the frames
                if emotions:
                    from collections import Counter
                    emotion = Counter(emotions).most_common(1)[0][0]
                    motivation = get_motivation(emotion)
                    st.session_state['emotion'] = emotion
                    st.session_state['motivation'] = motivation
                else:
                    st.error("Could not detect emotion.")
            except Exception as e:
                st.error(f"Error analyzing emotion: {e}")
        else:
            st.error("Could not access webcam.")

if reset:
    st.session_state['emotion'] = None
    st.session_state['motivation'] = None
    st.session_state['frame'] = None
    st.success("Reset!")

if st.session_state['emotion']:
    st.markdown(f"<div class='result-card'>"
                f"<div class='emotion-title'>Detected Emotion: {st.session_state['emotion'].capitalize()}</div>"
                f"<div class='motivation-text'>{st.session_state['motivation']}</div>"
                "</div>", unsafe_allow_html=True)
    