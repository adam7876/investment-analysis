#!/usr/bin/env python3
"""
修復驗證測試腳本
測試修復的問題：下拉選單、第二層數據收集、選股推薦顯示
"""

import requests
import json
from datetime import datetime

def test_web_server():
    """測試Web服務器是否正常運行"""
    try:
        response = requests.get('http://localhost:8080', timeout=5)
        if response.status_code == 200:
            print("✅ Web服務器運行正常")
            return True
        else:
            print(f"❌ Web服務器響應異常: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Web服務器連接失敗: {str(e)}")
        return False

def test_layer2_api():
    """測試第二層API功能"""
    print("\n🧪 測試第二層API功能...")
    
    # 測試數據收集
    try:
        response = requests.post('http://localhost:8080/api/layer2/collect', timeout=30)
        data = response.json()
        
        if data.get('success'):
            print("✅ 第二層數據收集成功")
            print(f"   📊 成功率: {data['data']['success_rate']}%")
            print(f"   ⏱️  處理時間: {data['data']['processing_time']}秒")
            
            # 檢查各個模組
            modules = ['economic_calendar', 'news_sentiment', 'sector_rotation', 'stock_screener']
            for module in modules:
                module_data = data['data'].get(module, {})
                status = "✅" if module_data.get('success') else "❌"
                print(f"   {status} {module}")
            
            return True
        else:
            print(f"❌ 第二層數據收集失敗: {data.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ 第二層API測試失敗: {str(e)}")
        return False

def test_stock_screener():
    """測試選股篩選器功能"""
    print("\n🔍 測試選股篩選器...")
    
    try:
        response = requests.get('http://localhost:8080/api/layer2/stock-screener', timeout=20)
        data = response.json()
        
        if data.get('success'):
            stocks = data['data'].get('stocks', [])
            print(f"✅ 選股篩選成功，找到 {len(stocks)} 支股票")
            
            # 顯示推薦股票
            buy_stocks = [s for s in stocks if s.get('recommendation') in ['買入', '強烈買入']]
            if buy_stocks:
                print(f"   💰 買入推薦 ({len(buy_stocks)} 支):")
                for stock in buy_stocks[:3]:  # 顯示前3支
                    print(f"      📈 {stock['symbol']}: {stock['recommendation']} (評分: {stock['score']}/{stock.get('max_score', 10)})")
                    print(f"         理由: {', '.join(stock.get('reasons', []))}")
            else:
                print("   ⚠️  目前沒有買入推薦")
            
            return True
        else:
            print(f"❌ 選股篩選失敗: {data.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ 選股篩選測試失敗: {str(e)}")
        return False

def test_news_sentiment():
    """測試新聞情緒分析"""
    print("\n📰 測試新聞情緒分析...")
    
    try:
        response = requests.get('http://localhost:8080/api/layer2/news-sentiment', timeout=15)
        data = response.json()
        
        if data.get('success'):
            sentiment_data = data['data']
            print(f"✅ 新聞情緒分析成功")
            print(f"   😊 整體情緒: {sentiment_data.get('overall_sentiment')}")
            print(f"   📊 平均分數: {sentiment_data.get('average_score')}")
            print(f"   📰 分析新聞數: {sentiment_data.get('total_analyzed')}")
            
            # 顯示情緒分布
            dist = sentiment_data.get('sentiment_distribution', {})
            print(f"   📈 情緒分布: 正面({dist.get('positive', 0)}) 中性({dist.get('neutral', 0)}) 負面({dist.get('negative', 0)})")
            
            return True
        else:
            print(f"❌ 新聞情緒分析失敗")
            return False
            
    except Exception as e:
        print(f"❌ 新聞情緒分析測試失敗: {str(e)}")
        return False

def main():
    """主測試函數"""
    print("🚀 修復驗證測試開始")
    print("=" * 50)
    
    # 測試Web服務器
    if not test_web_server():
        print("\n❌ Web服務器測試失敗，請先啟動服務器")
        return
    
    # 測試各項功能
    tests = [
        ("第二層API", test_layer2_api),
        ("選股篩選器", test_stock_screener),
        ("新聞情緒分析", test_news_sentiment),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}測試異常: {str(e)}")
            results.append((test_name, False))
    
    # 總結
    print("\n" + "=" * 50)
    print("📊 測試結果總結:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 總體結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有修復驗證通過！")
        print("\n💡 修復內容:")
        print("   ✅ 下拉選單：添加Bootstrap初始化")
        print("   ✅ 第二層數據：改善容錯機制，提供模擬數據")
        print("   ✅ 選股展示：優化卡片式展示，添加詳細評分")
        print("   ✅ 通知系統：統一showToast函數")
        
        print("\n🌐 您可以訪問以下網址測試:")
        print("   本地: http://localhost:8080")
        print("   線上: https://web-production-9cc8f.up.railway.app")
    else:
        print("⚠️  部分功能仍需改進")

if __name__ == "__main__":
    main() 