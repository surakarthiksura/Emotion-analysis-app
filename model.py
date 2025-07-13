import streamlit as st
import random
import kagglehub
import os
import base64
from PIL import Image
import io

st.set_page_config(page_title="AI Face Emotion Capture", layout="wide")


# --- Apple/OnePlus Inspired Custom CSS ---
st.markdown("""
    <style>
    @font-face {
        font-family: 'SF Pro Display';
        src: local('SF Pro Display'), url('https://fonts.cdnfonts.com/s/17510/SFProDisplay-Regular.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }
    body, html, .main-card, .result-card, .section-header, .emotion-title, .motivation-text, .hero-title, .hero-desc, .stButton > button, .stRadio > div {
        font-family: 'SF Pro Display', 'San Francisco', Arial, sans-serif !important;
    }
    body {
        background: #fff !important;
        color: #222;
    }
    .hero {
        width: 100vw;
        min-height: 320px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: transparent !important;
        margin-bottom: 32px;
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 700;
        color: #222;
        letter-spacing: 1.5px;
        text-align: center;
        margin-bottom: 12px;
        margin-top: 32px;
        background: transparent !important;
    }
    .hero-desc {
        font-size: 1.3rem;
        color: #555;
        text-align: center;
        margin-bottom: 18px;
        font-weight: 400;
        background: transparent !important;
    }
    .main-card {
        background: #fff;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(44,62,80,0.12);
        padding: 40px 40px 32px 40px;
        margin: 0 auto 32px auto;
        max-width: 650px;
        transition: box-shadow 0.2s;
    }
    .main-card:hover {
        box-shadow: 0 12px 48px rgba(44,62,80,0.18);
    }
    .section-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #222;
        margin-bottom: 22px;
        text-align: center;
        letter-spacing: 1.2px;
    }
    .result-card {
        background: #f6f8fa;
        border-radius: 14px;
        padding: 22px 28px;
        margin: 22px 0;
        box-shadow: 0 2px 16px rgba(44,62,80,0.09);
        text-align: center;
    }
    .emotion-title {
        font-size: 1.7rem;
        font-weight: 700;
        color: #007aff;
        margin-bottom: 10px;
    }
    .motivation-text {
        font-size: 1.15rem;
        color: #636e72;
        margin-top: 8px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #007aff 0%, #00bfae 100%);
        color: #fff;
        border: none;
        border-radius: 10px;
        padding: 0.7em 2em;
        font-size: 1.08rem;
        font-weight: 600;
        margin: 0 10px 0 0;
        box-shadow: 0 2px 12px rgba(44,62,80,0.10);
        transition: background 0.2s, box-shadow 0.2s;
        font-family: 'SF Pro Display', 'San Francisco', Arial, sans-serif !important;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #00bfae 0%, #007aff 100%);
        color: #222;
        box-shadow: 0 4px 24px rgba(44,62,80,0.18);
    }
    .stRadio > div {
        font-size: 1.15rem;
        font-weight: 500;
        color: #222;
        font-family: 'SF Pro Display', 'San Francisco', Arial, sans-serif !important;
    }
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 18px;
    }
    .sidebar-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #007aff;
        font-family: 'SF Pro Display', 'San Francisco', Arial, sans-serif !important;
    }
    .live-video-img {
        border-radius: 18px;
        box-shadow: 0 4px 24px rgba(44,62,80,0.18);
        border: 2px solid #007aff;
        margin-bottom: 14px;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown('''
<div class="hero" style="max-width:900px;margin:0 auto;">
    <div class="hero-title">AI Face Emotion Capture</div>
    <div class="hero-desc">A modern, professional emotion analysis platform for individuals and teams.<br>Fast, accurate, and beautifully designed.</div>
</div>
''', unsafe_allow_html=True)

## Motivation Texts
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

# --- Multi-person management ---
BASE_DIR = "facespace"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)




# --- Person Management UI in main interface (top right columns) ---
persons = [d for d in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, d))]
colA, colB, colC = st.columns([2,2,2])
with colA:
    st.markdown("<div style='text-align:right;font-weight:600;font-size:1.1rem;'>Person Management</div>", unsafe_allow_html=True)
with colB:
    selected_person = st.selectbox("Select Person", ["Add New Person"] + persons, key="main_select_person")
with colC:
    if selected_person == "Add New Person":
        new_name = st.text_input("Person Name", key="main_new_person")
        if st.button("Create Person Space", key="main_create_person") and new_name:
            person_dir = os.path.join(BASE_DIR, new_name)
            os.makedirs(person_dir, exist_ok=True)
            st.success(f"Space created for {new_name}!")
            st.experimental_rerun()
    else:
        new_person_name = st.text_input("Rename Person", value=selected_person, key="main_rename_person")
        if st.button("Save Name Change", key="main_save_name") and new_person_name and new_person_name != selected_person:
            old_path = os.path.join(BASE_DIR, selected_person)
            new_path = os.path.join(BASE_DIR, new_person_name)
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                st.success(f"Renamed to {new_person_name}")
                st.experimental_rerun()
            else:
                st.error("A person with that name already exists.")
        if 'delete_confirm' not in st.session_state:
            st.session_state['delete_confirm'] = False
        if st.button("Delete Person", key="main_delete_person"):
            st.warning(f"Are you sure you want to delete '{selected_person}'? This cannot be undone.")
            st.session_state['delete_confirm'] = True
        if st.session_state['delete_confirm']:
            if st.button("Confirm Delete", key="main_confirm_delete"):
                import shutil
                shutil.rmtree(os.path.join(BASE_DIR, selected_person))
                st.success(f"Deleted '{selected_person}'!")
                st.session_state['delete_confirm'] = False
                st.experimental_rerun()
            if st.button("Cancel Delete", key="main_cancel_delete"):
                st.session_state['delete_confirm'] = False

if selected_person == "Add New Person":
    st.markdown('''
    <div class="main-card" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:320px;">
        <div class="section-header" style="margin-bottom:12px;">Add a Person to Begin</div>
        <div style="font-size:2.5rem;margin-bottom:18px;">😊</div>
        <div style="font-size:1.15rem;color:#555;text-align:center;max-width:400px;">Please add a person to begin capturing emotions.</div>
    </div>
    ''', unsafe_allow_html=True)
else:
    person_dir = os.path.join(BASE_DIR, selected_person)
    st.markdown(f'''
    <div class="main-card" style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:320px;">
        <div class="section-header" style="margin-bottom:12px;">Welcome, {selected_person}!</div>
    </div>
    ''', unsafe_allow_html=True)
    mode = st.radio("Choose Mode", ["Photo", "Video"], horizontal=True)
    if mode == "Photo":
        # Assign button states to variables for logic
        capture = st.button("Capture Photo", key="capture_btn")
        retake = st.button("Retake Photo", key="retake_btn")
        reset_btn = st.button("Reset All", key="reset_btn")
        st.markdown('''
        <div style="display:flex;justify-content:center;align-items:center;gap:24px;margin-bottom:24px;">
            <div>{}</div><div>{}</div><div>{}</div>
        </div>
        '''.format(capture, retake, reset_btn), unsafe_allow_html=True)
        if 'frame' not in st.session_state:
            st.session_state['frame'] = None
        if 'emotion' not in st.session_state:
            st.session_state['emotion'] = None
        if 'motivation' not in st.session_state:
            st.session_state['motivation'] = None
        if st.session_state['frame'] is not None:
            st.markdown('''<div style="display:flex;justify-content:center;align-items:center;margin-bottom:18px;">
                <img src="data:image/png;base64,{}" style="border-radius:18px;box-shadow:0 4px 24px rgba(44,62,80,0.18);border:2px solid #007aff;max-width:340px;"/>
            </div>'''.format(base64.b64encode(Image.fromarray(st.session_state['frame']).tobytes()).decode()), unsafe_allow_html=True)
        if capture:
            import cv2
            from deepface import DeepFace
            import numpy as np
            cap = cv2.VideoCapture(0)
            # Warm up the camera for a few frames for reliability
            for _ in range(3):
                cap.read()
            ret, frame = cap.read()
            cap.release()
            if ret and frame is not None:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                st.session_state['frame'] = rgb_frame
                st.session_state['emotion'] = None
                st.session_state['motivation'] = None
                st.image(rgb_frame, caption="Captured Image", use_container_width=True, output_format="PNG")
                img_path = os.path.join(person_dir, f"face_{len(os.listdir(person_dir)) + 1}.png")
                cv2.imwrite(img_path, cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))
                try:
                    # Only one analysis for speed
                    result = DeepFace.analyze(rgb_frame, actions=['emotion'], enforce_detection=False)
                    if isinstance(result, list):
                        result = result[0]
                    emotion = result.get('dominant_emotion', None)
                    if emotion:
                        motivation = get_motivation(emotion)
                        st.session_state['emotion'] = emotion
                        st.session_state['motivation'] = motivation
                        with open(os.path.join(person_dir, f"emotion_{len(os.listdir(person_dir))}.txt"), "w") as f:
                            f.write(f"Emotion: {emotion}\nMotivation: {motivation}")
                    else:
                        st.error("Could not detect emotion.")
                except Exception as e:
                    st.error(f"Error analyzing emotion: {e}")
            else:
                st.error("Could not access webcam. Please ensure your camera is connected and not in use by another application.")
        if retake:
            st.session_state['frame'] = None
            st.session_state['emotion'] = None
            st.session_state['motivation'] = None
            st.success("Image cleared. Please capture again.")
        if reset_btn:
            st.session_state['emotion'] = None
            st.session_state['motivation'] = None
            st.session_state['frame'] = None
            st.success("Reset!")
        if st.session_state['emotion']:
            st.markdown(f'''
            <div class="result-card" style="margin-top:18px;">
                <div class="emotion-title">Detected Emotion: {st.session_state['emotion'].capitalize()}</div>
                <div class="motivation-text">{st.session_state['motivation']}</div>
            </div>
            ''', unsafe_allow_html=True)
    elif mode == "Video":
        st.markdown("<div style='margin-bottom:12px'></div>", unsafe_allow_html=True)
        video_mode = st.radio("Video Mode", ["Record and Analyze", "Live Detection"], horizontal=True)
        if video_mode == "Record and Analyze":
            st.info("Click 'Record Video' to record a short video and analyze emotions.")
            record_btn = st.button("Record Video", key="record_video_btn")
            if record_btn:
                st.warning("Video recording feature is not implemented in this demo.")
                # Placeholder for video recording and analysis logic
        elif video_mode == "Live Detection":
            st.info("Click 'Start Live Video' for real-time emotion detection.")
            video_active = st.button("Start Live Video", key="live_video_btn")
            if video_active:
                st.warning("Press 'Stop' above to end live video.")
                stop_video = st.button("Stop Live Video", key="main_stop_video_btn")
                st.session_state['video_stop'] = False if not stop_video else True
                import cv2
                from deepface import DeepFace
                import numpy as np
                cap = cv2.VideoCapture(0)
                frame_placeholder = st.empty()
                emotion_placeholder = st.empty()
                import time
                while cap.isOpened() and not st.session_state.get('video_stop', False):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    try:
                        result = DeepFace.analyze(rgb_frame, actions=['emotion'], enforce_detection=False)
                        if isinstance(result, list):
                            result = result[0]
                        emotion = result.get('dominant_emotion', None)
                        score = result['emotion'][emotion] if emotion and 'emotion' in result else None
                        motivation = get_motivation(emotion)
                        emotion_placeholder.markdown(f"<div class='result-card' style='border:2px solid #0984e3;'>"
                                                   f"<div class='emotion-title' style='font-size:2.5rem;color:#0984e3;'>True Emotion: {emotion.capitalize() if emotion else 'Unknown'}</div>"
                                                   f"<div style='font-size:1.1rem;color:#555;'>Confidence: {score:.1f}%</div>"
                                                   f"<div class='motivation-text'>{motivation}</div>"
                                                   "</div>", unsafe_allow_html=True)
                    except Exception as e:
                        emotion_placeholder.error(f"Error analyzing emotion: {e}")
                    pil_img = Image.fromarray(rgb_frame)
                    buf = io.BytesIO()
                    pil_img.save(buf, format='PNG')
                    byte_im = buf.getvalue()
                    base64_img = base64.b64encode(byte_im).decode()
                    frame_placeholder.markdown(f'<img src="data:image/png;base64,{base64_img}" class="live-video-img" width="100%"/>', unsafe_allow_html=True)
                    time.sleep(0.15)
                cap.release()
                st.session_state['video_stop'] = False
                st.success("Live video stopped.")

## Main App Content (person management)
st.markdown('<div style="margin-top:60px"></div>', unsafe_allow_html=True)
