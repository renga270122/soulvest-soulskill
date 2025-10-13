import streamlit as st
from streamlit_lottie import st_lottie
import requests

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

career_lottie = load_lottie("https://lottie.host/1c3a3b7e-2c9f-4e4a-9c3e-8c7d1f7b9e3f/animation.json")

st.set_page_config(page_title="SoulSkill", page_icon="✨", layout="centered")

st.title("✨ SoulSkill: Resume Builder")
st.subheader("Empower your career with clarity and soul")

if career_lottie:
    st_lottie(career_lottie, height=200)

st.text_input("🌟 Soulful Summary")
st.text_area("🧠 Skills & Strengths")
st.text_area("💼 Experience Highlights")
st.text_area("🎨 Passion Projects")

if st.button("Generate Resume"):
    st.success("Your resume has been generated! (Download feature coming soon)")
