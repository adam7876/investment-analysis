#!/usr/bin/env python3
"""
階段1升級版 - 添加基礎數據獲取功能
"""

import os
import requests
from flask import Flask, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# 升級版HTML模板
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>四層聯動美股投資分析系統 - 階段1</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { text-align: center; color: #2c3e50; margin-bottom: 30px; }
        .status { background: #e8f5e8; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .feature-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .api-test { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .btn:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">🚀 四層聯動美股投資分析系統</h1>
        <div class="status">
            <h2>✅ 階段1部署成功</h2>
            <p>系統已在Railway上運行，基礎功能已啟用。</p>
            <p>時間：{{ timestamp }}</p>
        </div>
        
        <div class="feature-grid">
            <div class="feature-card">
                <h3>🎯 四層分析架構</h3>
                <ul>
                    <li><strong>第一層</strong>：市場總觀趨勢分析</li>
                    <li><strong>第二層</strong>：產業與催化劑分析</li>
                    <li><strong>第三層</strong>：精選操作名單</li>
                    <li><strong>第四層</strong>：選擇權策略建議</li>
                </ul>
            </div>
            
            <div class="feature-card">
                <h3>📊 當前功能狀態</h3>
                <ul>
                    <li>✅ 基礎Web框架</li>
                    <li>✅ 健康檢查API</li>
                    <li>✅ 數據獲取模組</li>
                    <li>🔄 市場數據API（開發中）</li>
                </ul>
            </div>
            
            <div class="feature-card">
                <h3>🔧 API測試</h3>
                <div class="api-test">
                    <button class="btn" onclick="testAPI()">測試市場數據API</button>
                    <div id="api-result" style="margin-top: 10px;"></div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        async function testAPI() {
            const resultDiv = document.getElementById('api-result');
            resultDiv.innerHTML = '⏳ 測試中...';
            
            try {
                const response = await fetch('/api/market-data');
                const data = await response.json();
                resultDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            } catch (error) {
                resultDiv.innerHTML = `❌ 錯誤: ${error.message}`;
            }
        }
    </script>
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
        'version': '1.1.0',
        'stage': 'Stage 1 - Basic Data Access'
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
            'stage': 'Stage 1',
            'timestamp': datetime.now().isoformat()
        }
    })

@app.route('/api/market-data')
def market_data():
    """基礎市場數據API"""
    try:
        # 簡單的市場數據模擬
        market_data = {
            'market_overview': {
                'sentiment': 'Neutral',
                'fear_greed_index': 50,
                'trend': 'Sideways'
            },
            'sectors': [
                {'name': 'Technology', 'performance': '+1.2%'},
                {'name': 'Healthcare', 'performance': '+0.8%'},
                {'name': 'Energy', 'performance': '-0.5%'}
            ],
            'watchlist': [
                {'symbol': 'AAPL', 'price': 185.50, 'change': '+1.2%'},
                {'symbol': 'NVDA', 'price': 425.30, 'change': '+2.1%'},
                {'symbol': 'MSFT', 'price': 340.80, 'change': '+0.9%'}
            ],
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': market_data,
            'message': '市場數據獲取成功（模擬數據）'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '市場數據獲取失敗'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 