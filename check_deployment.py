#!/usr/bin/env python3
"""
Railway部署狀態檢查腳本
"""

import requests
import time
import json
from datetime import datetime

def check_railway_deployment(url):
    """檢查Railway部署狀態"""
    print(f"🔍 檢查Railway部署狀態...")
    print(f"📍 URL: {url}")
    print("-" * 50)
    
    endpoints = [
        ("/", "主頁面"),
        ("/health", "健康檢查"),
        ("/api/test", "API測試"),
        ("/api/market-data", "市場數據API")
    ]
    
    for endpoint, description in endpoints:
        try:
            full_url = f"{url}{endpoint}"
            print(f"🔗 測試 {description}: {full_url}")
            
            response = requests.get(full_url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {description} - 狀態碼: {response.status_code}")
                
                # 如果是JSON響應，顯示部分內容
                if 'application/json' in response.headers.get('content-type', ''):
                    try:
                        data = response.json()
                        if 'version' in data:
                            print(f"   📊 版本: {data.get('version')}")
                        if 'stage' in data:
                            print(f"   🎯 階段: {data.get('stage')}")
                        if 'message' in data:
                            print(f"   💬 訊息: {data.get('message')}")
                    except:
                        pass
                else:
                    # HTML響應，檢查標題
                    if "四層聯動美股投資分析系統" in response.text:
                        print(f"   📄 頁面標題正確")
                        
            else:
                print(f"❌ {description} - 狀態碼: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {description} - 連接錯誤: {str(e)}")
        
        print()
        time.sleep(1)
    
    print("=" * 50)
    print(f"⏰ 檢查完成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # 請替換為您的實際Railway URL
    railway_url = "https://your-app-name.railway.app"
    
    print("🚀 Railway部署狀態檢查工具")
    print("=" * 50)
    print("📝 請將下面的URL替換為您的實際Railway應用URL：")
    print(f"   {railway_url}")
    print()
    
    # 如果您有實際的URL，請取消註釋下面這行
    # check_railway_deployment(railway_url)
    
    print("💡 使用方法：")
    print("1. 在Railway控制台找到您的應用URL")
    print("2. 修改此腳本中的railway_url變量")
    print("3. 重新運行此腳本進行檢查") 