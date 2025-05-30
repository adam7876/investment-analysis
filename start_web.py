#!/usr/bin/env python3
"""
美股投資分析系統 Web 啟動器
整合AI增強功能的Web界面
"""

import os
import sys
import socket
from loguru import logger
import flask

def check_port(port):
    """檢查端口是否可用"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def find_available_port():
    """尋找可用端口"""
    ports = [5000, 8080, 8083, 8000, 3000, 9000]
    for port in ports:
        if check_port(port):
            return port
    return 8888  # 備用端口

def main():
    """啟動Web服務"""
    logger.info("🚀 正在啟動美股投資分析系統 Web 介面...")
    
    # 檢查Flask版本
    try:
        logger.info(f"✅ Flask 版本: {flask.__version__}")
    except:
        logger.info("✅ Flask 已安裝")
    
    # 設置環境變量
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    # 尋找可用端口
    port = find_available_port()
    
    if port != 5000:
        if port == 8080:
            logger.warning("⚠️ 端口 5000 被占用（可能是 AirPlay Receiver）")
        elif port == 8083:
            logger.warning("⚠️ 端口 5000 被占用（可能是 AirPlay Receiver）")
            logger.warning("⚠️ 端口 8080 也被占用")
        logger.info(f"🔄 改用端口 {port}")
    
    # 導入並啟動應用
    try:
        from app import app
        
        logger.info("🌐 Web 介面啟動中...")
        logger.info(f"📱 請在瀏覽器中打開: http://localhost:{port}")
        logger.info("⏹️  按 Ctrl+C 停止服務")
        
        # 啟動Flask應用
        app.run(
            host='0.0.0.0',
            port=port,
            debug=True,
            use_reloader=False  # 避免重複啟動
        )
        
    except ImportError as e:
        logger.error(f"❌ 無法導入應用: {e}")
        logger.info("🔧 正在檢查依賴...")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ 啟動失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 