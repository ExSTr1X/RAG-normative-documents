import fitz
from src.config import RAW_TEXT_PATH, PROCESSED_DIR
from src.extract.normalize import normalize_text


def extract_pdf(path: str):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(path)
    pages = []

    for i, page in enumerate(doc, start=1):
        raw_text = page.get_text("text")
        text = normalize_text(raw_text)
        pages.append({"page": i, "text": text})

        # ДОБАВЛЯЕМ текст к общему raw-файлу
        with open(RAW_TEXT_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n\n=== Страница {i} ===\n")
            f.write(text)

        print(f"📄 Страница {i} извлечена")

    print("Всего страниц:", len(pages))
    return pages
