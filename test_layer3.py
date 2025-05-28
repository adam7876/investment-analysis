#!/usr/bin/env python3
"""
第三層功能測試腳本
測試技術分析和風險管理功能
"""

import sys
import time
from datetime import datetime
from layer3_collector import Layer3Collector

def test_technical_analysis():
    """測試技術分析功能"""
    print("🧪 測試技術分析功能...")
    
    try:
        collector = Layer3Collector()
        result = collector.get_technical_analysis()
        
        if result.get('success'):
            analysis = result.get('analysis', [])
            print(f"✅ 技術分析成功，分析了 {len(analysis)} 支股票")
            
            for stock in analysis[:3]:  # 顯示前3支股票
                symbol = stock['symbol']
                signal = stock['trading_signals']['overall_signal']
                confidence = stock['trading_signals']['confidence']
                rsi = stock['indicators']['rsi']
                
                print(f"   📈 {symbol}: {signal} (信心度: {confidence}%, RSI: {rsi:.1f})")
            
            return True
        else:
            print(f"❌ 技術分析失敗")
            return False
            
    except Exception as e:
        print(f"❌ 技術分析測試異常: {str(e)}")
        return False

def test_risk_management():
    """測試風險管理功能"""
    print("\n🛡️ 測試風險管理功能...")
    
    try:
        collector = Layer3Collector()
        result = collector.get_risk_management()
        
        if result.get('success'):
            risk_analysis = result.get('risk_analysis', [])
            portfolio_advice = result.get('portfolio_advice', {})
            
            print(f"✅ 風險管理分析成功，分析了 {len(risk_analysis)} 支股票")
            print(f"   📊 投資組合風險等級: {portfolio_advice.get('risk_level', 'N/A')}")
            
            for stock in risk_analysis:
                symbol = stock['symbol']
                risk_level = stock['risk_metrics']['risk_level']
                volatility = stock['risk_metrics']['volatility']
                
                print(f"   🎯 {symbol}: {risk_level} (波動率: {volatility:.1f}%)")
            
            return True
        else:
            print(f"❌ 風險管理分析失敗")
            return False
            
    except Exception as e:
        print(f"❌ 風險管理測試異常: {str(e)}")
        return False

def test_full_layer3_collection():
    """測試完整的第三層數據收集"""
    print("\n🚀 測試完整第三層數據收集...")
    
    try:
        collector = Layer3Collector()
        start_time = time.time()
        
        result = collector.collect_all_data()
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        success_rate = result.get('success_rate', 0)
        summary = result.get('summary', {})
        
        print(f"✅ 第三層數據收集完成")
        print(f"   ⏱️  處理時間: {processing_time:.2f} 秒")
        print(f"   📊 成功率: {success_rate}%")
        print(f"   🎯 強勢信號: {summary.get('strong_signals', 0)} 個")
        print(f"   📈 平均信心度: {summary.get('avg_confidence', 0)}%")
        print(f"   ⚠️  高風險股票: {summary.get('high_risk_stocks', 0)} 支")
        
        return True
        
    except Exception as e:
        print(f"❌ 完整數據收集測試失敗: {str(e)}")
        return False

def test_summary_report():
    """測試摘要報告生成"""
    print("\n📋 測試摘要報告生成...")
    
    try:
        collector = Layer3Collector()
        summary = collector.get_summary_report()
        
        print(f"✅ 摘要報告生成成功")
        print(f"   📊 層級: {summary.get('layer', 'N/A')}")
        print(f"   📈 成功率: {summary.get('success_rate', 0)}%")
        
        insights = summary.get('key_insights', {})
        print(f"   🎯 強勢信號: {insights.get('strong_signals', 0)} 個")
        print(f"   💡 投資建議: {insights.get('investment_advice', 'N/A')}")
        print(f"   📊 操作等級: {insights.get('action_level', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ 摘要報告測試失敗: {str(e)}")
        return False

def main():
    """主測試函數"""
    print("🚀 美股投資分析系統 - 第三層功能測試")
    print("=" * 60)
    print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 執行各項測試
    tests = [
        ("技術分析", test_technical_analysis),
        ("風險管理", test_risk_management),
        ("完整數據收集", test_full_layer3_collection),
        ("摘要報告", test_summary_report),
    ]
    
    results = []
    total_start_time = time.time()
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}測試異常: {str(e)}")
            results.append((test_name, False))
    
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    
    # 顯示測試結果
    print("\n" + "=" * 60)
    print("📊 測試結果總結:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 總體結果: {passed}/{len(results)} 通過")
    print(f"⏱️  總測試時間: {total_time:.2f} 秒")
    
    if passed == len(results):
        print("🎉 所有第三層功能測試通過！")
        print("\n💡 第三層功能特色:")
        print("   ✅ 深度技術分析：RSI、MACD、布林帶等指標")
        print("   ✅ 支撐阻力位識別：關鍵價位分析")
        print("   ✅ 交易信號生成：綜合多指標判斷")
        print("   ✅ 風險管理：波動率、VaR、Beta分析")
        print("   ✅ 投資組合建議：持倉比例和停損策略")
        return True
    else:
        print("⚠️  部分功能需要改進")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 