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

app = Flask(__name__)

# 全域變數儲存最新數據
latest_data = None
data_lock = threading.Lock()

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')

@app.route('/api/layer1/collect', methods=['POST'])
def collect_layer1_data():
    """收集第一層數據的API端點"""
    try:
        collector = Layer1Collector()
        data = collector.collect_all_data()
        
        # 更新全域數據
        global latest_data
        with data_lock:
            latest_data = data
        
        return jsonify({
            'success': True,
            'data': data,
            'message': '第一層數據收集完成'
        })
    except Exception as e:
        logger.error(f"數據收集失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '數據收集失敗'
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
        logger.error(f"摘要獲取失敗: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/layer1/latest')
def get_latest_data():
    """獲取最新的數據"""
    global latest_data
    with data_lock:
        if latest_data:
            return jsonify({
                'success': True,
                'data': latest_data
            })
        else:
            return jsonify({
                'success': False,
                'message': '尚無數據，請先收集數據'
            })

@app.route('/dashboard')
def dashboard():
    """儀表板頁面"""
    return render_template('dashboard.html')

@app.route('/layer2')
def layer2():
    """第二層功能頁面（預留）"""
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