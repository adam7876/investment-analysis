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
from loguru import logger

from layer1_collector import Layer1Collector
from layer2_collector import Layer2Collector

app = Flask(__name__)

# 全域變數儲存最新數據
latest_layer1_data = None
latest_layer2_data = None
data_lock = threading.Lock()

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