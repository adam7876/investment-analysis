#!/usr/bin/env python3
"""
Railway部署進度監控和功能測試
"""

import requests
import time
import json
from datetime import datetime

def check_deployment_status():
    """檢查Railway部署狀態"""
    url = "https://web-production-9cc8f.up.railway.app"
    
    print("🚀 檢查Railway部署狀態...")
    print("=" * 60)
    print(f"📍 應用URL: {url}")
    print(f"⏰ 檢查時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 測試健康檢查
    try:
        print("🔍 測試健康檢查端點...")
        response = requests.get(f"{url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康檢查成功")
            print(f"   版本: {data.get('version', 'N/A')}")
            print(f"   階段: {data.get('stage', 'N/A')}")
            print(f"   狀態: {data.get('status', 'N/A')}")
        else:
            print(f"❌ 健康檢查失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康檢查連接失敗: {str(e)}")
        return False
    
    print()
    
    # 測試主頁面
    try:
        print("🏠 測試主頁面...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            if "四層聯動美股投資分析系統" in response.text:
                print("✅ 主頁面載入成功")
                if "完整版" in response.text or "integrated" in response.text.lower():
                    print("✅ 檢測到完整版系統")
                else:
                    print("⚠️ 可能仍是階段1版本")
            else:
                print("⚠️ 主頁面內容異常")
        else:
            print(f"❌ 主頁面載入失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ 主頁面連接失敗: {str(e)}")
    
    print()
    
    # 測試API端點
    try:
        print("🔧 測試API端點...")
        response = requests.get(f"{url}/api/test", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API測試成功")
            print(f"   系統: {data.get('data', {}).get('system', 'N/A')}")
            print(f"   階段: {data.get('data', {}).get('stage', 'N/A')}")
        else:
            print(f"❌ API測試失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ API連接失敗: {str(e)}")
    
    print()
    
    # 測試四層分析端點
    try:
        print("🎯 測試四層分析端點...")
        response = requests.post(f"{url}/api/integrated-analysis", 
                               json={}, timeout=30)
        if response.status_code == 200:
            print("✅ 四層分析端點可用")
            try:
                data = response.json()
                if data.get('success'):
                    print("✅ 四層分析功能正常")
                    # 檢查各層數據
                    layers = ['layer1_market_overview', 'layer2_sector_analysis', 
                             'layer3_trading_watchlist', 'layer4_options_strategies']
                    for layer in layers:
                        if layer in data:
                            print(f"   ✅ {layer} 數據完整")
                        else:
                            print(f"   ⚠️ {layer} 數據缺失")
                else:
                    print("⚠️ 四層分析返回錯誤")
            except json.JSONDecodeError:
                print("⚠️ 四層分析返回格式異常")
        else:
            print(f"❌ 四層分析端點失敗: {response.status_code}")
            if response.status_code == 500:
                print("   可能是依賴問題或代碼錯誤")
    except Exception as e:
        print(f"❌ 四層分析連接失敗: {str(e)}")
    
    print()
    print("📋 部署狀態總結:")
    print("1. 如果看到 '完整版' 或四層分析功能正常，部署成功")
    print("2. 如果仍顯示 '階段1'，請等待幾分鐘讓Railway完成部署")
    print("3. 如果持續失敗，可能需要檢查依賴或代碼問題")
    
    return True

if __name__ == "__main__":
    check_deployment_status()
    
    print("\n🔄 持續監控模式（每30秒檢查一次，按Ctrl+C停止）:")
    try:
        while True:
            time.sleep(30)
            print("\n" + "="*60)
            check_deployment_status()
    except KeyboardInterrupt:
        print("\n👋 監控結束") 