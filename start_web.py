#!/usr/bin/env python3
"""
美股投資分析系統 - Web介面啟動腳本
"""

import os
import sys
from loguru import logger

def main():
    """啟動Web應用程式"""
    logger.info("🚀 正在啟動美股投資分析系統 Web 介面...")
    
    # 檢查是否在正確的目錄
    if not os.path.exists('app.py'):
        logger.error("❌ 找不到 app.py，請確認您在正確的目錄中")
        sys.exit(1)
    
    # 檢查是否安裝了Flask
    try:
        import flask
        logger.info(f"✅ Flask 版本: {flask.__version__}")
    except ImportError:
        logger.error("❌ Flask 未安裝，請運行: pip3 install Flask")
        sys.exit(1)
    
    # 檢查端口5000是否被占用，如果被占用則使用8080
    import socket
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    port = 5000
    if is_port_in_use(port):
        logger.warning(f"⚠️ 端口 {port} 被占用（可能是 AirPlay Receiver）")
        port = 8080
        logger.info(f"🔄 改用端口 {port}")
    
    # 設定環境變數
    os.environ['PORT'] = str(port)
    
    # 啟動應用程式
    try:
        from app import app
        logger.info("🌐 Web 介面啟動中...")
        logger.info(f"📱 請在瀏覽器中打開: http://localhost:{port}")
        logger.info("⏹️  按 Ctrl+C 停止服務")
        
        app.run(debug=True, host='0.0.0.0', port=port)
        
    except KeyboardInterrupt:
        logger.info("👋 Web 介面已停止")
    except Exception as e:
        logger.error(f"❌ 啟動失敗: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 