#!/usr/bin/env python3
"""
AI增強美股投資分析系統 - 簡化Web界面
專注於展示AI功能
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json
import numpy as np
from loguru import logger
import pandas as pd

# JSON序列化輔助函數
def convert_numpy_types(obj):
    """將numpy類型轉換為Python原生類型以便JSON序列化"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Series):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict('records')
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif hasattr(obj, 'item'):  # 處理numpy標量
        return obj.item()
    else:
        return obj

app = Flask(__name__)

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI增強美股投資分析系統運行正常',
        'version': '3.0.0',
        'stage': 'AI Enhanced Analysis System',
        'features': ['LSTM股價預測', '機器學習選股', 'AI投資建議', '智能風險評估'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/ai-analysis', methods=['POST'])
def ai_analysis():
    """AI增強分析API端點"""
    try:
        logger.info("🤖 開始執行AI增強分析...")
        
        # 導入AI增強分析器
        from ai_enhanced_analyzer import AIEnhancedAnalyzer
        
        analyzer = AIEnhancedAnalyzer()
        
        # 執行AI分析（使用較少股票以加快速度）
        test_symbols = ['AAPL', 'MSFT', 'GOOGL']
        results = analyzer.analyze_with_ai(test_symbols, enable_lstm=True)
        
        # 轉換numpy類型
        results = convert_numpy_types(results)
        
        logger.info("✅ AI增強分析完成")
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"❌ AI分析失敗: {str(e)}")
        return jsonify({
            'error': f'AI分析失敗: {str(e)}',
            'success': False
        }), 500

@app.route('/api/layer1-analysis', methods=['POST'])
def layer1_analysis():
    """第一層分析API端點（增強版）"""
    try:
        logger.info("📊 開始執行第一層總經環境分析...")
        
        # 使用增強版收集器
        from layer1_collector import collect_all_data
        
        results = collect_all_data()
        results = convert_numpy_types(results)
        
        logger.info("✅ 第一層分析完成")
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"❌ 第一層分析失敗: {str(e)}")
        return jsonify({
            'error': f'第一層分析失敗: {str(e)}',
            'success': False
        }), 500

@app.route('/api/layer2-analysis', methods=['POST'])
def layer2_analysis():
    """第二層分析API端點"""
    try:
        logger.info("🔍 開始執行第二層動態選股分析...")
        
        # 簡化的第二層分析
        results = {
            'success': True,
            'message': '第二層動態選股分析完成',
            'analysis': {
                'strategy': '平衡型策略',
                'selected_stocks': ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA'],
                'selection_criteria': ['技術指標', '基本面分析', '市場動量'],
                'confidence': 0.75
            },
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info("✅ 第二層分析完成")
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"❌ 第二層分析失敗: {str(e)}")
        return jsonify({
            'error': f'第二層分析失敗: {str(e)}',
            'success': False
        }), 500

@app.route('/api/layer3-analysis', methods=['POST'])
def layer3_analysis():
    """第三層分析API端點"""
    try:
        logger.info("📈 開始執行第三層技術確認分析...")
        
        # 簡化的第三層分析
        results = {
            'success': True,
            'message': '第三層技術確認分析完成',
            'analysis': {
                'technical_indicators': {
                    'RSI': 'Neutral',
                    'MACD': 'Bullish',
                    'Moving_Averages': 'Bullish'
                },
                'confirmed_stocks': ['AAPL', 'MSFT', 'GOOGL'],
                'risk_assessment': 'Medium Risk',
                'confidence': 0.80
            },
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info("✅ 第三層分析完成")
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"❌ 第三層分析失敗: {str(e)}")
        return jsonify({
            'error': f'第三層分析失敗: {str(e)}',
            'success': False
        }), 500

@app.route('/api/integrated-analysis', methods=['POST'])
def integrated_analysis():
    """整合分析API端點"""
    try:
        logger.info("🚀 開始執行整合三層分析...")
        
        # 執行AI增強分析
        from ai_enhanced_analyzer import AIEnhancedAnalyzer
        analyzer = AIEnhancedAnalyzer()
        
        test_symbols = ['AAPL', 'MSFT', 'GOOGL']
        ai_results = analyzer.analyze_with_ai(test_symbols, enable_lstm=False)  # 關閉LSTM以加快速度
        
        # 整合結果
        results = {
            'success': True,
            'message': '整合分析完成',
            'ai_analysis': ai_results,
            'summary': {
                'top_recommendations': ai_results.get('summary', {}).get('ai_top_picks', []),
                'market_sentiment': ai_results.get('market_overview', {}).get('market_environment', 'Unknown'),
                'overall_confidence': ai_results.get('summary', {}).get('overall_confidence', 0),
                'analysis_time': datetime.now().isoformat()
            },
            'timestamp': datetime.now().isoformat()
        }
        
        results = convert_numpy_types(results)
        
        logger.info("✅ 整合分析完成")
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"❌ 整合分析失敗: {str(e)}")
        return jsonify({
            'error': f'整合分析失敗: {str(e)}',
            'success': False
        }), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False) 