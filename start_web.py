#!/usr/bin/env python3
"""
美股投資分析系統 - Web 啟動腳本
自動檢測可用端口並啟動 Flask 應用
"""

import os
import sys
import socket
import subprocess
import time
from loguru import logger
import flask

def check_port_available(port):
    """檢查端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def find_available_port():
    """尋找可用端口"""
    # 嘗試的端口列表
    ports_to_try = [5000, 8080, 8081, 8082, 8083, 8084, 8085, 3000, 3001, 9000, 9001]
    
    for port in ports_to_try:
        if check_port_available(port):
            return port
    
    # 如果所有預設端口都被占用，隨機選擇一個
    for port in range(8090, 8200):
        if check_port_available(port):
            return port
    
    return None

def main():
    logger.info("🚀 正在啟動美股投資分析系統 Web 介面...")
    
    # 檢查 Flask 版本
    try:
        logger.info(f"✅ Flask 版本: {flask.__version__}")
    except AttributeError:
        logger.info("✅ Flask 已安裝")
    
    # 尋找可用端口
    port = find_available_port()
    
    if port is None:
        logger.error("❌ 無法找到可用端口，請手動停止其他服務")
        sys.exit(1)
    
    if port != 5000:
        logger.warning(f"⚠️ 端口 5000 被占用（可能是 AirPlay Receiver）")
        if port != 8080:
            logger.warning(f"⚠️ 端口 8080 也被占用")
        logger.info(f"🔄 改用端口 {port}")
    
    # 設置環境變數
    os.environ['PORT'] = str(port)
    os.environ['FLASK_ENV'] = 'development'
    
    # 等待一下確保端口釋放
    time.sleep(1)
    
    logger.info("🌐 Web 介面啟動中...")
    logger.info(f"📱 請在瀏覽器中打開: http://localhost:{port}")
    logger.info("⏹️  按 Ctrl+C 停止服務")
    
    try:
        # 啟動 Flask 應用
        from app import app
        app.run(
            debug=True,
            host='0.0.0.0',
            port=port,
            use_reloader=False  # 避免重複啟動
        )
    except KeyboardInterrupt:
        logger.info("👋 服務已停止")
    except Exception as e:
        logger.error(f"❌ 啟動失敗: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 