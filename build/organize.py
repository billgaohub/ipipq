#!/usr/bin/env python3
"""
AI File Auto Organizer - 极简版
自动整理下载文件夹

用法:
    python organize.py                    # 整理默认 Downloads 文件夹
    python organize.py /path/to/folder    # 整理指定文件夹
    python organize.py --dry-run          # 试运行（不实际移动文件）
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ─── 文件类型映射 ───
FILE_TYPES = {
    # 图片
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".raw", ".psd", ".ai", ".sketch"],
    # 文档
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".pages", ".epub", ".mobi", ".azw3"],
    # 表格/演示
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".numbers", ".ppt", ".pptx", ".key"],
    # 视频
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v", ".mpg", ".mpeg"],
    # 音频
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a", ".ogg", ".wma", ".aiff"],
    # 压缩包
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".dmg", ".pkg", ".deb"],
    # 代码
    "Code": [".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".scss", ".java", ".cpp", ".c", ".h", ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".sql", ".json", ".xml", ".yaml", ".yml", ".toml"],
    # 可执行文件
    "Executables": [".exe", ".msi", ".app", ".bat", ".sh", ".command"],
    # 字体
    "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    # 数据
    "Data": [".db", ".sqlite", ".sqlite3", ".mdb", ".accdb"],
}

# 反向映射：扩展名 -> 类别
EXT_TO_CATEGORY = {}
for category, exts in FILE_TYPES.items():
    for ext in exts:
        EXT_TO_CATEGORY[ext.lower()] = category

# 日期格式文件夹
DATE_FORMAT = "%Y-%m"


class FileOrganizer:
    """文件整理器"""

    def __init__(self, source_dir: str = None, dry_run: bool = False):
        # 默认使用 Downloads 文件夹
        if source_dir is None:
            source_dir = str(Path.home() / "Downloads")

        self.source_dir = Path(source_dir).expanduser().resolve()
        self.dry_run = dry_run
        self.stats = defaultdict(int)
        self.log = []

    def get_category(self, file_path: Path) -> str:
        """根据扩展名获取文件类别"""
        ext = file_path.suffix.lower()
        return EXT_TO_CATEGORY.get(ext, "Others")

    def generate_new_name(self, file_path: Path, target_dir: Path) -> Path:
        """生成新的文件名（处理重名）"""
        name = file_path.stem
        ext = file_path.suffix

        # 清理文件名（移除常见乱码字符）
        name = self._clean_filename(name)

        new_path = target_dir / f"{name}{ext}"

        # 处理重名
        counter = 1
        while new_path.exists():
            new_path = target_dir / f"{name}_{counter:03d}{ext}"
            counter += 1

        return new_path

    def _clean_filename(self, name: str) -> str:
        """清理文件名"""
        # 移除或替换常见乱码字符
        replacements = {
            "【": "[",
            "】": "]",
            "（": "(",
            "）": ")",
            " ": "_",
            "　": "_",
            "—": "-",
            "——": "-",
        }

        for old, new in replacements.items():
            name = name.replace(old, new)

        # 移除连续的下划线
        while "__" in name:
            name = name.replace("__", "_")

        # 截断过长的文件名（保留前50个字符）
        if len(name) > 50:
            name = name[:50]

        return name.strip("_")

    def organize(self) -> dict:
        """执行整理"""
        if not self.source_dir.exists():
            print(f"❌ 源文件夹不存在: {self.source_dir}")
            return {"error": "Source directory not found"}

        print(f"📁 整理文件夹: {self.source_dir}")
        print(f"{'[试运行] ' if self.dry_run else ''}开始整理...\n")

        # 获取所有文件（不包括隐藏文件和文件夹）
        files = [f for f in self.source_dir.iterdir() if f.is_file() and not f.name.startswith(".")]

        if not files:
            print("ℹ️ 没有找到需要整理的文件")
            return {"total": 0, "organized": 0}

        print(f"发现 {len(files)} 个文件\n")

        for file_path in files:
            # 获取类别
            category = self.get_category(file_path)

            # 获取文件修改时间
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            date_folder = mtime.strftime(DATE_FORMAT)

            # 构建目标路径: Downloads/Images/2024-01/
            target_dir = self.source_dir / category / date_folder

            if not self.dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)

            # 生成新文件名
            new_path = self.generate_new_name(file_path, target_dir)

            # 移动文件
            if self.dry_run:
                print(f"[试运行] {file_path.name}")
                print(f"         → {category}/{date_folder}/{new_path.name}")
            else:
                try:
                    shutil.move(str(file_path), str(new_path))
                    print(f"✅ {file_path.name}")
                    print(f"   → {category}/{date_folder}/{new_path.name}")
                except Exception as e:
                    print(f"❌ 移动失败: {file_path.name} - {e}")
                    continue

            self.stats[category] += 1
            self.log.append({
                "original": str(file_path),
                "category": category,
                "date": date_folder,
                "new_name": new_path.name,
            })

        # 打印统计
        print(f"\n{'='*50}")
        print("整理完成!")
        print(f"{'='*50}")
        print(f"总计: {len(files)} 个文件")
        print("\n分类统计:")
        for category, count in sorted(self.stats.items(), key=lambda x: -x[1]):
            print(f"  {category}: {count} 个文件")

        return {
            "total": len(files),
            "organized": len(self.log),
            "stats": dict(self.stats),
        }


def main():
    """主函数"""
    # 解析参数
    args = sys.argv[1:]
    source_dir = None
    dry_run = False

    for arg in args:
        if arg == "--dry-run" or arg == "-n":
            dry_run = True
        elif arg.startswith("-"):
            print(f"未知参数: {arg}")
            print(__doc__)
            sys.exit(1)
        else:
            source_dir = arg

    # 创建整理器并执行
    organizer = FileOrganizer(source_dir=source_dir, dry_run=dry_run)
    result = organizer.organize()

    # 返回码
    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
