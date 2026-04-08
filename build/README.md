# AI File Auto Organizer

自动整理你的下载文件夹。

## 功能

- ✅ **自动识别文件类型** - 图片、文档、表格、视频、音频、压缩包、代码等
- ✅ **自动分类归档** - 按类型和日期自动分文件夹
- ✅ **自动命名优化** - 清理乱码字符，处理重名文件

## 使用方法

### 1. 直接运行（整理 Downloads 文件夹）

```bash
python organize.py
```

### 2. 整理指定文件夹

```bash
python organize.py /path/to/folder
```

### 3. 试运行（查看效果，不实际移动文件）

```bash
python organize.py --dry-run
```

## 整理效果

**整理前：**
```
Downloads/
├── 合同.pdf
├── IMG_1234.jpg
├── 数据.xlsx
├── script.py
├── 视频.mp4
└── ...（一堆杂乱文件）
```

**整理后：**
```
Downloads/
├── Documents/
│   └── 2024-01/
│       └── 合同.pdf
├── Images/
│   └── 2024-01/
│       └── IMG_1234.jpg
├── Spreadsheets/
│   └── 2024-01/
│       └── 数据.xlsx
├── Code/
│   └── 2024-01/
│       └── script.py
├── Videos/
│   └── 2024-01/
│       └── 视频.mp4
└── ...（井井有条）
```

## 支持格式

| 类别 | 格式 |
|------|------|
| Images | jpg, png, gif, psd, ai, sketch... |
| Documents | pdf, doc, docx, txt, pages, epub... |
| Spreadsheets | xls, xlsx, csv, ppt, pptx... |
| Videos | mp4, mov, avi, mkv... |
| Audio | mp3, wav, aac, flac... |
| Archives | zip, rar, 7z, tar, dmg... |
| Code | py, js, html, css, java, go, rs... |
| Executables | exe, app, sh... |
| Fonts | ttf, otf, woff... |

## 系统要求

- Python 3.7+
- macOS / Linux / Windows

## 许可证

MIT License
