import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(page_title="AI Model GPU Sizer", page_icon="🧠", layout="centered")

st.title("🧠 AI Model GPU Sizer")
st.markdown("Select your model, user count, and latency goal to find the recommended GPU configuration.")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("sizing_matrix.csv")

df = load_data()

# --- UI Controls ---
models = sorted(df["Model"].unique())
latencies = sorted(df["Latency Target (s)"].unique())

selected_model = st.selectbox("Model", models)
selected_latency = st.selectbox("Target First-Token Latency", latencies)
selected_users = st.slider("Concurrent Users", min_value=1, max_value=50, value=10)

# --- Filter Logic ---
matches = df[
    (df["Model"] == selected_model) &
    (df["Latency Target (s)"] == selected_latency) &
    (df["Users"] >= selected_users)
].sort_values("Users")

# --- Results Display ---
if not matches.empty:
    st.success(f"Recommended GPU configurations for {selected_model} with ≥{selected_users} users and latency {selected_latency}:")
    st.dataframe(
        matches[["Quantization", "GPUs Needed", "GPU Type", "RAM (GB)", "CPUs"]],
        use_container_width=True
    )
else:
    st.warning("No matching configuration found. Try reducing user count or changing the latency target.")
