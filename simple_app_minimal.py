#!/usr/bin/env python3
"""
美股投資分析系統 - 最小版本
專注於基礎功能，確保Railway部署成功
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json
from loguru import logger

app = Flask(__name__)

@app.route('/')
def index():
    """主頁面"""
    return """
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🤖 AI增強美股投資分析系統</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .main-container { background: rgba(255, 255, 255, 0.95); border-radius: 20px; margin: 20px auto; padding: 30px; max-width: 800px; }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="main-container">
                <div class="text-center mb-5">
                    <h1 class="text-primary">🤖 AI增強美股投資分析系統</h1>
                    <p class="lead text-muted">系統部署成功！正在準備完整功能...</p>
                    <div class="mt-3">
                        <span class="badge bg-success">✅ 系統運行正常</span>
                        <span class="badge bg-info ms-2">🚀 Railway部署成功</span>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-12">
                        <div class="card">
                            <div class="card-body text-center">
                                <h5 class="card-title">🎉 部署成功！</h5>
                                <p class="card-text">
                                    美股投資分析系統已成功部署到Railway平台。<br>
                                    完整的AI功能正在準備中，包括：
                                </p>
                                <ul class="list-unstyled">
                                    <li>🔮 LSTM深度學習股價預測</li>
                                    <li>🔬 機器學習智能選股</li>
                                    <li>💡 AI投資建議生成</li>
                                    <li>📈 三層聯動分析</li>
                                </ul>
                                <button class="btn btn-primary" onclick="testHealth()">測試系統健康</button>
                                <div id="health-result" class="mt-3"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            function testHealth() {
                fetch('/health')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('health-result').innerHTML = 
                            '<div class="alert alert-success">✅ 系統健康檢查通過！<br>版本: ' + data.version + '</div>';
                    })
                    .catch(error => {
                        document.getElementById('health-result').innerHTML = 
                            '<div class="alert alert-danger">❌ 健康檢查失敗</div>';
                    });
            }
        </script>
    </body>
    </html>
    """

@app.route('/health')
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI增強美股投資分析系統運行正常',
        'version': '3.0.0-minimal',
        'stage': 'Railway Deployment Success',
        'features': ['基礎系統', '健康檢查', 'Railway部署'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/test')
def api_test():
    """API測試端點"""
    return jsonify({
        'success': True,
        'message': 'API運行正常',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"🚀 啟動最小版本系統，端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 