#!/usr/bin/env python3
"""
IPIPQ - 文件自动整理工具
按类型和日期整理文件夹，支持撤销

用法:
    python organize.py                    # 整理默认 Downloads 文件夹
    python organize.py /path/to/folder    # 整理指定文件夹
    python organize.py --dry-run          # 试运行（不实际移动文件）
    python organize.py --undo             # 撤销上一次整理
    python organize.py --undo --all       # 撤销所有整理记录
"""

import json
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ─── 文件类型映射 ───
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".raw", ".psd", ".ai", ".sketch"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".pages", ".epub", ".mobi", ".azw3"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".numbers", ".ppt", ".pptx", ".key"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v", ".mpg", ".mpeg"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a", ".ogg", ".wma", ".aiff"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".dmg", ".pkg", ".deb"],
    "Code": [".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".scss", ".java", ".cpp", ".c", ".h", ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".sql", ".json", ".xml", ".yaml", ".yml", ".toml"],
    "Executables": [".exe", ".msi", ".app", ".bat", ".sh", ".command"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    "Data": [".db", ".sqlite", ".sqlite3", ".mdb", ".accdb"],
}

EXT_TO_CATEGORY = {}
for category, exts in FILE_TYPES.items():
    for ext in exts:
        EXT_TO_CATEGORY[ext.lower()] = category

DATE_FORMAT = "%Y-%m"
LOG_DIR_NAME = ".ipipq"
LOG_FILE_NAME = "history.jsonl"


class FileOrganizer:
    """文件整理器"""

    def __init__(self, source_dir: str = None, dry_run: bool = False):
        if source_dir is None:
            source_dir = str(Path.home() / "Downloads")
        self.source_dir = Path(source_dir).expanduser().resolve()
        self.dry_run = dry_run
        self.stats = defaultdict(int)
        self.moves: list[dict] = []

    def get_category(self, file_path: Path) -> str:
        ext = file_path.suffix.lower()
        return EXT_TO_CATEGORY.get(ext, "Others")

    def generate_new_name(self, file_path: Path, target_dir: Path) -> Path:
        name = file_path.stem
        ext = file_path.suffix
        name = self._clean_filename(name)
        new_path = target_dir / f"{name}{ext}"
        counter = 1
        while new_path.exists():
            new_path = target_dir / f"{name}_{counter:03d}{ext}"
            counter += 1
        return new_path

    def _clean_filename(self, name: str) -> str:
        replacements = {
            "【": "[", "】": "]",
            "（": "(", "）": ")",
            " ": "_", "　": "_",
            "—": "-", "——": "-",
        }
        for old, new in replacements.items():
            name = name.replace(old, new)
        while "__" in name:
            name = name.replace("__", "_")
        if len(name) > 50:
            name = name[:50]
        return name.strip("_")

    def _log_path(self) -> Path:
        log_dir = self.source_dir / LOG_DIR_NAME
        return log_dir / LOG_FILE_NAME

    def _append_log(self, session_moves: list[dict]) -> None:
        log_path = self._log_path()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.now().isoformat(),
            "source_dir": str(self.source_dir),
            "moves": session_moves,
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _read_log(self) -> list[dict]:
        log_path = self._log_path()
        if not log_path.exists():
            return []
        entries = []
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        return entries

    def undo(self, undo_all: bool = False) -> int:
        """撤销整理操作，返回成功恢复的文件数"""
        entries = self._read_log()
        if not entries:
            print("没有找到整理记录，无需撤销。")
            return 0

        target = entries if undo_all else [entries[-1]]
        restored = 0

        for entry in reversed(target):
            ts = entry.get("timestamp", "未知时间")
            moves = entry.get("moves", [])
            print(f"撤销 {ts} 的整理（{len(moves)} 个文件）...\n")

            for move in reversed(moves):
                src = Path(move["dest"])
                dst = Path(move["source"])
                if src.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                    print(f"  恢复: {src.name} → {dst}")
                    restored += 1
                else:
                    print(f"  跳过（文件不存在）: {src}")

            print()

        # 重写日志，移除已撤销的条目
        if not undo_all:
            remaining = entries[:-1]
        else:
            remaining = []

        log_path = self._log_path()
        with open(log_path, "w", encoding="utf-8") as f:
            for entry in remaining:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        print(f"共恢复 {restored} 个文件。")
        return restored

    def organize(self) -> dict:
        if not self.source_dir.exists():
            print(f"源文件夹不存在: {self.source_dir}")
            return {"error": "Source directory not found"}

        print(f"整理文件夹: {self.source_dir}")
        if self.dry_run:
            print("[试运行] 不会实际移动文件\n")

        files = [f for f in self.source_dir.iterdir()
                 if f.is_file() and not f.name.startswith(".")]

        if not files:
            print("没有找到需要整理的文件")
            return {"total": 0, "organized": 0}

        print(f"发现 {len(files)} 个文件\n")

        for file_path in files:
            category = self.get_category(file_path)
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            date_folder = mtime.strftime(DATE_FORMAT)
            target_dir = self.source_dir / category / date_folder

            if not self.dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)

            new_path = self.generate_new_name(file_path, target_dir)

            if self.dry_run:
                print(f"  {file_path.name}")
                print(f"  → {category}/{date_folder}/{new_path.name}")
            else:
                try:
                    shutil.move(str(file_path), str(new_path))
                    print(f"  {file_path.name} → {category}/{date_folder}/{new_path.name}")
                except Exception as e:
                    print(f"  失败: {file_path.name} - {e}")
                    continue

            self.stats[category] += 1
            self.moves.append({
                "source": str(file_path),
                "dest": str(new_path),
                "category": category,
                "date": date_folder,
            })

        # 保存日志（非试运行时）
        if not self.dry_run and self.moves:
            self._append_log(self.moves)

        print(f"\n{'='*50}")
        print(f"整理完成: {len(self.moves)}/{len(files)} 个文件")
        print(f"{'='*50}")
        for category, count in sorted(self.stats.items(), key=lambda x: -x[1]):
            print(f"  {category}: {count}")

        if not self.dry_run and self.moves:
            print(f"\n如需撤销: python organize.py --undo")

        return {
            "total": len(files),
            "organized": len(self.moves),
            "stats": dict(self.stats),
        }


def main():
    args = sys.argv[1:]
    source_dir = None
    dry_run = False
    undo = False
    undo_all = False

    for arg in args:
        if arg in ("--dry-run", "-n"):
            dry_run = True
        elif arg == "--undo":
            undo = True
        elif arg == "--all":
            undo_all = True
        elif arg in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
        elif arg.startswith("-"):
            print(f"未知参数: {arg}")
            print(__doc__)
            sys.exit(1)
        else:
            source_dir = arg

    organizer = FileOrganizer(source_dir=source_dir, dry_run=dry_run)

    if undo:
        organizer.undo(undo_all=undo_all)
        sys.exit(0)

    result = organizer.organize()
    sys.exit(1 if "error" in result else 0)


if __name__ == "__main__":
    main()
