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
** 创建测试文件**

<img width="1497" height="734" alt="5a68f1c858da308ec428bb12e9f121b6" src="https://github.com/user-attachments/assets/03bc0731-e2d5-474d-8c9e-535a0b43a3cc" />

**Compressing a directory using zstd:**

```bash
python archiver.py test_data archive.tar.zst

```
<img width="2007" height="1080" alt="image" src="https://github.com/user-attachments/assets/5f9a684e-4f8a-4a05-b143-1cf1d262fe96" />

**解压文件**

```bash
python archiver.py -x archive.tar.zst out_folder

```
<img width="1857" height="1245" alt="image" src="https://github.com/user-attachments/assets/64791f53-7380-4580-8318-b4147973b1bb" />

**自动识别（压缩成zst 格式）**
```bash
python archiver.py test_data output.tar.zst

``` 
<img width="1860" height="1308" alt="image" src="https://github.com/user-attachments/assets/6e31802f-6df4-4bab-b262-e316ad58b7d0" />

**自动识别（压缩成bz2 格式）**
```bash
python archiver.py test_data output.tar.zst

```
<img width="1842" height="1392" alt="image" src="https://github.com/user-attachments/assets/a1094abb-a8a4-42d3-b01b-a0c08f79efe1" />

**自动识别（解压zst）**
```bash
python archiver.py -x output.tar.zst out_folder

```
<img width="1821" height="1404" alt="image" src="https://github.com/user-attachments/assets/feacc811-42b8-4f15-864d-598c54144e10" />


**自动识别（解压bz2）**
```bash
python archiver.py -x output.tar.bz2 out_folder

```
<img width="1844" height="1392" alt="image" src="https://github.com/user-attachments/assets/bcfdf1c5-02af-44ec-be19-cb3a339a1d6a" />


**argparse 帮助信息**
```bash
python archiver.py -h

```
<img width="840" height="345" alt="image" src="https://github.com/user-attachments/assets/a4033093-af35-4800-9f8e-aa47ec343513" />
