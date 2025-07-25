
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Model GPU Sizer", layout="centered")

@st.cache_data
def load_data():
    models = pd.read_csv("model_catalog.csv")
    gpus = pd.read_csv("gpu_catalog.csv")
    return models, gpus

models, gpus = load_data()

st.title("🧠 AI Model GPU Sizer")
st.subheader("Select your model, user count, and latency goal to get a sizing recommendation.")

# Model selector
selected_model = st.selectbox("Choose a model", models["Model"].unique())
model_info = models[models["Model"] == selected_model].iloc[0]

# Show model metadata
with st.expander("🔍 Model Details", expanded=True):
    st.markdown(f"""
**Model:** {model_info["Model"]}  
**Parameters:** {model_info["Parameters"]}  
**Weights Size (FP16):** {model_info["Weights Size (FP16, GB)"]} GB  
**VRAM Required:** {model_info["VRAM Required (GB)"]} GB  
**Base Latency:** {model_info["Base Latency (s)"]} s  
**Architecture:** {model_info["Architecture"]}  
**Intended Use:** {model_info["Intended Use"]}
    """)

# User input
users = st.slider("Number of concurrent users", min_value=1, max_value=100, value=10)
latency_target = st.slider("Latency goal (seconds)", min_value=0.2, max_value=5.0, value=1.0, step=0.1)

# Estimate VRAM needs
total_vram_required = model_info["VRAM Required (GB)"] * users
st.markdown(f"#### 📊 Total VRAM Required: {total_vram_required:.1f} GB")

# Suggest GPUs
eligible_gpus = gpus[gpus["Memory (GB)"] >= model_info["VRAM Required (GB)"]]
eligible_gpus = eligible_gpus.sort_values(by="FP16 TFLOPs", ascending=False)

if not eligible_gpus.empty:
    st.success("✅ Compatible GPU Configurations:")
    st.dataframe(eligible_gpus[["Model", "Memory (GB)", "FP16 TFLOPs", "NVLink Support"]].reset_index(drop=True), use_container_width=True)
else:
    st.error("❌ No single GPU meets the model's memory requirements.")
