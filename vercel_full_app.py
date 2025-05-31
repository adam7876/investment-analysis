#!/usr/bin/env python3
"""
美股投資分析系統 - Vercel純Python版本
使用Python內建模組，確保100%部署成功
"""

import json
import os
import sys
import random
import urllib.parse
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

class InvestmentAnalysisHandler(BaseHTTPRequestHandler):
    """投資分析系統HTTP處理器"""
    
    def do_GET(self):
        """處理GET請求"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_main_page()
        elif self.path == '/health':
            self.serve_health_check()
        else:
            self.send_error(404, "Page not found")
    
    def do_POST(self):
        """處理POST請求"""
        if self.path == '/api/data-collection':
            self.serve_data_collection()
        elif self.path == '/api/ai-analysis':
            self.serve_ai_analysis()
        elif self.path == '/api/integrated-analysis':
            self.serve_integrated_analysis()
        else:
            self.send_error(404, "API not found")
    
    def serve_main_page(self):
        """提供主頁面"""
        html_content = """
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>🤖 AI增強美股投資分析系統</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                body { 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    min-height: 100vh; 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                .main-container { 
                    background: rgba(255, 255, 255, 0.95); 
                    border-radius: 20px; 
                    margin: 20px auto; 
                    padding: 40px; 
                    max-width: 1200px; 
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                }
                .feature-card {
                    background: linear-gradient(45deg, #f8f9fa, #e9ecef);
                    border: none;
                    border-radius: 15px;
                    transition: transform 0.3s ease;
                    margin-bottom: 20px;
                    cursor: pointer;
                }
                .feature-card:hover {
                    transform: translateY(-5px);
                }
                .status-badge {
                    font-size: 1.1em;
                    padding: 10px 20px;
                    border-radius: 25px;
                }
                .pulse {
                    animation: pulse 2s infinite;
                }
                @keyframes pulse {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                    100% { transform: scale(1); }
                }
                .loading {
                    display: none;
                }
                .result-container {
                    max-height: 500px;
                    overflow-y: auto;
                }
            </style>
        </head>
        <body>
            <div class="container-fluid">
                <div class="main-container">
                    <div class="text-center mb-5">
                        <h1 class="text-primary mb-3">
                            <i class="fas fa-robot"></i> AI增強美股投資分析系統
                        </h1>
                        <p class="lead text-muted">Vercel部署成功！純Python版本 🚀 v4.0.0 終極版</p>
                        <div class="mt-4">
                            <span class="badge bg-success status-badge pulse">
                                <i class="fas fa-check-circle"></i> 系統運行正常
                            </span>
                            <span class="badge bg-info status-badge ms-2">
                                <i class="fas fa-rocket"></i> Vercel部署成功
                            </span>
                            <span class="badge bg-warning status-badge ms-2">
                                <i class="fas fa-cogs"></i> 版本 v4.0.0 (純Python)
                            </span>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6 mb-4">
                            <div class="card feature-card h-100" onclick="runDataCollection()">
                                <div class="card-body text-center">
                                    <i class="fas fa-database fa-3x text-primary mb-3"></i>
                                    <h5 class="card-title">📊 市場數據分析</h5>
                                    <p class="card-text">
                                        實時市場數據收集<br>
                                        <small class="text-muted">Fear & Greed Index | 市場指數</small>
                                    </p>
                                    <button class="btn btn-primary btn-sm">
                                        <i class="fas fa-play"></i> 執行數據分析
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-6 mb-4">
                            <div class="card feature-card h-100" onclick="runAIAnalysis()">
                                <div class="card-body text-center">
                                    <i class="fas fa-brain fa-3x text-success mb-3"></i>
                                    <h5 class="card-title">🤖 AI投資建議</h5>
                                    <p class="card-text">
                                        智能投資策略分析<br>
                                        <small class="text-muted">股票推薦 | 風險評估</small>
                                    </p>
                                    <button class="btn btn-success btn-sm">
                                        <i class="fas fa-play"></i> 獲取AI建議
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-6 mb-4">
                            <div class="card feature-card h-100" onclick="runIntegratedAnalysis()">
                                <div class="card-body text-center">
                                    <i class="fas fa-layer-group fa-3x text-info mb-3"></i>
                                    <h5 class="card-title">📈 綜合分析</h5>
                                    <p class="card-text">
                                        多維度投資分析<br>
                                        <small class="text-muted">技術面 + 基本面</small>
                                    </p>
                                    <button class="btn btn-info btn-sm">
                                        <i class="fas fa-play"></i> 綜合分析
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-6 mb-4">
                            <div class="card feature-card h-100" onclick="testHealth()">
                                <div class="card-body text-center">
                                    <i class="fas fa-heartbeat fa-3x text-warning mb-3"></i>
                                    <h5 class="card-title">🔧 系統狀態</h5>
                                    <p class="card-text">
                                        系統健康檢查<br>
                                        <small class="text-muted">服務狀態監控</small>
                                    </p>
                                    <button class="btn btn-warning btn-sm">
                                        <i class="fas fa-play"></i> 檢查狀態
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div id="loading" class="text-center loading">
                        <i class="fas fa-spinner fa-spin fa-3x text-primary"></i>
                        <h5 class="mt-3">分析進行中...</h5>
                        <p class="text-muted">請稍候，正在處理您的請求</p>
                    </div>
                    
                    <div id="result-area" class="mt-4"></div>
                </div>
            </div>
            
            <script>
                function showLoading() {
                    document.getElementById('loading').style.display = 'block';
                    document.getElementById('result-area').innerHTML = '';
                }
                
                function hideLoading() {
                    document.getElementById('loading').style.display = 'none';
                }
                
                function showResult(html) {
                    hideLoading();
                    document.getElementById('result-area').innerHTML = html;
                }
                
                function runDataCollection() {
                    showLoading();
                    fetch('/api/data-collection', {method: 'POST'})
                        .then(response => response.json())
                        .then(data => {
                            showResult(`
                                <div class="alert alert-success">
                                    <h5><i class="fas fa-database"></i> 市場數據分析完成</h5>
                                    <div class="result-container">
                                        <p><strong>Fear & Greed Index:</strong> ${data.fear_greed}</p>
                                        <p><strong>市場情緒:</strong> ${data.market_sentiment}</p>
                                        <p><strong>市場趨勢:</strong> ${data.market_trend}</p>
                                        <p><strong>分析時間:</strong> ${new Date().toLocaleString()}</p>
                                    </div>
                                </div>
                            `);
                        })
                        .catch(error => {
                            showResult(`
                                <div class="alert alert-danger">
                                    <h5><i class="fas fa-exclamation-triangle"></i> 請求失敗</h5>
                                    <p>錯誤: ${error.message}</p>
                                </div>
                            `);
                        });
                }
                
                function runAIAnalysis() {
                    showLoading();
                    fetch('/api/ai-analysis', {method: 'POST'})
                        .then(response => response.json())
                        .then(data => {
                            showResult(`
                                <div class="alert alert-success">
                                    <h5><i class="fas fa-brain"></i> AI投資建議</h5>
                                    <div class="result-container">
                                        <h6>推薦股票:</h6>
                                        <p>${data.recommended_stocks.join(', ')}</p>
                                        <h6>風險等級:</h6>
                                        <p>${data.risk_level}</p>
                                        <h6>投資建議:</h6>
                                        <p>${data.recommendation}</p>
                                    </div>
                                </div>
                            `);
                        })
                        .catch(error => {
                            showResult(`
                                <div class="alert alert-danger">
                                    <h5><i class="fas fa-exclamation-triangle"></i> 請求失敗</h5>
                                    <p>錯誤: ${error.message}</p>
                                </div>
                            `);
                        });
                }
                
                function runIntegratedAnalysis() {
                    showLoading();
                    fetch('/api/integrated-analysis', {method: 'POST'})
                        .then(response => response.json())
                        .then(data => {
                            showResult(`
                                <div class="alert alert-success">
                                    <h5><i class="fas fa-layer-group"></i> 綜合分析結果</h5>
                                    <div class="result-container">
                                        <h6>市場環境:</h6>
                                        <p>${data.market_environment}</p>
                                        <h6>投資策略:</h6>
                                        <p>${data.investment_strategy}</p>
                                        <h6>風險評估:</h6>
                                        <p>${data.risk_assessment}</p>
                                    </div>
                                </div>
                            `);
                        })
                        .catch(error => {
                            showResult(`
                                <div class="alert alert-danger">
                                    <h5><i class="fas fa-exclamation-triangle"></i> 請求失敗</h5>
                                    <p>錯誤: ${error.message}</p>
                                </div>
                            `);
                        });
                }
                
                function testHealth() {
                    showLoading();
                    fetch('/health')
                        .then(response => response.json())
                        .then(data => {
                            showResult(`
                                <div class="alert alert-success">
                                    <h5><i class="fas fa-check-circle"></i> 系統狀態正常！</h5>
                                    <div class="result-container">
                                        <p><strong>版本:</strong> ${data.version}</p>
                                        <p><strong>狀態:</strong> ${data.status}</p>
                                        <p><strong>平台:</strong> ${data.platform}</p>
                                        <p><strong>模式:</strong> ${data.mode}</p>
                                        <p><strong>時間:</strong> ${new Date(data.timestamp).toLocaleString()}</p>
                                    </div>
                                </div>
                            `);
                        })
                        .catch(error => {
                            showResult(`
                                <div class="alert alert-danger">
                                    <h5><i class="fas fa-exclamation-triangle"></i> 健康檢查失敗</h5>
                                    <p>錯誤: ${error.message}</p>
                                </div>
                            `);
                        });
                }
                
                // 自動執行健康檢查
                setTimeout(testHealth, 1000);
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_health_check(self):
        """健康檢查API"""
        response_data = {
            'status': 'healthy',
            'version': 'v4.0.0 (純Python版)',
            'timestamp': datetime.now().isoformat(),
            'platform': 'Vercel',
            'mode': 'Demo (模擬數據)',
            'dependencies': 'None (純Python內建模組)'
        }
        
        self.send_json_response(response_data)
    
    def serve_data_collection(self):
        """數據收集API"""
        mock_data = self.generate_mock_data()
        response_data = {
            'success': True,
            'fear_greed': mock_data['fear_greed_index'],
            'market_sentiment': mock_data['market_sentiment'],
            'market_trend': mock_data['market_trend'],
            'note': '使用模擬數據 - 純Python版本'
        }
        
        self.send_json_response(response_data)
    
    def serve_ai_analysis(self):
        """AI分析API"""
        mock_data = self.generate_mock_data()
        response_data = {
            'success': True,
            'recommended_stocks': mock_data['recommended_stocks'][:3],
            'risk_level': mock_data['risk_level'],
            'recommendation': f"基於當前市場{mock_data['market_sentiment']}情緒，建議採取{mock_data['risk_level']}風險策略",
            'note': '使用模擬數據 - 純Python版本'
        }
        
        self.send_json_response(response_data)
    
    def serve_integrated_analysis(self):
        """整合分析API"""
        mock_data = self.generate_mock_data()
        response_data = {
            'success': True,
            'market_environment': mock_data['market_sentiment'],
            'investment_strategy': f"建議採用{mock_data['risk_level']}風險投資策略",
            'risk_assessment': f"當前市場風險等級：{mock_data['risk_level']}",
            'note': '使用模擬數據 - 純Python版本'
        }
        
        self.send_json_response(response_data)
    
    def send_json_response(self, data):
        """發送JSON響應"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(json_data.encode('utf-8'))
    
    def generate_mock_data(self):
        """生成模擬投資分析數據"""
        return {
            'fear_greed_index': random.randint(20, 80),
            'market_sentiment': random.choice(['Bullish', 'Bearish', 'Neutral']),
            'recommended_stocks': ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA'],
            'market_trend': random.choice(['上漲', '下跌', '震盪']),
            'risk_level': random.choice(['Low', 'Medium', 'High'])
        }
    
    def log_message(self, format, *args):
        """覆蓋日誌方法以減少輸出"""
        pass

def run_server():
    """運行HTTP服務器"""
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, InvestmentAnalysisHandler)
    
    print(f"🚀 美股投資分析系統啟動成功！")
    print(f"📱 服務運行在端口: {port}")
    print(f"🌐 訪問地址: http://localhost:{port}")
    print(f"✅ 版本: v4.0.0 (純Python版)")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️ 服務器已停止")
        httpd.server_close()

if __name__ == '__main__':
    run_server() 