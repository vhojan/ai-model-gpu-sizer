# 🧠 AI Model GPU Sizer

**AI Model GPU Sizer** is a Streamlit web app that helps infrastructure architects, IT admins, and AI engineers determine the optimal on-prem hardware (GPUs, CPUs, RAM) needed to deploy large language models (LLMs) in air-gapped or customer-controlled environments.

This tool is especially useful for ISVs transitioning from cloud-native AI APIs (like OpenAI or Anthropic) to on-prem inference due to privacy, latency, or compliance requirements.

## 🚀 Features

- Select from popular open-source and commercial LLMs (LLaMA, GPT, Claude, Command R+)
- Filter by:
  - Model size
  - Quantization type
  - First-token latency target
  - Number of concurrent users
- See recommended GPU types and quantities
- Includes options for NVLink, Grace Hopper, and AMD MI300X hardware

## 🧪 Try it locally

Make sure you have Python 3 and Streamlit installed:

```bash
pip install streamlit pandas
