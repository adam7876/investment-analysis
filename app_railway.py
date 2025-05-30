#!/usr/bin/env python3
"""
四層聯動美股投資分析系統 - Railway部署專用版本
簡化版本，確保部署穩定性
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json
import os

app = Flask(__name__)

# 內建HTML模板
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>四層聯動美股投資分析系統</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white; 
            padding: 30px; 
            text-align: center; 
        }
        .header h1 { margin: 0; font-size: 2.5em; }
        .header p { margin: 10px 0 0 0; opacity: 0.9; }
        .status { 
            background: #e8f5e8; 
            padding: 20px; 
            margin: 20px; 
            border-radius: 8px; 
            border-left: 5px solid #27ae60;
        }
        .feature-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 20px; 
            padding: 20px;
        }
        .feature-card { 
            background: #f8f9fa; 
            padding: 25px; 
            border-radius: 10px; 
            border: 1px solid #e9ecef;
            transition: transform 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .feature-card h3 { 
            color: #2c3e50; 
            margin-top: 0; 
            display: flex;
            align-items: center;
        }
        .feature-card .icon {
            font-size: 1.5em;
            margin-right: 10px;
        }
        .btn { 
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white; 
            padding: 12px 25px; 
            border: none; 
            border-radius: 6px; 
            cursor: pointer; 
            font-size: 16px;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        .btn:hover { 
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }
        .api-test { 
            background: #f1f3f4; 
            padding: 15px; 
            border-radius: 5px; 
            margin-top: 15px; 
            font-family: monospace;
        }
        .version-info {
            text-align: center;
            padding: 20px;
            color: #7f8c8d;
            border-top: 1px solid #ecf0f1;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 四層聯動美股投資分析系統</h1>
            <p>Complete Four-Layer US Stock Investment Analysis System</p>
        </div>
        
        <div class="status">
            <h3>✅ 系統狀態：運行正常</h3>
            <p>Railway部署成功，四層分析系統已啟動</p>
            <p><strong>部署時間：</strong> <span id="timestamp"></span></p>
        </div>

        <div class="feature-grid">
            <div class="feature-card">
                <h3><span class="icon">📊</span>第一層：市場總觀趨勢</h3>
                <ul>
                    <li>總經環境分析（GDP、通膨、利率）</li>
                    <li>市場情緒指標（恐懼貪婪指數）</li>
                    <li>資金流向監控</li>
                </ul>
                <button class="btn" onclick="testLayer1()">測試第一層分析</button>
                <div id="layer1-result" class="api-test" style="display:none;"></div>
            </div>

            <div class="feature-card">
                <h3><span class="icon">🏭</span>第二層：產業與催化劑</h3>
                <ul>
                    <li>本週重點觀察產業</li>
                    <li>產業輪動分析</li>
                    <li>催化劑事件追蹤</li>
                </ul>
                <button class="btn" onclick="testLayer2()">測試第二層分析</button>
                <div id="layer2-result" class="api-test" style="display:none;"></div>
            </div>

            <div class="feature-card">
                <h3><span class="icon">📈</span>第三層：精選操作名單</h3>
                <ul>
                    <li>個股技術分析</li>
                    <li>進出場時機判斷</li>
                    <li>風險評估與管理</li>
                </ul>
                <button class="btn" onclick="testLayer3()">測試第三層分析</button>
                <div id="layer3-result" class="api-test" style="display:none;"></div>
            </div>

            <div class="feature-card">
                <h3><span class="icon">⚡</span>第四層：選擇權策略</h3>
                <ul>
                    <li>選擇權策略建議</li>
                    <li>風險收益評估</li>
                    <li>市場波動度分析</li>
                </ul>
                <button class="btn" onclick="testLayer4()">測試第四層分析</button>
                <div id="layer4-result" class="api-test" style="display:none;"></div>
            </div>
        </div>

        <div style="text-align: center; padding: 30px;">
            <button class="btn" onclick="runCompleteAnalysis()" style="font-size: 18px; padding: 15px 30px;">
                🎯 執行完整四層聯動分析
            </button>
            <div id="complete-result" class="api-test" style="display:none; margin-top: 20px; text-align: left;"></div>
        </div>

        <div class="version-info">
            <p>版本 2.0.0 | Railway部署版本 | 四層聯動分析系統</p>
        </div>
    </div>

    <script>
        // 設置時間戳
        document.getElementById('timestamp').textContent = new Date().toLocaleString('zh-TW');

        function showResult(elementId, data) {
            const element = document.getElementById(elementId);
            element.style.display = 'block';
            
            if (elementId === 'complete-result' && data.success) {
                // 格式化完整四層分析結果
                element.innerHTML = formatCompleteAnalysis(data);
            } else {
                // 格式化其他結果
                element.innerHTML = formatSimpleResult(data);
            }
        }

        function formatCompleteAnalysis(data) {
            let html = '<div style="background: #f8f9fa; padding: 20px; border-radius: 8px; line-height: 1.6;">';
            
            // 第一層：市場總觀
            html += '<h3 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">📊 第一層：市場總觀趨勢</h3>';
            const layer1 = data.layer1_market_overview;
            html += `<div style="margin: 15px 0; padding: 15px; background: #e8f5e8; border-radius: 5px;">`;
            html += `<p><strong>🎯 市場情緒：</strong>${layer1.market_sentiment.sentiment} (${layer1.market_sentiment.fear_greed_index})</p>`;
            html += `<p><strong>📈 經濟指標：</strong></p>`;
            html += `<ul style="margin: 10px 0; padding-left: 20px;">`;
            html += `<li>GDP成長率：${layer1.economic_indicators.gdp_growth}%</li>`;
            html += `<li>通膨率：${layer1.economic_indicators.inflation_rate}%</li>`;
            html += `<li>失業率：${layer1.economic_indicators.unemployment_rate}%</li>`;
            html += `<li>聯準會利率：${layer1.economic_indicators.fed_rate}%</li>`;
            html += `</ul>`;
            html += `<p><strong>💡 市場趨勢：</strong>${layer1.market_trend}</p>`;
            html += `</div>`;

            // 第二層：產業分析
            html += '<h3 style="color: #2c3e50; border-bottom: 2px solid #e74c3c; padding-bottom: 10px;">🏭 第二層：產業催化劑分析</h3>';
            const layer2 = data.layer2_sector_analysis;
            html += `<div style="margin: 15px 0; padding: 15px; background: #fef9e7; border-radius: 5px;">`;
            html += `<p><strong>🎯 重點觀察產業：</strong></p>`;
            html += `<ul style="margin: 10px 0; padding-left: 20px;">`;
            layer2.focus_sectors.forEach(sector => {
                html += `<li><strong>${sector.sector}</strong> (強度: ${sector.strength}/10)<br>`;
                html += `<span style="color: #666; font-size: 0.9em;">${sector.reason}</span></li>`;
            });
            html += `</ul>`;
            html += `<p><strong>⚡ 關鍵催化劑：</strong>${layer2.catalysts.join('、')}</p>`;
            html += `</div>`;

            // 第三層：操作名單
            html += '<h3 style="color: #2c3e50; border-bottom: 2px solid #f39c12; padding-bottom: 10px;">📈 第三層：精選操作名單</h3>';
            const layer3 = data.layer3_trading_watchlist;
            html += `<div style="margin: 15px 0; padding: 15px; background: #f0f8ff; border-radius: 5px;">`;
            layer3.forEach(stock => {
                const signalColor = stock.signal === '強力買進' ? '#27ae60' : stock.signal === '買進' ? '#f39c12' : '#95a5a6';
                html += `<div style="margin: 10px 0; padding: 10px; background: white; border-left: 4px solid ${signalColor}; border-radius: 3px;">`;
                html += `<p><strong>${stock.symbol} - ${stock.company}</strong></p>`;
                html += `<p>評分：<span style="color: ${signalColor}; font-weight: bold;">${stock.score}/100</span> | `;
                html += `信號：<span style="color: ${signalColor}; font-weight: bold;">${stock.signal}</span></p>`;
                html += `<p>目標價：$${stock.target_price} | 現價：$${stock.current_price}</p>`;
                html += `<p style="color: #666; font-size: 0.9em;">${stock.reason}</p>`;
                html += `</div>`;
            });
            html += `</div>`;

            // 第四層：選擇權策略
            html += '<h3 style="color: #2c3e50; border-bottom: 2px solid #9b59b6; padding-bottom: 10px;">⚡ 第四層：選擇權策略建議</h3>';
            const layer4 = data.layer4_options_strategies;
            html += `<div style="margin: 15px 0; padding: 15px; background: #f8f0ff; border-radius: 5px;">`;
            html += `<p><strong>🎯 推薦策略：</strong>${layer4.recommended_strategy}</p>`;
            html += `<div style="margin: 15px 0;">`;
            layer4.strategies.forEach(strategy => {
                html += `<div style="margin: 10px 0; padding: 10px; background: white; border-radius: 3px; border: 1px solid #ddd;">`;
                html += `<p><strong>${strategy.type}</strong> - ${strategy.target}</p>`;
                if (strategy.strike) {
                    html += `<p>履約價：$${strategy.strike} | 到期日：${strategy.expiry}</p>`;
                    html += `<p>權利金：$${strategy.premium} | 風險等級：${strategy.risk_level}</p>`;
                    html += `<p>最大獲利：${strategy.max_profit} | 最大損失：$${strategy.max_loss}</p>`;
                } else {
                    html += `<p>多頭履約價：$${strategy.long_strike} | 空頭履約價：$${strategy.short_strike}</p>`;
                    html += `<p>淨權利金：$${strategy.net_premium} | 風險等級：${strategy.risk_level}</p>`;
                    html += `<p>最大獲利：$${strategy.max_profit} | 最大損失：$${strategy.max_loss}</p>`;
                }
                html += `</div>`;
            });
            html += `</div></div>`;

            // AI整合建議
            html += '<h3 style="color: #2c3e50; border-bottom: 2px solid #1abc9c; padding-bottom: 10px;">🤖 AI整合投資建議</h3>';
            const ai = data.ai_integrated_recommendation;
            html += `<div style="margin: 15px 0; padding: 15px; background: #e8f8f5; border-radius: 5px;">`;
            html += `<p><strong>📊 整體策略：</strong>${ai.overall_strategy}</p>`;
            html += `<p><strong>💰 資產配置：</strong></p>`;
            html += `<ul style="margin: 10px 0; padding-left: 20px;">`;
            Object.entries(ai.allocation).forEach(([key, value]) => {
                html += `<li>${key}：${value}</li>`;
            });
            html += `</ul>`;
            html += `<p><strong>💡 關鍵要點：</strong></p>`;
            html += `<ul style="margin: 10px 0; padding-left: 20px;">`;
            ai.key_points.forEach(point => {
                html += `<li>${point}</li>`;
            });
            html += `</ul>`;
            html += `<p><strong>⚠️ 風險提醒：</strong><span style="color: #e74c3c;">${ai.risk_warning}</span></p>`;
            html += `</div>`;

            html += `<div style="text-align: center; margin-top: 20px; padding: 15px; background: #ecf0f1; border-radius: 5px;">`;
            html += `<p style="color: #7f8c8d; margin: 0;">分析完成時間：${new Date(data.timestamp).toLocaleString('zh-TW')}</p>`;
            html += `</div>`;
            
            html += '</div>';
            return html;
        }

        function formatSimpleResult(data) {
            if (data.error) {
                return `<div style="color: #e74c3c; padding: 10px; background: #fdf2f2; border-radius: 5px;">
                    <strong>❌ 錯誤：</strong>${data.error}<br>
                    <span style="font-size: 0.9em;">${data.message || ''}</span>
                </div>`;
            }

            let html = '<div style="background: #f8f9fa; padding: 15px; border-radius: 5px; line-height: 1.5;">';
            
            if (data.data) {
                const d = data.data;
                
                if (d.market_sentiment) {
                    html += `<p><strong>市場情緒：</strong>${d.market_sentiment}</p>`;
                }
                
                if (d.economic_indicators) {
                    html += `<p><strong>經濟指標：</strong></p><ul>`;
                    Object.entries(d.economic_indicators).forEach(([key, value]) => {
                        const keyMap = {
                            'gdp_growth': 'GDP成長率',
                            'inflation': '通膨率', 
                            'unemployment': '失業率'
                        };
                        html += `<li>${keyMap[key] || key}：${value}</li>`;
                    });
                    html += `</ul>`;
                }
                
                if (d.market_trend) {
                    html += `<p><strong>市場趨勢：</strong>${d.market_trend}</p>`;
                }
                
                if (d.focus_sectors) {
                    html += `<p><strong>重點產業：</strong>${d.focus_sectors.join('、')}</p>`;
                }
                
                if (d.catalysts) {
                    html += `<p><strong>催化劑：</strong>${d.catalysts.join('、')}</p>`;
                }
                
                if (d.rotation_signal) {
                    html += `<p><strong>輪動信號：</strong>${d.rotation_signal}</p>`;
                }
                
                if (d.watchlist) {
                    html += `<p><strong>觀察名單：</strong></p><ul>`;
                    d.watchlist.forEach(stock => {
                        html += `<li>${stock.symbol} - 評分：${stock.score} - ${stock.signal}</li>`;
                    });
                    html += `</ul>`;
                }
                
                if (d.strategy) {
                    html += `<p><strong>策略：</strong>${d.strategy}</p>`;
                    html += `<p><strong>標的：</strong>${d.target}</p>`;
                    html += `<p><strong>履約價：</strong>${d.strike}</p>`;
                    html += `<p><strong>到期日：</strong>${d.expiry}</p>`;
                    html += `<p><strong>風險等級：</strong>${d.risk_level}</p>`;
                }
            }
            
            html += '</div>';
            return html;
        }

        function testLayer1() {
            showResult('layer1-result', {
                status: 'success',
                data: {
                    market_sentiment: '貪婪 (71)',
                    economic_indicators: {
                        gdp_growth: '2.1%',
                        inflation: '3.2%',
                        unemployment: '3.8%'
                    },
                    market_trend: '多頭趨勢'
                }
            });
        }

        function testLayer2() {
            showResult('layer2-result', {
                status: 'success',
                data: {
                    focus_sectors: ['AI人工智慧', '綠能科技', '生技醫療'],
                    catalysts: ['財報季', 'Fed會議', '地緣政治'],
                    rotation_signal: '科技股 → 價值股'
                }
            });
        }

        function testLayer3() {
            showResult('layer3-result', {
                status: 'success',
                data: {
                    watchlist: [
                        { symbol: 'NVDA', score: 88, signal: '強力買進' },
                        { symbol: 'MSFT', score: 82, signal: '買進' },
                        { symbol: 'AAPL', score: 75, signal: '持有' }
                    ]
                }
            });
        }

        function testLayer4() {
            showResult('layer4-result', {
                status: 'success',
                data: {
                    strategy: 'Buy Call',
                    target: 'NVDA',
                    strike: '$450',
                    expiry: '2025-06-20',
                    risk_level: '中等'
                }
            });
        }

        async function runCompleteAnalysis() {
            const resultDiv = document.getElementById('complete-result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = '🔄 正在執行四層聯動分析，請稍候...';

            try {
                const response = await fetch('/api/integrated-analysis', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({})
                });
                
                const data = await response.json();
                showResult('complete-result', data);
            } catch (error) {
                showResult('complete-result', {
                    error: '分析服務暫時不可用',
                    message: error.message
                });
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """主頁面"""
    return INDEX_HTML

@app.route('/health')
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'healthy',
        'message': '四層聯動美股投資分析系統運行正常',
        'version': '2.0.0',
        'stage': 'Complete Four-Layer Analysis System',
        'features': ['市場總觀分析', '產業催化劑分析', '精選操作名單', '選擇權策略建議'],
        'deployment': 'Railway',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/integrated-analysis', methods=['POST'])
def integrated_analysis():
    """四層聯動分析API - 簡化版本"""
    try:
        # 模擬四層分析結果
        result = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "layer1_market_overview": {
                "market_sentiment": {
                    "fear_greed_index": 71,
                    "sentiment": "Greed",
                    "description": "市場情緒偏向貪婪，投資者信心較高"
                },
                "economic_indicators": {
                    "gdp_growth": 2.1,
                    "inflation_rate": 3.2,
                    "unemployment_rate": 3.8,
                    "fed_rate": 5.25
                },
                "market_trend": "多頭趨勢，但需注意高估值風險"
            },
            "layer2_sector_analysis": {
                "focus_sectors": [
                    {
                        "sector": "AI人工智慧",
                        "reason": "ChatGPT等技術突破帶動產業革命",
                        "strength": 9
                    },
                    {
                        "sector": "綠能科技", 
                        "reason": "政府政策支持與ESG投資趨勢",
                        "strength": 8
                    },
                    {
                        "sector": "生技醫療",
                        "reason": "人口老化與新藥開發機會",
                        "strength": 7
                    }
                ],
                "catalysts": ["Q4財報季", "Fed利率決議", "地緣政治風險"]
            },
            "layer3_trading_watchlist": [
                {
                    "symbol": "NVDA",
                    "company": "NVIDIA Corporation",
                    "score": 88,
                    "signal": "強力買進",
                    "target_price": 480,
                    "current_price": 420,
                    "reason": "AI晶片需求強勁，技術面突破關鍵阻力"
                },
                {
                    "symbol": "MSFT",
                    "company": "Microsoft Corporation", 
                    "score": 82,
                    "signal": "買進",
                    "target_price": 380,
                    "current_price": 350,
                    "reason": "雲端服務成長穩健，AI整合效益顯現"
                },
                {
                    "symbol": "AAPL",
                    "company": "Apple Inc.",
                    "score": 75,
                    "signal": "持有",
                    "target_price": 200,
                    "current_price": 185,
                    "reason": "iPhone銷售穩定，服務業務持續成長"
                }
            ],
            "layer4_options_strategies": {
                "recommended_strategy": "保守型策略",
                "strategies": [
                    {
                        "type": "Buy Call",
                        "target": "NVDA",
                        "strike": 450,
                        "expiry": "2025-06-20",
                        "premium": 25,
                        "risk_level": "中等",
                        "max_profit": "無限",
                        "max_loss": 25
                    },
                    {
                        "type": "Bull Call Spread",
                        "target": "MSFT", 
                        "long_strike": 360,
                        "short_strike": 380,
                        "expiry": "2025-05-16",
                        "net_premium": 8,
                        "risk_level": "低",
                        "max_profit": 12,
                        "max_loss": 8
                    }
                ]
            },
            "ai_integrated_recommendation": {
                "overall_strategy": "積極成長型",
                "allocation": {
                    "科技股": "60%",
                    "價值股": "25%", 
                    "現金": "15%"
                },
                "key_points": [
                    "重點配置AI相關科技股",
                    "適度配置傳統價值股平衡風險",
                    "保留現金應對市場波動",
                    "分批建倉控制進場風險"
                ],
                "risk_warning": "注意科技股估值偏高，建議分散投資"
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "分析服務暫時不可用，請稍後再試"
        }), 500

@app.route('/api/test')
def api_test():
    """API測試端點"""
    return jsonify({
        'success': True,
        'message': 'API運行正常',
        'data': {
            'system': '四層聯動美股投資分析系統',
            'version': '2.0.0',
            'stage': 'Complete System',
            'timestamp': datetime.now().isoformat()
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 啟動四層聯動美股投資分析系統（Railway版），端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 