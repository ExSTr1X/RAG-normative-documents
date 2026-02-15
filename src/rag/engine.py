import re
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from src.config import FAISS_INDEX_PATH, FAISS_META_PATH, MODEL_NAME
from src.rag.perplexity_api import PerplexityClient


class RagEngine:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))

        with open(FAISS_META_PATH, "rb") as f:
            data = pickle.load(f)

        self.metas = data["metas"]
        self.texts = data["texts"]

        self.llm = PerplexityClient()

    def search(self, query, top_k=8):
        q = f"query: {query}"
        q_vec = self.model.encode([q], normalize_embeddings=True)
        q_vec = np.array(q_vec, dtype="float32")

        scores, ids = self.index.search(q_vec, top_k)

        results = []
        for score, idx in zip(scores[0], ids[0]):
            results.append(
                {
                    "score": float(score),
                    "meta": self.metas[idx],
                    "text": self.texts[idx],
                }
            )
        return results

    def build_prompt(self, query, chunks):
        context = ""
        for c in chunks:
            ref = c["meta"]["id"] or c["meta"]["title"]
            context += f"\nПункт {ref} (стр. {c['meta']['page']}):\n{c['text']}\n"

        prompt = f"""
Ты — эксперт по ГОСТам и нормативным документам.

Используй ТОЛЬКО предоставленный контекст, не придумывай ничего сверх него.

Вопрос пользователя:
{query}

Контекст:
{context}

Сформулируй точный, нормативно корректный ответ.
"""
        return prompt

    def answer(self, query):
        candidates = self.search(query, top_k=10)

        # простейший rerank
        q_tokens = set(re.findall(r"\w+", query.lower()))
        for c in candidates:
            t_tokens = set(re.findall(r"\w+", c["text"].lower()))
            c["score"] += len(q_tokens & t_tokens) * 0.01

        candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:4]

        prompt = self.build_prompt(query, candidates)
        answer = self.llm.ask(prompt)

        return {
            "answer": answer,
            "citations": [
                {
                    "ref": c["meta"]["id"] or c["meta"]["title"],
                    "page": c["meta"]["page"],
                }
                for c in candidates
            ],
        }
