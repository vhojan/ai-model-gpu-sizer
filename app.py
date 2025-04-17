import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="AI Model GPU Sizer", page_icon="🧠", layout="centered")

st.title("🧠 AI Model GPU Sizer")
st.markdown("Get GPU recommendations for running large language models based on VRAM and latency requirements.")

# Load data
@st.cache_data
def load_data():
    models = pd.read_csv("model_catalog.csv")
    gpus = pd.read_csv("gpu_catalog.csv")
    return models, gpus

model_df, gpu_df = load_data()

# --- User Inputs ---
selected_model = st.selectbox("Choose an AI Model", sorted(model_df["Model"].unique()))
latency_target = st.selectbox("Target First-Token Latency", ["<1", "<2", "<3", "<5"])

# --- Matching Logic ---
def find_compatible_gpus(model_name, user_latency_target):
    selected = model_df[model_df["Model"] == model_name].iloc[0]
    required_vram = selected["VRAM Required (GB)"]
    base_latency = selected["Base Latency (s)"]

    results = []
    for _, gpu in gpu_df.iterrows():
        vram = gpu["VRAM (GB)"]
        latency_factor = gpu["Latency Factor"]
        max_nvlink = int(gpu["Max NVLink GPUs"]) if gpu["NVLink"] and gpu["Max NVLink GPUs"] != "-" else 1

        for count in range(1, max_nvlink + 1):
            total_vram = vram * count
            if total_vram >= required_vram:
                est_latency = round(base_latency * latency_factor / count, 2)
                if est_latency <= float(user_latency_target.replace("<", "")):
                    results.append({
                        "GPU Type": gpu["GPU Type"],
                        "Qty": count,
                        "Total VRAM (GB)": total_vram,
                        "Est. Latency (s)": est_latency,
                        "TFLOPs (FP16)": gpu["TFLOPs (FP16)"],
                        "TFLOPs (FP8)": gpu["TFLOPs (FP8)"],
                        "TFLOPs (BF16)": gpu["TFLOPs (BF16)"],
                        "TFLOPs (FP4)": gpu["TFLOPs (FP4)"],
                        "TOPs (INT8)": gpu["TOPs (INT8)"],
                        "Arch": gpu["Arch"],
                        "HGX System": gpu["HGX System"]
                    })
                break  # use smallest number of GPUs that work

    return pd.DataFrame(results)

# --- Display Results ---
results_df = find_compatible_gpus(selected_model, latency_target)

if not results_df.empty:
    st.success(f"Recommended GPU configurations for **{selected_model}** with latency target {latency_target}:")
    st.dataframe(results_df, use_container_width=True)
    csv = results_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download results as CSV", csv, "gpu_recommendations.csv", "text/csv")
else:
    st.warning("No matching GPU configurations found. Try relaxing the latency target or choosing another model.")
