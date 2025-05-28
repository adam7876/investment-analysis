#!/usr/bin/env python3
"""
測試改善後的整合分析系統
檢查推薦股票和詳細分析資訊
"""

import sys
import json
from loguru import logger
from integrated_analyzer import IntegratedAnalyzer

def test_improved_integrated_analysis():
    """測試改善後的整合分析系統"""
    try:
        logger.info("🔍 測試改善後的整合分析系統...")
        
        # 創建分析器
        analyzer = IntegratedAnalyzer()
        logger.info(f"✅ 分析器初始化成功，股票池大小: {len(analyzer.market_universe)}")
        
        # 設定用戶偏好
        user_preferences = {
            "risk_tolerance": "中等",
            "investment_amount": 50000,
            "time_horizon": "中期"
        }
        
        # 執行完整分析
        logger.info("🚀 開始執行完整的三層聯動分析...")
        result = analyzer.analyze_complete_flow(user_preferences)
        
        # 檢查結果結構
        logger.info("📊 檢查分析結果...")
        
        # 檢查第一層分析
        if 'layer1_analysis' in result:
            layer1 = result['layer1_analysis']
            logger.info(f"✅ 第一層分析完成")
            logger.info(f"   市場階段: {layer1.get('market_phase', 'N/A')}")
            logger.info(f"   風險偏好: {layer1.get('risk_appetite', 'N/A')}")
            logger.info(f"   信心度: {layer1.get('confidence_level', 'N/A')}%")
        else:
            logger.warning("❌ 第一層分析結果缺失")
        
        # 檢查第二層分析
        if 'layer2_analysis' in result:
            layer2 = result['layer2_analysis']
            selected_count = len(layer2.get('selected_stocks', []))
            logger.info(f"✅ 第二層分析完成，選出 {selected_count} 支候選股票")
            
            if selected_count > 0:
                # 顯示前3支候選股票
                for i, stock in enumerate(layer2['selected_stocks'][:3]):
                    logger.info(f"   候選股票 {i+1}: {stock['symbol']} - {stock['name']} (評分: {stock.get('total_score', 0)})")
            else:
                logger.warning("❌ 第二層沒有選出候選股票")
        else:
            logger.warning("❌ 第二層分析結果缺失")
        
        # 檢查第三層分析
        if 'layer3_analysis' in result:
            layer3 = result['layer3_analysis']
            final_count = len(layer3.get('final_recommendations', []))
            logger.info(f"✅ 第三層分析完成，最終推薦 {final_count} 支股票")
            
            if final_count > 0:
                # 顯示推薦股票詳情
                for i, stock in enumerate(layer3['final_recommendations']):
                    logger.info(f"   推薦股票 {i+1}: {stock['symbol']} - {stock['name']}")
                    logger.info(f"      最終評分: {stock.get('final_rating', 0)}")
                    logger.info(f"      技術評分: {stock.get('technical_score', 0)}")
                    logger.info(f"      信心度: {stock.get('confidence_level', 0)}%")
                    logger.info(f"      投資建議: {stock.get('investment_recommendation', {}).get('recommendation', 'N/A')}")
                    logger.info(f"      風險等級: {stock.get('risk_assessment', {}).get('risk_level', 'N/A')}")
                    logger.info(f"      進場時機: {stock.get('entry_timing', {}).get('timing_rating', 'N/A')}")
                    
                    # 檢查價格目標
                    if 'price_targets' in stock:
                        pt = stock['price_targets']
                        logger.info(f"      當前價格: ${pt.get('current_price', 'N/A')}")
                        logger.info(f"      目標價格: ${pt.get('conservative_target', 'N/A')}")
                        logger.info(f"      停損點: ${pt.get('stop_loss', 'N/A')}")
                    
                    # 檢查推薦理由
                    reasons = stock.get('investment_recommendation', {}).get('reasons', [])
                    if reasons:
                        logger.info(f"      推薦理由: {', '.join(reasons[:2])}")
                    
                    logger.info("")
            else:
                logger.warning("❌ 第三層沒有產生最終推薦")
        else:
            logger.warning("❌ 第三層分析結果缺失")
        
        # 檢查最終建議
        if 'final_recommendations' in result:
            final_recs = result['final_recommendations']
            top_picks = final_recs.get('top_picks', [])
            logger.info(f"✅ 最終建議包含 {len(top_picks)} 支頂級推薦")
            
            # 檢查執行摘要
            if 'summary' in result:
                summary = result['summary']
                logger.info(f"   總推薦數: {summary.get('total_recommendations', 0)}")
                logger.info(f"   強烈推薦數: {summary.get('strong_buy_count', 0)}")
                logger.info(f"   平均信心度: {summary.get('average_confidence', 0)}%")
                logger.info(f"   主要產業: {', '.join(summary.get('primary_sectors', []))}")
                logger.info(f"   關鍵訊息: {summary.get('key_message', 'N/A')}")
        else:
            logger.warning("❌ 最終建議結果缺失")
        
        # 檢查投資策略
        if 'investment_strategy' in result:
            strategy = result['investment_strategy']
            logger.info(f"✅ 投資策略: {strategy.get('primary_focus', 'N/A')}")
            logger.info(f"   策略類型: {strategy.get('strategy_type', 'N/A')}")
            logger.info(f"   風險水準: {strategy.get('risk_level', 'N/A')}")
        
        # 總結測試結果
        logger.info("📈 測試結果總結:")
        
        has_layer1 = 'layer1_analysis' in result
        has_layer2 = 'layer2_analysis' in result and len(result['layer2_analysis'].get('selected_stocks', [])) > 0
        has_layer3 = 'layer3_analysis' in result and len(result['layer3_analysis'].get('final_recommendations', [])) > 0
        has_final = 'final_recommendations' in result and len(result['final_recommendations'].get('top_picks', [])) > 0
        
        logger.info(f"   第一層分析: {'✅ 通過' if has_layer1 else '❌ 失敗'}")
        logger.info(f"   第二層選股: {'✅ 通過' if has_layer2 else '❌ 失敗'}")
        logger.info(f"   第三層確認: {'✅ 通過' if has_layer3 else '❌ 失敗'}")
        logger.info(f"   最終推薦: {'✅ 通過' if has_final else '❌ 失敗'}")
        
        if has_layer1 and has_layer2 and has_layer3 and has_final:
            logger.success("🎉 整合分析系統測試完全通過！")
            return True
        else:
            logger.error("❌ 整合分析系統測試部分失敗")
            return False
            
    except Exception as e:
        logger.error(f"測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_data_structure():
    """測試數據結構的完整性"""
    logger.info("🔍 測試數據結構完整性...")
    
    try:
        analyzer = IntegratedAnalyzer()
        
        # 測試單一股票分析
        test_symbols = ['AAPL', 'MSFT', 'GOOGL']
        
        for symbol in test_symbols:
            logger.info(f"測試股票: {symbol}")
            
            # 測試基本數據獲取
            import yfinance as yf
            stock = yf.Ticker(symbol)
            hist = stock.history(period="3mo")
            info = stock.info
            
            if len(hist) > 20:
                # 測試技術指標計算
                indicators = analyzer._calculate_comprehensive_technical_indicators(hist)
                logger.info(f"   技術指標: ✅")
                
                # 測試技術信號生成
                signals = analyzer._generate_comprehensive_technical_signals(indicators, hist)
                logger.info(f"   技術信號: ✅")
                
                # 測試技術評分
                tech_score = analyzer._calculate_comprehensive_technical_score(signals, indicators)
                logger.info(f"   技術評分: {tech_score}")
                
                # 測試詳細報告
                detailed_report = analyzer._generate_detailed_technical_report(hist, indicators, signals, tech_score)
                logger.info(f"   詳細報告: ✅")
                
            else:
                logger.warning(f"   {symbol} 數據不足")
        
        logger.success("✅ 數據結構測試通過")
        return True
        
    except Exception as e:
        logger.error(f"數據結構測試失敗: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 開始測試改善後的整合分析系統")
    
    # 測試數據結構
    structure_ok = test_data_structure()
    
    # 測試完整流程
    if structure_ok:
        analysis_ok = test_improved_integrated_analysis()
        
        if analysis_ok:
            logger.success("🎉 所有測試通過！系統已準備就緒")
            sys.exit(0)
        else:
            logger.error("❌ 分析流程測試失敗")
            sys.exit(1)
    else:
        logger.error("❌ 數據結構測試失敗")
        sys.exit(1) 