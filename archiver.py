import argparse
import time
import tarfile
import sys
from pathlib import Path
from compression import zstd


def get_algorithm(filename):
    if filename.lower().endswith(".bz2"):
        return "bz2"
    if filename.lower().endswith(".zst"):
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
            with zstd.ZstdFile(source_path, "rb") as zf:
                with tarfile.open(fileobj=zf, mode="r") as tar:
                    tar.extractall(path=target_dir, filter="data")
        else:
            with tarfile.open(source_path, "r:bz2") as tar:
                tar.extractall(path=target_dir, filter="data")
        print("Распаковка выполнена успешно")
    else:
        algorithm = get_algorithm(output)
        if not source_path.exists():
            raise FileNotFoundError(f"Источник не найден: {source_path}")
        print(f"Архивация: {source_path} -> {output} ({algorithm})")
        if algorithm == "zst":
            with zstd.ZstdFile(output, "wb") as zf:
                with tarfile.open(fileobj=zf, mode="w") as tar:
                    tar.add(source_path, arcname=source_path.name)
        else:
            with tarfile.open(output, "w:bz2") as tar:
                tar.add(source_path, arcname=source_path.name)
        print("Архивация выполнена успешно")


def main():
    parser = argparse.ArgumentParser(
        description="Утилита архивации и распаковки (zstd & bz2)",
        epilog=(
            "Примеры:\n"
            "  python archiver.py data.txt  archive.zst   # архивировать файл\n"
            "  python archiver.py ./my_dir  backup.bz2    # архивировать папку\n"
            "  python archiver.py -x archive.zst ./out    # распаковать .zst\n"
            "  python archiver.py -x backup.bz2  ./out    # распаковать .bz2\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("source", help="Файл/папка для архивации или путь к архиву при распаковке")
    parser.add_argument("output", help="Целевой архив (.zst/.bz2) или папка для распаковки")
    parser.add_argument("-x", "--extract", action="store_true", help="Режим распаковки")
    args = parser.parse_args()

    start = time.perf_counter()
    try:
        process_archive(args.source, args.output, args.extract)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"Execution time: {time.perf_counter() - start:.4f} seconds")


if __name__ == "__main__":
    main()