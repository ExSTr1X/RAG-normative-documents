from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_TEXT_PATH = PROCESSED_DIR / "out_raw.txt"
CLEAN_TEXT_PATH = PROCESSED_DIR / "out_clean.txt"
CHUNKS_PATH = PROCESSED_DIR / "chunks.jsonl"
FAISS_INDEX_PATH = PROCESSED_DIR / "faiss.index"
FAISS_META_PATH = PROCESSED_DIR / "faiss_meta.pkl"

MODEL_NAME = "intfloat/multilingual-e5-base"
