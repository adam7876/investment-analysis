#!/usr/bin/env python3
"""
第一層測試腳本 - 總經與市場環境數據收集
測試 Alternative.me Fear & Greed Index API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.logger import logger
from scrapers.alternative_fear_greed_scraper import AlternativeFearGreedScraper

def test_alternative_fear_greed():
    """測試 Alternative.me Fear & Greed Index API"""
    logger.info("=" * 50)
    logger.info("開始測試 Alternative.me Fear & Greed Index API")
    logger.info("=" * 50)
    
    try:
        with AlternativeFearGreedScraper() as scraper:
            # 測試基本數據獲取
            result = scraper.scrape()
            
            if result:
                logger.info("✅ Alternative.me Fear & Greed Index API 測試成功")
                logger.info(f"📊 指數值: {result['index_value']}")
                logger.info(f"📝 指數描述: {result['index_text']}")
                logger.info(f"😱 市場情緒: {result['sentiment']}")
                logger.info(f"⏰ 時間戳: {result['timestamp']}")
                logger.info(f"🔄 下次更新: {result.get('time_until_update', 'N/A')} 秒")
                
                # 驗證數據合理性
                if 0 <= result['index_value'] <= 100:
                    logger.info("✅ 指數值在合理範圍內 (0-100)")
                else:
                    logger.warning(f"⚠️ 指數值異常: {result['index_value']}")
                
                # 測試趨勢分析
                logger.info("\n📈 測試趨勢分析功能...")
                trend_analysis = scraper.analyze_trend(7)
                
                if trend_analysis:
                    logger.info("✅ 趨勢分析成功")
                    logger.info(f"📊 當前值: {trend_analysis['current_value']}")
                    logger.info(f"📈 趨勢: {trend_analysis['trend']}")
                    logger.info(f"📊 變化: {trend_analysis['change']} ({trend_analysis['change_percent']}%)")
                    logger.info(f"📊 平均值: {trend_analysis['average_value']}")
                else:
                    logger.warning("⚠️ 趨勢分析失敗")
                
                return True
            else:
                logger.error("❌ Alternative.me Fear & Greed Index API 測試失敗 - 無數據返回")
                return False
                
    except Exception as e:
        logger.error(f"❌ Alternative.me Fear & Greed Index API 測試失敗: {str(e)}")
        return False

def test_historical_data():
    """測試歷史數據獲取"""
    logger.info("=" * 50)
    logger.info("開始測試歷史數據獲取")
    logger.info("=" * 50)
    
    try:
        with AlternativeFearGreedScraper() as scraper:
            historical_data = scraper.get_historical_data(5)
            
            if historical_data and len(historical_data) > 0:
                logger.info(f"✅ 歷史數據獲取成功，共 {len(historical_data)} 筆數據")
                
                # 顯示最近3天的數據
                for i, data in enumerate(historical_data[:3]):
                    logger.info(f"📅 {data['date'][:10]}: {data['index_value']} ({data['sentiment']})")
                
                return True
            else:
                logger.error("❌ 歷史數據獲取失敗")
                return False
                
    except Exception as e:
        logger.error(f"❌ 歷史數據測試失敗: {str(e)}")
        return False

def main():
    """主測試函數"""
    logger.info("🚀 開始第一層功能測試 - Alternative.me API 版本")
    
    # 測試結果統計
    test_results = []
    
    # 測試 Alternative.me Fear & Greed Index API
    test_results.append(("Alternative.me Fear & Greed Index", test_alternative_fear_greed()))
    
    # 測試歷史數據功能
    test_results.append(("歷史數據獲取", test_historical_data()))
    
    # 輸出測試結果摘要
    logger.info("\n" + "=" * 50)
    logger.info("📋 第一層測試結果摘要")
    logger.info("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通過" if result else "❌ 失敗"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\n📊 測試統計: {passed}/{total} 通過")
    
    if passed == total:
        logger.info("🎉 第一層所有測試通過！可以進行下一層開發")
        logger.info("💡 Alternative.me API 運行穩定，數據品質良好")
    else:
        logger.warning("⚠️ 部分測試失敗，請檢查並修復問題")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 