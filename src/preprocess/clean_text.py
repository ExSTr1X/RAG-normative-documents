import re
from src.config import RAW_TEXT_PATH, CLEAN_TEXT_PATH


def load_raw_pages():
    text = RAW_TEXT_PATH.read_text(encoding="utf-8")
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


def clean_text_block(text: str) -> str:
    # минимальная очистка: убираем лишние пробелы, дублирующиеся пустые строки
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_pages(pages):
    for p in pages:
        p["text"] = clean_text_block(p["text"])

        # ДОБАВЛЯЕМ в общий clean-файл
        with open(CLEAN_TEXT_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n\n=== Страница {p['page']} ===\n")
            f.write(p["text"])

    print("✨ Предобработка завершена")
