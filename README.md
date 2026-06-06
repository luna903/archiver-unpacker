# Python Console Archiver Utility

A robust console utility developed for archiving and extracting files/directories using `zstd` and `bz2` algorithms. It leverages the new `compression.zstd` module introduced in the Python 3.14 standard library.

## Features
- **Automatic Algorithm Routing:** Dynamically selects the compression/extraction algorithm (`zstd` or `bz2`) based on the target file extension.
- **Directory Support:** Automatically utilizes `tarfile` to package directories before compression.
- **Stream Pipeline:** Uses file object mapping (`fileobj`) for stream processing, ensuring $O(1)$ memory complexity when handling large datasets.
- **Security:** Implements `filter='data'` during extraction to prevent path traversal attacks.

## Prerequisites
- **Python 3.14** or higher (requires standard library `compression.zstd`).

## Command Line Arguments

| Argument | Type | Description |
| :--- | :--- | :--- |
| `source` | Positional | Path to the source file or directory. |
| `output` | Positional | Path to the output archive (must end with `.zst` or `.bz2`) or extraction target directory. |
| `-x`, `--extract`| Optional | Flag to enable extraction mode. If omitted, compression mode is used. |
| `-h`, `--help` | Optional | Show the help message and exit. |

## Usage Examples

### 1. Archiving (Compression)
To compress a directory or file, provide the source path and the desired output archive name.

**Compressing a directory using zstd:**
```bash
python archiver.py test_data archive.tar.zst


---
<img width="1497" height="734" alt="5a68f1c858da308ec428bb12e9f121b6" src="https://github.com/user-attachments/assets/521f7cc5-c140-4e6c-872d-d3cd762bd7db" />
