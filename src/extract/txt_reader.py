from pathlib import Path
import chardet
from src.config import RAW_TEXT_PATH, PROCESSED_DIR
from src.extract.normalize import normalize_text


def extract_txt(path: str):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    raw_bytes = path.read_bytes()
    text = normalize_text(raw_bytes)

    # ДОБАВЛЯЕМ текст к общему raw-файлу
    with open(RAW_TEXT_PATH, "a", encoding="utf-8") as f:
        f.write("\n\n=== Страница 1 ===\n")
        f.write(text)

    print(f"📄 TXT файл загружен: {path}")
    return [{"page": 1, "text": text}]
