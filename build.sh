#!/bin/bash
# 打包 IPIPQ 工具

VERSION="1.0.0"
BUILD_DIR="./build"

echo "📦 打包 AI File Auto Organizer v${VERSION}"

# 创建构建目录
mkdir -p ${BUILD_DIR}

# 复制文件
cp organize.py ${BUILD_DIR}/
cp README_IPIPQ.md ${BUILD_DIR}/README.md

# 创建 ZIP 包
cd ${BUILD_DIR}
zip -r "../ipipq-v${VERSION}.zip" .
cd ..

echo "✅ 打包完成: ipipq-v${VERSION}.zip"
echo ""
echo "文件内容:"
unzip -l "ipipq-v${VERSION}.zip"
