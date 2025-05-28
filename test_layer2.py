#!/usr/bin/env python3
"""
第二層功能測試腳本
測試事件與產業選股功能
"""

import sys
import json
from datetime import datetime
from loguru import logger

from layer2_collector import Layer2Collector

def test_layer2_functions():
    """測試第二層所有功能"""
    
    print("🚀 美股投資分析系統 - 第二層功能測試")
    print("=" * 60)
    
    collector = Layer2Collector()
    
    # 測試各個功能
    tests = [
        ("財經事件日曆", collector.get_economic_calendar),
        ("新聞情緒分析", collector.get_news_sentiment),
        ("產業輪動分析", collector.get_sector_rotation),
        ("選股篩選器", collector.get_stock_screener),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n📊 測試 {test_name}...")
        try:
            result = test_func()
            if result.get("success", False):
                print(f"✅ {test_name} - 成功")
                if test_name == "財經事件日曆":
                    print(f"   📅 找到 {result.get('total_events', 0)} 個即將事件")
                elif test_name == "新聞情緒分析":
                    print(f"   📰 分析 {result.get('total_analyzed', 0)} 篇新聞")
                    print(f"   😊 整體情緒: {result.get('overall_sentiment', '未知')}")
                elif test_name == "產業輪動分析":
                    print(f"   🏭 分析 {result.get('total_sectors', 0)} 個產業")
                    if result.get('analysis'):
                        print(f"   📈 市場趨勢: {result['analysis'].get('trend', '未知')}")
                elif test_name == "選股篩選器":
                    print(f"   🔍 篩選 {result.get('total_analyzed', 0)} 支股票")
                    print(f"   💰 買入建議: {result.get('buy_recommendations', 0)} 支")
            else:
                print(f"❌ {test_name} - 失敗: {result.get('error', '未知錯誤')}")
            
            results[test_name] = result
            
        except Exception as e:
            print(f"❌ {test_name} - 異常: {str(e)}")
            results[test_name] = {"success": False, "error": str(e)}
    
    # 測試完整數據收集
    print(f"\n🔄 測試完整數據收集...")
    try:
        full_data = collector.collect_all_data()
        print(f"✅ 完整數據收集 - 成功")
        print(f"   ⏱️  處理時間: {full_data.get('processing_time', 0)} 秒")
        print(f"   📊 成功率: {full_data.get('success_rate', 0)}%")
        
        # 測試摘要報告
        summary = collector.get_summary_report()
        print(f"\n📋 摘要報告:")
        print(f"   市場情緒: {summary['key_insights']['market_sentiment']}")
        print(f"   產業趨勢: {summary['key_insights']['sector_trend']}")
        print(f"   投資建議: {summary['key_insights']['investment_advice']}")
        print(f"   風險等級: {summary['key_insights']['risk_level']}")
        
    except Exception as e:
        print(f"❌ 完整數據收集 - 異常: {str(e)}")
    
    # 計算總體成功率
    successful_tests = sum(1 for result in results.values() if result.get("success", False))
    total_tests = len(results)
    overall_success_rate = (successful_tests / total_tests) * 100
    
    print(f"\n" + "=" * 60)
    print(f"📊 測試結果總結:")
    print(f"   成功測試: {successful_tests}/{total_tests}")
    print(f"   總體成功率: {overall_success_rate:.1f}%")
    
    if overall_success_rate >= 75:
        print(f"🎉 第二層功能測試通過！")
        return True
    else:
        print(f"⚠️  第二層功能需要改進")
        return False

def main():
    """主函數"""
    try:
        # 設置日誌
        logger.remove()
        logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss} | {level} | {message}")
        
        # 執行測試
        success = test_layer2_functions()
        
        if success:
            print(f"\n✅ 第二層功能已準備就緒！")
            print(f"💡 您現在可以在Web介面中使用第二層功能")
        else:
            print(f"\n⚠️  部分功能可能不穩定，但基本功能可用")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print(f"\n⏹️  測試被用戶中斷")
        return 1
    except Exception as e:
        print(f"\n❌ 測試過程發生錯誤: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main()) 