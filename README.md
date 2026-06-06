# Утилита архивации для консоли Python

Надёжная консольная утилита для архивации и извлечения файлов/директорий с использованием алгоритмов `zstd` и `bz2`. Использует новый модуль `compression.zstd`, введённый в стандартную библиотеку Python 3.14.

## Возможности

- **Автоматический выбор алгоритма:** Динамически выбирает алгоритм сжатия/распаковки (`zstd` или `bz2`) на основе расширения целевого файла.
- **Поддержка директорий:** Автоматически использует `tarfile` для упаковки директорий перед сжатием.
- **Потоковый конвейер:** Использует маппинг файловых объектов (`fileobj`) для потоковой обработки, обеспечивая сложность памяти $O(1)$ при работе с большими данными.
- **Безопасность:** Применяет `filter='data'` при извлечении для предотвращения атак обхода пути.
- 
## Требования

- **Python 3.14** или выше (требуется стандартная библиотека `compression.zstd`).
- 
## Аргументы командной строки

| Аргумент | Тип | Описание |
| :--- | :--- | :--- |
| `source` | Позиционный | Путь к исходному файлу или директории. |
| `output` | Позиционный | Путь к выходному архиву (должен оканчиваться на `.zst` или `.bz2`) или целевая директория для распаковки. |
| `-x`, `--extract`| Необязательный | Флаг для включения режима извлечения. Если не указан, используется режим сжатия. |
| `-h`, `--help` | Необязательный | Показать справочное сообщение и выйти. |

## Примеры использования

### 1. Архивация (сжатие)

Чтобы сжать директорию или файл, укажите исходный путь и желаемое имя выходного архива.

**Создание тестовых файлов**

<img width="1497" height="734" alt="5a68f1c858da308ec428bb12e9f121b6" src="https://github.com/user-attachments/assets/03bc0731-e2d5-474d-8c9e-535a0b43a3cc" />

**Сжатие директории с использованием zstd:**

```bash
python archiver.py test_data archive.tar.zst
```

<img width="2007" height="1080" alt="image" src="https://github.com/user-attachments/assets/5f9a684e-4f8a-4a05-b143-1cf1d262fe96" />

**Распаковка файла**

```bash
python archiver.py -x archive.tar.zst out_folder
```

<img width="1857" height="1245" alt="image" src="https://github.com/user-attachments/assets/64791f53-7380-4580-8318-b4147973b1bb" />

**Автоматическое определение (сжатие в формат zst)**

```bash
python archiver.py test_data output.tar.zst
```

<img width="1860" height="1308" alt="image" src="https://github.com/user-attachments/assets/6e31802f-6df4-4bab-b262-e316ad58b7d0" />

**Автоматическое определение (сжатие в формат bz2)**

```bash
python archiver.py test_data output.tar.zst
```

<img width="1842" height="1392" alt="image" src="https://github.com/user-attachments/assets/a1094abb-a8a4-42d3-b01b-a0c08f79efe1" />

**Автоматическое определение (распаковка zst)**

```bash
python archiver.py -x output.tar.zst out_folder
```

<img width="1821" height="1404" alt="image" src="https://github.com/user-attachments/assets/feacc811-42b8-4f15-864d-598c54144e10" />

**Автоматическое определение (распаковка bz2)**

```bash
python archiver.py -x output.tar.bz2 out_folder
```

<img width="1844" height="1392" alt="image" src="https://github.com/user-attachments/assets/bcfdf1c5-02af-44ec-be19-cb3a339a1d6a" />

**Справочная информация argparse**

```bash
python archiver.py -h
```

<img width="840" height="345" alt="image" src="https://github.com/user-attachments/assets/a4033093-af35-4800-9f8e-aa47ec343513" />
