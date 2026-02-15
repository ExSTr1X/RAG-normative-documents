import re
import json
from src.config import CLEAN_TEXT_PATH, CHUNKS_PATH

re_top = re.compile(r"^(?P<num>\d+)\s+(?P<title>.+)$")
re_sub = re.compile(r"^(?P<num>\d+(?:\.\d+)+)\s*(?P<title>.*)$")


def load_pages():
    text = CLEAN_TEXT_PATH.read_text(encoding="utf-8")
    pages = []
    blocks = text.split("=== Страница ")
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        parts = block.split("\n", 1)
        if len(parts) == 2:
            page_num, page_text = parts
            try:
                page = int(page_num.strip("= \n"))
            except ValueError:
                page = 1
            pages.append({"page": page, "text": page_text.strip()})
    return pages


def build_chunks():
    pages = load_pages()
    chunks = []

    for p in pages:
        lines = p["text"].splitlines()
        current_id = None
        buffer = []

        for line in lines:
            ln = line.strip()
            if not ln:
                continue

            m_top = re_top.match(ln)
            if m_top:
                if current_id and buffer:
                    chunks.append(
                        {
                            "id": current_id,
                            "text": "\n".join(buffer).strip(),
                            "page": p["page"],
                        }
                    )
                current_id = m_top.group("num")
                buffer = [m_top.group("title")]
                continue

            m_sub = re_sub.match(ln)
            if m_sub:
                if current_id and buffer:
                    chunks.append(
                        {
                            "id": current_id,
                            "text": "\n".join(buffer).strip(),
                            "page": p["page"],
                        }
                    )
                current_id = m_sub.group("num")
                title = m_sub.group("title").strip()
                buffer = [title] if title else []
                continue

            if current_id:
                buffer.append(ln)

        if current_id and buffer:
            chunks.append(
                {"id": current_id, "text": "\n".join(buffer).strip(), "page": p["page"]}
            )

    # ПРАВИЛЬНАЯ запись JSONL
    with open(CHUNKS_PATH, "a", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"✅ Сегментация завершена. Чанков добавлено: {len(chunks)}")
