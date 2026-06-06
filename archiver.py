import argparse
import time
import tarfile
import sys
from pathlib import Path
from compression import zstd


def get_algorithm(filename):
    """从文件名提取压缩算法"""
    if filename.lower().endswith(".bz2"):
        return "bz2"
    elif filename.lower().endswith(".zst"):
        return "zst"
    raise ValueError(f"不支持的格式: {filename}，必须以 .zst 或 .bz2 结尾")


def process_archive(source, output, is_extract):
    """处理归档与解压缩"""
    source_path = Path(source)

    if is_extract:
        algorithm = get_algorithm(source)
        target_dir = Path(output)
        if not source_path.exists():
            raise FileNotFoundError(f"找不到压缩包: {source_path}")
        print(f"🔄 解压: {source_path} -> {target_dir} ({algorithm})")
        target_dir.mkdir(parents=True, exist_ok=True)
        if algorithm == "zst":
            with zstd.ZstdFile(source_path, "rb") as zf:
                with tarfile.open(fileobj=zf, mode="r") as tar:
                    tar.extractall(path=target_dir, filter="data")
        else:
            with tarfile.open(source_path, "r:bz2") as tar:
                tar.extractall(path=target_dir, filter="data")
        print("✅ 解压成功")

    else:
        algorithm = get_algorithm(output)
        if not source_path.exists():
            raise FileNotFoundError(f"找不到源文件: {source_path}")
        print(f"🔄 压缩: {source_path} -> {output} ({algorithm})")
        if algorithm == "zst":
            with zstd.ZstdFile(output, "wb") as zf:
                with tarfile.open(fileobj=zf, mode="w") as tar:
                    tar.add(source_path, arcname=source_path.name)
        else:
            with tarfile.open(output, "w:bz2") as tar:
                tar.add(source_path, arcname=source_path.name)
        print("✅ 压缩成功")


def main():
    parser = argparse.ArgumentParser(
        description="自动归档与解压缩工具 (支持 zstd & bz2)",
        epilog=(
            "示例:\n"
            "  python archiver.py data.txt archive.zst        # 压缩文件\n"
            "  python archiver.py ./my_dir backup.bz2         # 压缩目录\n"
            "  python archiver.py -x archive.zst ./out        # 解压 .zst\n"
            "  python archiver.py -x backup.bz2  ./out        # 解压 .bz2\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("source", help="源文件/目录（压缩模式）或压缩包路径（解压模式）")
    parser.add_argument("output", help="目标压缩包（压缩模式，须以 .zst/.bz2 结尾）或解压目录")
    parser.add_argument("-x", "--extract", action="store_true", help="解压模式（默认为压缩模式）")
    args = parser.parse_args()

    start = time.perf_counter()
    try:
        process_archive(args.source, args.output, args.extract)
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"Execution time: {time.perf_counter() - start:.4f} seconds")


if __name__ == "__main__":
    main()