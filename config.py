import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    try:
        NVIDIA_API_KEY = st.secrets["NVIDIA_API_KEY"]
    except Exception:
        NVIDIA_API_KEY = None

if not NVIDIA_API_KEY:
    raise ValueError("NVIDIA_API_KEY not found")

LLM_MODEL = "your_existing_model_name"

PDF_FOLDER = "web_data"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "college_admission"

LLM_MODEL = "nvidia/nemotron-3.5-super-vl-120b-a12b"
EMBEDDING_MODEL = "nvidia/nv-embedqa-e5-v5"