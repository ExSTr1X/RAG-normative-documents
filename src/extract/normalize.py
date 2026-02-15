import chardet
import re


def normalize_text(text_or_bytes):
    """
    Универсальная нормализация текста:
    - определение кодировки (если bytes)
    - декодирование
    - удаление мусорных символов
    - нормализация переносов
    """

    # Если пришли байты — определяем кодировку
    if isinstance(text_or_bytes, (bytes, bytearray)):
        detected = chardet.detect(text_or_bytes)
        encoding = detected.get("encoding", "utf-8")

        try:
            text = text_or_bytes.decode(encoding)
        except Exception:
            # fallback для Windows-1251
            text = text_or_bytes.decode("cp1251", errors="replace")
    else:
        # Если уже строка — просто используем
        text = text_or_bytes

    # Удаляем управляющие символы (кроме \n)
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text)

    # Нормализуем переносы строк
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Убираем лишние пробелы в начале/конце
    return text.strip()
