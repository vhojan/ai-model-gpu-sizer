# Use a slim Python base image
FROM python:3.11-slim

# Set environment variables to avoid interactive prompts during install
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Streamlit-specific configs
ENV STREAMLIT_SERVER_PORT=3000
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false

# Copy app source code
COPY . .

# Force copy config.toml separately (even if . was already copied)
COPY .streamlit/config.toml /root/.streamlit/config.toml

# Expose the port and run
EXPOSE 3000
CMD ["streamlit", "run", "app.py"]
