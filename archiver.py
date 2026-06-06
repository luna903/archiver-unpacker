import argparse
import time
import tarfile
import sys
from pathlib import Path
from compression import zstd

def get_algorithm(filename):
    if filename.lower().endswith(".bz2"):
        return "bz2"
    elif filename.lower().endswith(".zst"):
        return "zst"
    raise ValueError(f"Неподдерживаемый формат: {filename}, файл должен оканчиваться на .zst или .bz2")

def process_archive(source, output, is_extract):
    source_path = Path(source)
    
    if is_extract:
        algorithm = get_algorithm(source)
        target_dir = Path(output)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Архив не найден: {source_path}")
            
        print(f"Распаковка: {source_path} -> {target_dir} ({algorithm})")
        target_dir.mkdir(parents=True, exist_ok=True)
        
        if algorithm == "zst":
            with zstd.open(source_path, 'rb') as zstd_file:
                with tarfile.open(fileobj=zstd_file, mode='r') as tar:
                    tar.extractall(path=target_dir, filter='data')
        else:
            with tarfile.open(source_path, f"r:{algorithm}") as tar:
                tar.extractall(path=target_dir, filter='data')
        print("Успешно")
        
    else:
        algorithm = get_algorithm(output)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Исходный файл не найден: {source_path}")
            
        print(f"Архивация: {source_path} -> {output} ({algorithm})")
        
        if algorithm == "zst":
            with zstd.open(output, 'wb') as zstd_file:
                with tarfile.open(fileobj=zstd_file, mode='w') as tar:
                    tar.add(source_path, arcname=source_path.name)
        else:
            with tarfile.open(output, f"w:{algorithm}") as tar:
                tar.add(source_path, arcname=source_path.name)
        print("Успешно")

def main():
    parser = argparse.ArgumentParser(
        description="Инструмент архивации и распаковки (поддержка zstd и bz2)"
    )
    parser.add_argument("source", help="Путь к исходному файлу или директории")
    parser.add_argument("output", help="Целевой файл или директория для распаковки")
    parser.add_argument("-x", "--extract", action="store_true", help="Режим распаковки")
    
    args = parser.parse_args()
    
    start_time = time.perf_counter()
    
    try:
        process_archive(args.source, args.output, args.extract)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    
    end_time = time.perf_counter()
    print(f"Время выполнения: {end_time - start_time:.4f} секунд")

if __name__ == "__main__":
    main()
