from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_PATH = BASE_DIR / "data" / "DPM-2025-VOLUME-II.pdf"

VECTOR_DB_PATH = BASE_DIR / "vectorstore"

CHUNK_SIZE = 1200

CHUNK_OVERLAP = 150

TOP_K = 5

SIMILARITY_THRESHOLD = 0.70

EMBEDDING_MODEL = "text-embedding-3-small"

LLM_MODEL = "gpt-4.1"