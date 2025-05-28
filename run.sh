#!/bin/bash

# 美股投資分析系統 - 一鍵啟動腳本

echo "🚀 美股投資分析系統"
echo "===================="
echo ""

# 檢查Python是否安裝
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安裝，請先安裝Python3"
    exit 1
fi

# 檢查是否在正確目錄
if [ ! -f "app.py" ]; then
    echo "❌ 找不到app.py，請確認您在正確的目錄中"
    exit 1
fi

# 檢查並安裝依賴
echo "📦 檢查依賴..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask未安裝，正在安裝..."
    pip3 install Flask==3.0.0
fi

# 檢查端口是否被占用
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  端口5000已被占用"
    echo "請選擇操作："
    echo "1) 終止占用進程並繼續"
    echo "2) 退出"
    read -p "請輸入選擇 (1/2): " choice
    
    if [ "$choice" = "1" ]; then
        echo "🔄 終止占用進程..."
        lsof -ti:5000 | xargs kill -9 2>/dev/null
        sleep 2
    else
        echo "👋 退出"
        exit 0
    fi
fi

# 啟動Web介面
echo ""
echo "🌐 啟動Web介面..."
echo "📱 請在瀏覽器中打開: http://localhost:5000"
echo "⏹️  按 Ctrl+C 停止服務"
echo ""

# 啟動應用程式
python3 start_web.py 