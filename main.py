#!/usr/bin/env python3
"""
簡化的啟動文件 - Railway部署用（階段1升級）
"""

import os
import sys

# 設置環境
os.environ.setdefault('FLASK_ENV', 'production')

# 導入並啟動應用
if __name__ == "__main__":
    try:
        from app_stage1 import app
        port = int(os.environ.get('PORT', 5000))
        print(f"🚀 啟動四層聯動美股投資分析系統（階段1），端口: {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"啟動失敗: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 