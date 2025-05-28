#!/usr/bin/env python3
"""
美股投資分析系統 - Web介面
提供現代化的Web介面來操作投資分析系統
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json
import threading
import time
import os
import numpy as np
from loguru import logger
import pandas as pd

from layer1_collector import Layer1Collector
from layer2_collector import Layer2Collector
from layer3_collector import Layer3Collector
from integrated_analyzer import IntegratedAnalyzer

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

# 全域變數儲存最新數據
latest_layer1_data = None
latest_layer2_data = None
latest_layer3_data = None
data_lock = threading.Lock()

# 創建整合分析器實例
integrated_analyzer = IntegratedAnalyzer()

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')

# ==================== 第一層 API ====================

@app.route('/api/layer1/collect', methods=['POST'])
def collect_layer1_data():
    """收集第一層數據的API端點"""
    try:
        collector = Layer1Collector()
        data = collector.collect_all_data()
        
        # 更新全域數據
        global latest_layer1_data
        with data_lock:
            latest_layer1_data = data
        
        return jsonify({
            'success': True,
            'data': data,
            'message': '第一層數據收集完成'
        })
    except Exception as e:
        logger.error(f"第一層數據收集失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '第一層數據收集失敗'
        }), 500

@app.route('/api/layer1/summary')
def get_layer1_summary():
    """獲取第一層數據摘要"""
    try:
        collector = Layer1Collector()
        summary = collector.get_summary_report()
        return jsonify({
            'success': True,
            'data': summary
        })
    except Exception as e:
        logger.error(f"第一層摘要獲取失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/layer1/latest')
def get_latest_layer1_data():
    """獲取最新的第一層數據"""
    global latest_layer1_data
    with data_lock:
        if latest_layer1_data:
            return jsonify({
                'success': True,
                'data': latest_layer1_data
            })
        else:
            return jsonify({
                'success': False,
                'message': '尚無數據，請先收集數據'
            })

# ==================== 第二層 API ====================

@app.route('/api/layer2/collect', methods=['POST'])
def collect_layer2_data():
    """收集第二層數據的API端點"""
    try:
        collector = Layer2Collector()
        data = collector.collect_all_data()
        
        # 更新全域數據
        global latest_layer2_data
        with data_lock:
            latest_layer2_data = data
        
        return jsonify({
            'success': True,
            'data': data,
            'message': '第二層數據收集完成'
        })
    except Exception as e:
        logger.error(f"第二層數據收集失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '第二層數據收集失敗'
        }), 500

@app.route('/api/layer2/summary')
def get_layer2_summary():
    """獲取第二層數據摘要"""
    try:
        collector = Layer2Collector()
        summary = collector.get_summary_report()
        return jsonify({
            'success': True,
            'data': summary
        })
    except Exception as e:
        logger.error(f"第二層摘要獲取失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/layer2/latest')
def get_latest_layer2_data():
    """獲取最新的第二層數據"""
    global latest_layer2_data
    with data_lock:
        if latest_layer2_data:
            return jsonify({
                'success': True,
                'data': latest_layer2_data
            })
        else:
            return jsonify({
                'success': False,
                'message': '尚無數據，請先收集數據'
            })

@app.route('/api/layer2/economic-calendar')
def get_economic_calendar():
    """獲取財經事件日曆"""
    try:
        collector = Layer2Collector()
        data = collector.get_economic_calendar()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"財經事件日曆獲取失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/layer2/news-sentiment')
def get_news_sentiment():
    """獲取新聞情緒分析"""
    try:
        collector = Layer2Collector()
        data = collector.get_news_sentiment()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"新聞情緒分析失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/layer2/sector-rotation')
def get_sector_rotation():
    """獲取產業輪動分析"""
    try:
        collector = Layer2Collector()
        data = collector.get_sector_rotation()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"產業輪動分析失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/layer2/stock-screener')
def get_stock_screener():
    """獲取選股篩選結果"""
    try:
        collector = Layer2Collector()
        data = collector.get_stock_screener()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"選股篩選失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== 第三層 API ====================

@app.route('/api/layer3/collect', methods=['POST'])
def collect_layer3_data():
    """收集第三層數據的API端點"""
    try:
        collector = Layer3Collector()
        data = collector.collect_all_data()
        
        # 更新全域數據
        global latest_layer3_data
        with data_lock:
            latest_layer3_data = data
        
        return jsonify({
            'success': True,
            'data': data,
            'message': '第三層數據收集完成'
        })
    except Exception as e:
        logger.error(f"第三層數據收集失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '第三層數據收集失敗'
        }), 500

@app.route('/api/layer3/summary')
def get_layer3_summary():
    """獲取第三層數據摘要"""
    try:
        collector = Layer3Collector()
        summary = collector.get_summary_report()
        return jsonify({
            'success': True,
            'data': summary
        })
    except Exception as e:
        logger.error(f"第三層摘要獲取失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/layer3/latest')
def get_latest_layer3_data():
    """獲取最新的第三層數據"""
    global latest_layer3_data
    with data_lock:
        if latest_layer3_data:
            return jsonify({
                'success': True,
                'data': latest_layer3_data
            })
        else:
            return jsonify({
                'success': False,
                'message': '尚無數據，請先收集數據'
            })

@app.route('/api/layer3/technical-analysis')
def get_technical_analysis():
    """獲取技術分析結果"""
    try:
        collector = Layer3Collector()
        data = collector.get_technical_analysis()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"技術分析獲取失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/layer3/risk-management')
def get_risk_management():
    """獲取風險管理分析"""
    try:
        collector = Layer3Collector()
        data = collector.get_risk_management()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"風險管理分析失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== 整合分析 API ====================

@app.route('/api/integrated-analysis', methods=['POST'])
def integrated_analysis():
    """整合四層分析API"""
    try:
        # 獲取用戶偏好（如果有的話）
        user_preferences = request.get_json() if request.is_json else {}
        
        logger.info("🚀 開始執行整合四層分析...")
        
        # 執行完整的四層聯動分析
        result = integrated_analyzer.analyze_complete_flow(user_preferences)
        
        # 轉換numpy類型以便JSON序列化
        result = convert_numpy_types(result)
        
        if result.get('success'):
            logger.info("✅ 整合分析完成")
            return jsonify(result)
        else:
            logger.error(f"❌ 整合分析失敗: {result.get('error')}")
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"整合分析API錯誤: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "整合分析服務暫時不可用"
        }), 500

@app.route('/integrated')
def integrated_page():
    """整合分析頁面"""
    return render_template('integrated.html')

# ==================== 頁面路由 ====================

@app.route('/dashboard')
def dashboard():
    """儀表板頁面"""
    return render_template('dashboard.html')

@app.route('/layer2')
def layer2():
    """第二層功能頁面"""
    return render_template('layer2.html')

@app.route('/layer3')
def layer3():
    """第三層功能頁面（預留）"""
    return render_template('layer3.html')

if __name__ == '__main__':
    # 獲取端口號（Heroku會提供PORT環境變數）
    port = int(os.environ.get('PORT', 5000))
    
    # 判斷是否為生產環境
    is_production = os.environ.get('FLASK_ENV') != 'development'
    
    logger.info("🚀 啟動美股投資分析系統 Web 介面")
    logger.info(f"🌐 運行模式: {'生產' if is_production else '開發'}")
    logger.info(f"🔌 端口: {port}")
    
    app.run(
        debug=not is_production,
        host='0.0.0.0',
        port=port
    ) 