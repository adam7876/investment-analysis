#!/usr/bin/env python3
"""
四層聯動美股投資分析系統 - Railway部署啟動文件
"""

import os
import sys
import traceback

# 設置環境
os.environ.setdefault('FLASK_ENV', 'production')

def main():
    """主啟動函數"""
    try:
        print("🚀 開始啟動四層聯動美股投資分析系統...")
        
        # 檢查Python版本
        print(f"🐍 Python版本: {sys.version}")
        
        # 檢查關鍵依賴
        try:
            import flask
            print(f"✅ Flask版本: {flask.__version__}")
        except ImportError as e:
            print(f"❌ Flask導入失敗: {e}")
            sys.exit(1)
        
        # 嘗試導入Railway專用應用
        try:
            print("📦 正在導入Railway專用應用模組...")
            from app_railway import app
            print("✅ Railway專用應用模組導入成功")
        except ImportError as e:
            print(f"❌ Railway專用應用模組導入失敗: {e}")
            print("🔄 嘗試使用完整版本...")
            try:
                from app import app
                print("✅ 完整版應用模組導入成功")
            except ImportError as e2:
                print(f"❌ 完整版應用模組也導入失敗: {e2}")
                print("🔄 嘗試使用階段1版本...")
                try:
                    from app_stage1 import app
                    print("✅ 階段1應用模組導入成功")
                except ImportError as e3:
                    print(f"❌ 所有應用模組都導入失敗: {e3}")
                    sys.exit(1)
        
        # 獲取端口
        port = int(os.environ.get('PORT', 5000))
        print(f"🌐 準備在端口 {port} 啟動服務...")
        
        # 啟動應用
        print("🚀 啟動Flask應用...")
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")
        print("📋 詳細錯誤信息:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 