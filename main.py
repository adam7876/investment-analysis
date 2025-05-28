#!/usr/bin/env python3
"""
四層聯動美股投資分析系統 - Railway部署啟動文件
"""

import os
import sys

# 設置環境
os.environ.setdefault('FLASK_ENV', 'production')

# 導入並啟動完整的四層分析應用
if __name__ == "__main__":
    try:
        from app import app  # 使用完整的app.py而不是app_stage1.py
        port = int(os.environ.get('PORT', 5000))
        print(f"🚀 啟動四層聯動美股投資分析系統（完整版），端口: {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"啟動失敗: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 