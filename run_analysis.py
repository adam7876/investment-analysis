#!/usr/bin/env python3
"""
四層聯動美股投資分析 - 完整分析腳本
"""

from integrated_analyzer import IntegratedAnalyzer
import json
from datetime import datetime

def main():
    print("🚀 開始執行四層聯動美股投資分析...")
    print("=" * 60)
    
    # 創建分析器實例
    analyzer = IntegratedAnalyzer()
    
    try:
        # 執行完整四層分析
        result = analyzer.analyze_complete_flow()
        
        if result and result.get('success'):
            # 第一層：市場總觀
            print("\n🌍 第一層：市場總觀趨勢分析")
            print("-" * 40)
            if 'layer1_market_overview' in result:
                layer1 = result['layer1_market_overview']
                if 'market_sentiment' in layer1:
                    sentiment = layer1['market_sentiment']
                    print(f"📈 市場情緒：{sentiment.get('sentiment', 'N/A')}")
                    print(f"😨 恐懼貪婪指數：{sentiment.get('fear_greed_index', 'N/A')}")
                
                if 'economic_environment' in layer1:
                    econ = layer1['economic_environment']
                    print(f"💰 GDP成長率：{econ.get('gdp_growth', 'N/A')}%")
                    print(f"📊 通膨率：{econ.get('inflation_rate', 'N/A')}%")
                    print(f"🏦 失業率：{econ.get('unemployment_rate', 'N/A')}%")
                
                if 'overall_outlook' in layer1:
                    print(f"🔮 市場展望：{layer1['overall_outlook']}")
            
            # 第二層：產業分析
            print("\n🏭 第二層：本週觀察產業與催化劑")
            print("-" * 40)
            if 'layer2_sector_analysis' in result:
                layer2 = result['layer2_sector_analysis']
                if 'focus_sectors' in layer2:
                    for i, sector in enumerate(layer2['focus_sectors'][:5], 1):
                        name = sector.get('name', 'N/A')
                        reason = sector.get('reason', 'N/A')
                        print(f"🎯 {i}. {name}: {reason}")
                
                if 'investment_themes' in layer2:
                    themes = layer2['investment_themes']
                    if themes:
                        print(f"💡 投資主題：{', '.join(themes[:3])}")
            
            # 第三層：精選名單
            print("\n📈 第三層：精選操作名單")
            print("-" * 40)
            if 'layer3_trading_watchlist' in result:
                layer3 = result['layer3_trading_watchlist']
                if 'watchlist' in layer3:
                    for i, stock in enumerate(layer3['watchlist'][:8], 1):
                        symbol = stock.get('symbol', 'N/A')
                        price = stock.get('current_price', 'N/A')
                        score = stock.get('total_score', 'N/A')
                        sector = stock.get('sector', 'N/A')
                        print(f"💎 {i}. {symbol} ({sector}): ${price} 評分: {score}")
            
            # 第四層：選擇權策略
            print("\n🎲 第四層：選擇權策略建議")
            print("-" * 40)
            if 'layer4_options_strategies' in result:
                layer4 = result['layer4_options_strategies']
                if 'recommended_strategies' in layer4:
                    for i, strategy in enumerate(layer4['recommended_strategies'][:3], 1):
                        strategy_type = strategy.get('type', 'N/A')
                        description = strategy.get('description', 'N/A')
                        print(f"📊 {i}. {strategy_type}: {description}")
                
                if 'volatility_environment' in layer4:
                    vol_env = layer4['volatility_environment']
                    print(f"📈 波動率環境：{vol_env.get('level', 'N/A')}")
            
            # AI整合建議
            print("\n🤖 AI整合投資建議")
            print("=" * 40)
            
            # 最終建議
            if 'final_recommendations' in result:
                recommendations = result['final_recommendations']
                
                # 推薦投資標的
                if 'top_picks' in recommendations:
                    print("📋 推薦投資標的：")
                    for i, stock in enumerate(recommendations['top_picks'][:5], 1):
                        symbol = stock.get('symbol', 'N/A')
                        sector = stock.get('sector', 'N/A')
                        reason = stock.get('recommendation_reason', '綜合評分優秀')
                        confidence = stock.get('confidence_level', 'N/A')
                        print(f"{i}. {symbol} ({sector})")
                        print(f"   💡 推薦原因：{reason}")
                        print(f"   📊 信心水準：{confidence}")
                        print()
                
                # 投資策略建議
                if 'strategy_recommendations' in recommendations:
                    strategy_rec = recommendations['strategy_recommendations']
                    print("💡 投資策略建議：")
                    for rec in strategy_rec[:4]:
                        print(f"• {rec}")
                
                # 風險提醒
                if 'risk_warnings' in recommendations:
                    risk_warnings = recommendations['risk_warnings']
                    print("\n⚠️ 風險提醒：")
                    for warning in risk_warnings[:3]:
                        print(f"• {warning}")
            
            # 執行摘要
            if 'executive_summary' in result:
                summary = result['executive_summary']
                print(f"\n📝 執行摘要：")
                print(f"市場環境：{summary.get('market_environment', 'N/A')}")
                print(f"投資建議：{summary.get('investment_recommendation', 'N/A')}")
                print(f"關鍵訊息：{summary.get('key_message', 'N/A')}")
                
        else:
            print("❌ 分析失敗，請檢查系統狀態")
            if result and 'error' in result:
                print(f"錯誤訊息：{result['error']}")
                
    except Exception as e:
        print(f"❌ 執行分析時發生錯誤：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 