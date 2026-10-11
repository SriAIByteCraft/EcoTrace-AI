# EcoTrace AI

EcoTrace AI is an environmental waste tracking and recycling guidance application.

## Features
- Waste disposal guidance
- AI assistant powered by a local Llama model
- Waste action recording
- Dashboard with waste statistics and charts

## Technologies
- Python
- Streamlit
- Pandas
- Ollama
- Llama 3.2

## Setup

1. Install Python.
2. Install Ollama from https://ollama.com/download
3. Download the model:

   ollama pull llama3.2:1b

4. Install dependencies:

   pip install -r requirements.txt

5. Run the app:

   streamlit run eco_trace_app.py

## Note
This is a prototype. Follow local municipal guidance for waste disposal.
The AI assistant uses Ollama's local API.
