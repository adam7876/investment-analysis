#!/usr/bin/env python3
"""
最小化的Flask應用 - 用於測試Railway部署
"""

import os
from flask import Flask, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# 簡單的HTML模板
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>四層聯動美股投資分析系統</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; color: #2c3e50; }
        .status { background: #e8f5e8; padding: 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">🚀 四層聯動美股投資分析系統</h1>
        <div class="status">
            <h2>✅ 系統運行正常</h2>
            <p>部署成功！系統已在Railway上運行。</p>
            <p>時間：{{ timestamp }}</p>
        </div>
        <div style="margin-top: 30px;">
            <h3>🎯 系統功能</h3>
            <ul>
                <li>第一層：市場總觀趨勢分析</li>
                <li>第二層：產業與催化劑分析</li>
                <li>第三層：精選操作名單</li>
                <li>第四層：選擇權策略建議</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """主頁面"""
    return render_template_string(INDEX_TEMPLATE, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/health')
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'healthy',
        'message': '四層聯動美股投資分析系統運行正常',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/test')
def api_test():
    """API測試端點"""
    return jsonify({
        'success': True,
        'message': 'API運行正常',
        'data': {
            'system': '四層聯動美股投資分析系統',
            'status': 'operational',
            'timestamp': datetime.now().isoformat()
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 