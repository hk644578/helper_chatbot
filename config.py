import os
from dotenv import load_dotenv

load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    raise ValueError("NVIDIA_API_KEY not found in .env file")

PDF_FOLDER = "web_data"
CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "college_admission"

LLM_MODEL = "nvidia/nemotron-3-super-120b-a12b"
EMBEDDING_MODEL = "nvidia/nv-embedqa-e5-v5"