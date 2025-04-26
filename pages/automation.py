import streamlit as st
from database_utils import search_properties, search_buyers
import sounddevice as sd
import soundfile as sf
import numpy as np
import os
from datetime import datetime

def automation_page():
    st.title("صفحة الأتمتة")

    # Audio Recording Section
    st.header("تسجيل الصوت")
    if st.button("بدء التسجيل"):
        st.info("جاري التسجيل... اضغط على زر إيقاف التسجيل عندما تنتهي")
        duration = st.slider("مدة التسجيل (بالثواني)", 1, 60, 10)
        sample_rate = 44100
        
        # Record audio
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        
        # Save the recording
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recordings/recording_{timestamp}.wav"
        os.makedirs("recordings", exist_ok=True)
        sf.write(filename, recording, sample_rate)
        
        st.success(f"تم حفظ التسجيل في: {filename}")
        st.audio(filename)
 

    # AI Question Answering Section
    st.header("الأسئلة الذكية")
    question = st.text_area("اطرح سؤالك هنا", 
                          placeholder="مثال: ما هي العقارات التي قد تهم المشتري X؟")
    
    if question:
        st.write("سيتم معالجة سؤالك قريباً...")
        # TODO: Add AI question answering functionality 