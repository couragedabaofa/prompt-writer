#!/bin/bash

echo "========================================"
echo "   AI提示词管理工具"
echo "========================================"
echo ""
echo "正在启动应用..."
echo ""

if ! command -v python3 &> /dev/null; then
    echo "错误：未检测到Python3，请先安装Python 3.7或更高版本"
    echo "安装方法：brew install python3"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "首次运行，正在创建虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "错误：创建虚拟环境失败"
        exit 1
    fi
fi

source venv/bin/activate

echo "正在检查依赖..."
pip install -r requirements.txt --quiet

echo ""
echo "应用启动成功！"
echo "请在浏览器中打开：http://localhost:8080"
echo ""
echo "按Ctrl+C停止应用"
echo "========================================"
echo ""

python app.py
