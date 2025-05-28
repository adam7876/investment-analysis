#!/usr/bin/env python3
"""
調試整合分析系統
找出沒有推薦股票的原因
"""

import sys
import traceback
from loguru import logger
from integrated_analyzer import IntegratedAnalyzer

def debug_integrated_analysis():
    """調試整合分析流程"""
    try:
        logger.info("🔍 開始調試整合分析系統...")
        
        # 創建分析器
        analyzer = IntegratedAnalyzer()
        logger.info(f"✅ 分析器初始化成功，股票池大小: {len(analyzer.market_universe)}")
        
        # 測試第一層分析
        logger.info("📊 測試第一層分析...")
        layer1_result = analyzer._analyze_macro_environment()
        logger.info(f"第一層結果: {layer1_result}")
        
        # 測試投資策略確定
        logger.info("🎯 測試投資策略確定...")
        strategy = analyzer._determine_investment_strategy(layer1_result)
        logger.info(f"投資策略: {strategy}")
        
        # 測試第二層選股（只測試少數股票）
        logger.info("🔍 測試第二層選股...")
        test_symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']
        
        for symbol in test_symbols:
            try:
                logger.info(f"分析股票: {symbol}")
                stock_data = analyzer._analyze_single_stock(symbol, strategy['screening_criteria'], strategy)
                if stock_data:
                    logger.info(f"{symbol} 分析結果: 評分={stock_data['total_score']}, 通過篩選={stock_data['passes_screening']}")
                    logger.info(f"評分詳情: {stock_data['score_breakdown']}")
                else:
                    logger.warning(f"{symbol} 分析失敗或數據不足")
            except Exception as e:
                logger.error(f"分析 {symbol} 時發生錯誤: {str(e)}")
                traceback.print_exc()
        
        # 測試完整流程
        logger.info("🚀 測試完整流程...")
        result = analyzer.analyze_complete_flow()
        
        if result.get('success'):
            logger.info("✅ 完整分析成功")
            
            # 檢查推薦股票
            top_picks = result.get('final_recommendations', {}).get('top_picks', [])
            logger.info(f"推薦股票數量: {len(top_picks)}")
            
            if top_picks:
                for i, stock in enumerate(top_picks):
                    logger.info(f"推薦股票 {i+1}: {stock.get('symbol')} (評分: {stock.get('total_score')})")
            else:
                logger.warning("❌ 沒有推薦股票！")
                
                # 檢查第二層結果
                layer2_stocks = result.get('layer2_analysis', {}).get('selected_stocks', [])
                logger.info(f"第二層篩選出的股票數量: {len(layer2_stocks)}")
                
                # 檢查第三層結果
                layer3_stocks = result.get('layer3_analysis', {}).get('confirmed_stocks', [])
                logger.info(f"第三層確認的股票數量: {len(layer3_stocks)}")
                
        else:
            logger.error(f"❌ 完整分析失敗: {result.get('error')}")
            
    except Exception as e:
        logger.error(f"調試過程中發生錯誤: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_integrated_analysis() 