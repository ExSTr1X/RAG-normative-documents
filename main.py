import os

from src.extract.pdf_reader import extract_pdf
from src.extract.docx_reader import extract_docx
from src.extract.txt_reader import extract_txt

from src.preprocess.clean_text import clean_pages, load_raw_pages
from src.chunking.segment import build_chunks
from src.index.build_faiss import build_index
from src.rag.engine import RagEngine
from src.config import FAISS_INDEX_PATH


def full_pipeline(path: str, filetype: str):
    print("\n=== ЭТАП 1: Извлечение текста ===")

    if filetype == "pdf":
        extract_pdf(path)
    elif filetype == "docx":
        extract_docx(path)
    elif filetype == "txt":
        extract_txt(path)

    print("\n=== ЭТАП 2: Предобработка ===")
    pages_raw = load_raw_pages()
    clean_pages(pages_raw)

    print("\n=== ЭТАП 3: Сегментация ===")
    build_chunks()

    print("\n=== ЭТАП 4: Построение FAISS индекса ===")
    build_index()

    print("\n🔥 Документ успешно загружен, очищен, сегментирован и проиндексирован!")
    print("Теперь можно переходить в режим вопросов.")


def main():
    while True:
        print("\n📚 RAG по нормативным документам")
        print("1 — Загрузить PDF")
        print("2 — Загрузить DOCX")
        print("3 — Загрузить TXT")
        print("4 — Режим вопросов")
        print("5 — Выход")

        choice = input("Выбор: ").strip()

        # --- Загрузка PDF ---
        if choice == "1":
            path = input("Введите путь к PDF файлу: ").strip().strip('"').strip("'")
            full_pipeline(path, "pdf")

        # --- Загрузка DOCX ---
        elif choice == "2":
            path = input("Введите путь к DOCX файлу: ").strip().strip('"').strip("'")
            full_pipeline(path, "docx")

        # --- Загрузка TXT ---
        elif choice == "3":
            path = input("Введите путь к TXT файлу: ").strip().strip('"').strip("'")
            full_pipeline(path, "txt")

        # --- Режим вопросов ---
        elif choice == "4":
            if not os.path.exists(FAISS_INDEX_PATH):
                print("\n❌ Индекс ещё не создан.")
                print("Сначала загрузите документ (PDF/DOCX/TXT).")
                continue

            engine = RagEngine()
            print("\n=== Режим вопросов ===")

            while True:
                q = input("\nВопрос (quit для выхода): ").strip()
                if q.lower() == "quit":
                    break

                result = engine.answer(q)

                print("\n=== Ответ ===")
                print(result["answer"])

                print("\n=== Использованные пункты ГОСТ ===")
                for c in result["citations"]:
                    print(f"- Пункт {c['ref']} (стр. {c['page']})")

        elif choice == "5":
            print("👋 Выход.")
            break

        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()
