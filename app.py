import streamlit as st
import threading
import recorder
import transcriptor
import painter

if "record_active" not in st.session_state:
    st.session_state.record_active = threading.Event()
    st.session_state.recording_status = "Başlamaya Hazırız!"
    st.session_state.recording_completed = False
    st.session_state.latest_image = ""
    st.session_state.messages = []
    st.session_state.frames = []


def start_recording():
    st.session_state.record_active.set()
    st.session_state.frames = []
    st.session_state.recording_status = "🔴 **Sesiniz Kaydediliyor...**"
    st.session_state.recording_completed = False

    threading.Thread(target = recorder.record, args = (st.session_state.record_active, st.session_state.frames)).start()

def stop_recording():
    st.session_state.record_active.clear()
    st.session_state.recording_status = "🟢 **Kayıt Tamamlandı!**"
    st.session_state.recording_completed = True




st.set_page_config(page_title="Voicedraw", page_icon="./icons/app_icon.png", layout="wide")
st.image("./icons/top_banner.png", use_column_width=True )
st.title("Voicedraw : Sesli Çizim")

st.divider()

col_audio, col_image = st.columns([1,4])

with col_audio:
    st.subheader("Ses Kayıt")
    st.divider()
    status_message = st.info(st.session_state.recording_status)
    st.divider()

    subcol_left, subcol_right = st.columns([1,2])

    with subcol_left:
        start_btn = st.button(label="Başlat", on_click=start_recording, disabled=st.session_state.record_active.is_set())
        stop_btn = st.button(label="Durdur", on_click=stop_recording, disabled=not st.session_state.record_active.is_set())

    with subcol_right:
        recorded_audio = st.empty()
        
        if st.session_state.recording_completed:
            recorded_audio.audio( data = "voice_prompt.wav")



    st.divider()
    latest_image_use = st.checkbox(label="Son Resmi Kullan")



