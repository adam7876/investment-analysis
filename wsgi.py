#!/usr/bin/env python3
"""
WSGI入口點 - Railway部署用
"""

import os
import sys

# 添加當前目錄到Python路徑
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import app
    
    if __name__ == "__main__":
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
        
except ImportError as e:
    print(f"導入錯誤: {e}")
    sys.exit(1)
except Exception as e:
    print(f"啟動錯誤: {e}")
    sys.exit(1) 