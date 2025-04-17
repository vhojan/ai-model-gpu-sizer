import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Model GPU Sizer", page_icon="🧠")
st.title("🧠 AI Model GPU Sizer")

st.markdown("Estimate the required on-prem hardware for AI model inference workloads.")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("sizing_matrix.csv")

df = load_data()

# Sidebar filters
with st.sidebar:
    st.header("Configuration")
    model = st.selectbox("Model", sorted(df["Model"].unique()))
    quant = st.selectbox("Quantization", sorted(df["Quantization"].unique()))
    latency = st.selectbox("Latency Target", sorted(df["Latency Target (s)"].unique()))
    users = st.slider("Minimum Concurrent Users", 1, 50, 5)

# Filter data
st.write("Available data preview:", df.head(10))
st.write("You selected:", model, quant, latency, users)

filtered = df[
    (df["Model"] == model) &
    (df["Quantization"] == quant) &
    (df["Latency Target (s)"] == latency) &
    (df["Users"] >= users)
]

# Display
if not filtered.empty:
    st.success(f"Found {len(filtered)} matching configuration(s):")
    # pyright: ignore[reportUndefinedVariable]
    st.dataframe(filtered.reset_index(drop=True), use_container_width) # type: ignore