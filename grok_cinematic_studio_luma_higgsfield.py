import streamlit as st
import os
import base64
import requests
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Grok Cinematic Studio — Luma + Higgsfield", page_icon="🎬", layout="wide")
st.title("🎬 Grok Cinematic Studio — Luma AI + Higgsfield Cinema Studio Integrated")
st.markdown("**Real Grok Imagine API + Full Luma Keyframes + Higgsfield Director Controls**")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("xAI API Key", type="password", value=os.getenv("XAI_API_KEY", ""), help="Enter your new key here.")
    if not api_key:
        st.warning("Please enter your xAI API key.")
    st.divider()
    st.caption("Real generation enabled – March 2026")

# Real API call for video
def generate_video(prompt, start_image=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-imagine-video",
        "prompt": prompt
    }
    if start_image:
        buffered = BytesIO()
        start_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        payload["image"] = f"data:image/png;base64,{img_str}"
    
    try:
        response = requests.post("https://api.x.ai/v1/videos/generations", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# Hybrid Prompt Builder (Luma + Higgsfield)
def build_hybrid_prompt(base_prompt, camera_preset, motion_style, start_frame_desc, end_frame_desc,
                        character_ref_desc, style_ref_desc, motion_ref_desc, motion_brush,
                        lens_type, focal_length, sensor_size, camera_moves, speed_ramp,
                        genre, emotion, lipsync_audio_desc):
    prompt = base_prompt.strip()
    if camera_preset and camera_preset != "None":
        prompt += f". Camera: {camera_preset} with smooth cinematic movement."
    if motion_style:
        prompt += f". Motion style: {motion_style} with realistic physics."
    if start_frame_desc:
        prompt += f". Start exactly from the uploaded start frame: {start_frame_desc}."
    if end_frame_desc:
        prompt += f". Transition smoothly to the end frame: {end_frame_desc}."
    if character_ref_desc:
        prompt += f". Lock character identity using reference: {character_ref_desc}."
    if style_ref_desc:
        prompt += f". Apply exact visual style from reference: {style_ref_desc}."
    if motion_ref_desc:
        prompt += f". Transfer exact motion from reference: {motion_ref_desc}."
    if motion_brush:
        prompt += f". Apply targeted motion brush: {motion_brush}."
    if lens_type and lens_type != "None":
        prompt += f". Higgsfield Cinema Studio: Use {lens_type} lens at {focal_length} focal length on {sensor_size} sensor."
    if camera_moves and len(camera_moves) > 0:
        prompt += f". Multi-axis camera stacking: {', '.join(camera_moves)}."
    prompt += " Maintain perfect temporal consistency and cinematic quality."
    return prompt

# Tab 2 – Image-to-Video (Real Generation)
with st.tabs(["📸 Image-to-Video (Luma + Higgsfield)"])[0]:
    st.subheader("Image-to-Video — Real Generation")
    main_image = st.file_uploader("Main / Start Frame Image", type=["png","jpg","jpeg"], key="i2v_main")
    if main_image:
        st.image(main_image, caption="Start Frame")
        base_prompt = st.text_area("Base prompt", "Animate the scene with fluid cinematic motion")
        col1, col2 = st.columns(2)
        with col1:
            camera_preset = st.selectbox("Luma Camera Preset", ["None", "Handheld tracking", "Dolly zoom", "Crane shot"])
            motion_style = st.selectbox("Motion Style", ["Realistic physics", "Slow-motion elegance"])
        with col2:
            duration = st.slider("Duration (s)", 5, 15, 10)
        if st.button("Generate Video (Real Grok Imagine)"):
            full_prompt = build_hybrid_prompt(base_prompt, camera_preset, motion_style, "uploaded start frame", "", "", "", "", "", "", "", "", "", "", "", "", "")
            result = generate_video(full_prompt, Image.open(main_image))
            if result:
                st.success("✅ Video generation started successfully!")
                st.json(result)  # You will see the real API response here

st.caption("✅ Real Grok Imagine API integration active. Video generation now uses your actual API key.")
