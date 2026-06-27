# IPIPQ - 文件自动整理工具

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)

> 按类型和日期自动整理文件夹，支持一键撤销

IPIPQ 自动识别 50+ 种文件格式，按类型和修改日期归档，整理后可一键撤销。

---

## 功能

| 功能 | 描述 |
|------|------|
| **按类型归档** | 识别图片、文档、表格、视频、音频、代码、压缩包等 50+ 种格式 |
| **按日期归档** | 每个分类下自动创建"年-月"子目录（如 `Images/2026-05/`） |
| **文件名清理** | 替换全角字符、清理多余下划线、截断过长文件名 |
| **重名处理** | 自动追加数字后缀，防止覆盖 |
| **预览模式** | `--dry-run` 提前查看整理结果，不实际移动文件 |
| **一键撤销** | `--undo` 恢复上一次整理，`--undo --all` 恢复所有 |
| **本地运行** | 所有操作在本地完成，文件不上传 |

---

## 安装

### 下载发行版

```bash
curl -O https://ipipq.com/ipipq-v1.0.1.zip
unzip ipipq-v1.0.1.zip
cd ipipq
```

### 从源码安装

```bash
git clone https://github.com/billgaohub/ipipq.git
cd ipipq
```

---

## 使用方法

```bash
# 整理默认 Downloads 文件夹
python3 organize.py

# 整理指定目录
python3 organize.py /path/to/folder

# 预览模式（不实际移动）
python3 organize.py --dry-run

# 撤销上一次整理
python3 organize.py --undo

# 撤销所有整理记录
python3 organize.py --undo --all
```

---

## 整理效果

### 整理前

```
Downloads/
├── 合同.pdf
├── IMG_1234.jpg
├── 数据.xlsx
├── script.py
├── 视频.mp4
└── ...（杂乱文件）
```

### 整理后

```
Downloads/
├── Documents/2026-05/合同.pdf
├── Images/2026-05/IMG_1234.jpg
├── Spreadsheets/2026-05/数据.xlsx
├── Code/2026-05/script.py
├── Videos/2026-05/视频.mp4
└── .ipipq/history.jsonl  ← 操作日志（可用于撤销）
```

---

## 文件分类

| 类型 | 目标文件夹 | 扩展名 |
|------|-----------|--------|
| 文档 | `Documents/` | `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.pages`, `.epub` |
| 图片 | `Images/` | `.jpg`, `.png`, `.gif`, `.svg`, `.webp`, `.psd`, `.raw` |
| 表格 | `Spreadsheets/` | `.xls`, `.xlsx`, `.csv`, `.ppt`, `.pptx` |
| 视频 | `Videos/` | `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm` |
| 音频 | `Audio/` | `.mp3`, `.wav`, `.flac`, `.m4a`, `.ogg` |
| 压缩包 | `Archives/` | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.dmg` |
| 代码 | `Code/` | `.py`, `.js`, `.ts`, `.html`, `.css`, `.java`, `.go`, `.rs` |
| 可执行 | `Executables/` | `.exe`, `.msi`, `.app`, `.bat`, `.sh` |
| 字体 | `Fonts/` | `.ttf`, `.otf`, `.woff`, `.woff2` |
| 数据 | `Data/` | `.db`, `.sqlite`, `.sqlite3` |
| 其他 | `Others/` | 未匹配的文件 |

---

## 系统要求

- Python 3.7+
- macOS / Linux / Windows

---

## 许可证

MIT License

---

## 链接

- 官网: https://ipipq.com
- GitHub: https://github.com/billgaohub/ipipq

---

Made with ❤️ by **IPIPQ**
