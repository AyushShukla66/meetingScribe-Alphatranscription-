from services.report_generator import generate_report
import services.audio_capture as audio

import streamlit as st

from services.audio_capture import start_meeting, stop_meeting

st.set_page_config(
    page_title="MeetingScribe",
    page_icon="📝",
    layout="centered"
)

st.title("📝 MeetingScribe Alpha")

meeting_name = st.text_input("Meeting Name")

col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Start Meeting", use_container_width=True):
        start_meeting(meeting_name)
        st.success("Meeting Started")

with col2:
    if st.button("■ Stop Meeting", use_container_width=True):
        stop_meeting()
        st.success("Meeting Stopped")

if st.button("📄 Generate Executive Brief", use_container_width=True):

    if audio.current_meeting:
        generate_report(audio.current_meeting)
        st.success("Report Generated")
    else:
        st.error("No meeting found")
st.divider()

st.info("Status : Ready")