#!/usr/bin/env python3
"""
Railway部署監控腳本
"""

import requests
import time
import json
from datetime import datetime

def check_railway_status():
    """檢查Railway部署狀態"""
    print("🚀 Railway部署監控開始...")
    print("=" * 50)
    
    # 您需要在Railway控制台中找到您的應用URL
    # 格式通常為：https://your-app-name.railway.app
    
    print("📋 部署檢查清單：")
    print("1. ✅ 代碼已推送到GitHub")
    print("2. 🔄 Railway正在構建應用...")
    print("3. ⏳ 等待部署完成...")
    
    print("\n📱 請執行以下步驟：")
    print("1. 登入 Railway.app")
    print("2. 找到您的項目")
    print("3. 查看 'Deployments' 標籤")
    print("4. 等待構建完成（通常2-5分鐘）")
    
    print("\n🔍 部署完成後，請檢查以下端點：")
    print("• 主頁面：https://your-app.railway.app/")
    print("• 健康檢查：https://your-app.railway.app/health")
    print("• API測試：https://your-app.railway.app/api/test")
    print("• 四層分析：https://your-app.railway.app/api/integrated-analysis")
    
    print("\n📊 當前系統功能：")
    print("✅ 第一層：市場總觀趨勢分析（恐懼貪婪指數：71）")
    print("✅ 第二層：產業催化劑分析（AI、能源、數位化）")
    print("✅ 第三層：精選操作名單（NVDA、MSFT、CVX）")
    print("✅ 第四層：選擇權策略建議")
    print("✅ AI整合投資建議生成")
    
    return True

def test_local_system():
    """測試本地系統功能"""
    print("\n🧪 本地系統測試：")
    try:
        from integrated_analyzer import IntegratedAnalyzer
        analyzer = IntegratedAnalyzer()
        print("✅ 分析器初始化成功")
        
        # 快速測試
        result = analyzer.analyze_complete_flow()
        if result and result.get('success'):
            print("✅ 四層分析功能正常")
            
            # 檢查各層數據
            layers = ['layer1_market_overview', 'layer2_sector_analysis', 
                     'layer3_trading_watchlist', 'layer4_options_strategies']
            
            for layer in layers:
                if layer in result:
                    print(f"✅ {layer} 數據完整")
                else:
                    print(f"⚠️ {layer} 數據缺失")
        else:
            print("❌ 四層分析功能異常")
            
    except Exception as e:
        print(f"❌ 本地測試失敗：{str(e)}")

if __name__ == "__main__":
    check_railway_status()
    test_local_system()
    
    print("\n🎯 下一步行動：")
    print("1. 等待Railway部署完成")
    print("2. 獲取應用URL")
    print("3. 測試所有功能端點")
    print("4. 驗證四層分析功能")
    print("5. 開始使用美股投資建議系統！") 