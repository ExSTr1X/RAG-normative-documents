from docx import Document
from src.config import RAW_TEXT_PATH, PROCESSED_DIR
from src.extract.normalize import normalize_text


def extract_docx(path: str):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    doc = Document(path)
    raw_text = "\n".join(p.text for p in doc.paragraphs)
    text = normalize_text(raw_text)

    # ДОБАВЛЯЕМ текст к общему raw-файлу
    with open(RAW_TEXT_PATH, "a", encoding="utf-8") as f:
        f.write("\n\n=== Страница 1 ===\n")
        f.write(text)

    print("📄 DOCX извлечён")
    return [{"page": 1, "text": text}]
