import json
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from src.config import CHUNKS_PATH, FAISS_INDEX_PATH, FAISS_META_PATH, MODEL_NAME


def build_index():
    model = SentenceTransformer(MODEL_NAME)

    texts = []
    metas = []

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                print("⚠ Пропущена повреждённая строка в chunks.jsonl")
                continue

            texts.append(obj["text"])
            metas.append({"id": obj["id"], "page": obj["page"]})

    if not texts:
        print("⚠ Нет чанков для индексации.")
        return

    embeddings = model.encode(texts, normalize_embeddings=True)
    embeddings = np.array(embeddings, dtype="float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(FAISS_INDEX_PATH))

    with open(FAISS_META_PATH, "wb") as f:
        pickle.dump({"texts": texts, "metas": metas}, f)

    print(f"🔥 Индекс построен. Всего чанков: {len(texts)}")
