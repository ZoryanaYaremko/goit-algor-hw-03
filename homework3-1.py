from pathlib import Path
import argparse
import shutil

def parse_args():
    parser = argparse.ArgumentParser(description="Копіювання файлів з сортуванням за розширеннями.")
    parser.add_argument("--source", type=Path, help="Шлях до вихідної директорії (опціонально)")
    parser.add_argument("--dest", type=Path, default=Path("dist"), help="Шлях до директорії призначення")
    parser.add_argument("--create-source", action="store_true", help="Створити нову вихідну директорію")
    parser.add_argument("--ext", nargs='*', help="Список розширень для копіювання (опціонально)")
    return parser.parse_args()

def create_sample_files(directory):
    """Створює файли з різними розширеннями в заданій директорії."""
    files = {
        "example.txt": "Це текстовий файл.",
        "image.jpg": "Фейкові дані для зображення.",
        "document.pdf": "Фейкові дані для PDF документу.",
        "script.py": "print('Це приклад скрипта на Python')",
        "archive.zip": "PK\x03\x04\n",  # Початок файлу ZIP
    }
    try:
        for filename, content in files.items():
            file_path = directory / filename
            with open(file_path, 'w') as file:
                file.write(content)
        print(f"Файли зразків створено у директорії {directory}.")
    except Exception as e:
        print(f"Помилка при створенні файлів зразків: {e}")

def create_source_directory(source):
    try:
        source.mkdir(parents=True, exist_ok=True)
        print(f"Директорію {source} створено.")
        create_sample_files(source)
    except Exception as e:
        print(f"Помилка при створенні директорії {source}: {e}")

def copy_files(src, dst, extensions=None):
    try:
        for item in src.rglob('*'):
            if item.is_file():
                ext = item.suffix.lstrip('.').lower()
                if extensions and ext not in extensions:
                    continue
                dest_dir = dst / ext
                dest_dir.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.copy2(item, dest_dir / item.name)
                    print(f"Файл {item} скопійовано до {dest_dir}")
                except Exception as e:
                    print(f"Помилка при копіюванні файлу {item}: {e}")
    except Exception as e:
        print(f"Помилка при обробці файлів: {e}")

def main():
    args = parse_args()

    if args.create_source:
        if not args.source:
            args.source = Path("new_source_directory")
        create_source_directory(args.source)

    if not args.source or not args.source.exists():
        print("Не вказано або не існує вихідної директорії. Створено нову вихідну директорію за замовчуванням.")
        args.source = Path("new_source_directory")
        create_source_directory(args.source)

    print(f"Копіювання з {args.source} до {args.dest}")
    args.dest.mkdir(parents=True, exist_ok=True)
    copy_files(args.source, args.dest, args.ext)

if __name__ == "__main__":
    main()








