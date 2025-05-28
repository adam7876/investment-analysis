#!/usr/bin/env python3
"""
第一層數據收集器 - 總經與市場環境
整合所有總經數據源，提供統一的數據收集介面
"""

import time
import random
from datetime import datetime
from loguru import logger

from scrapers.alternative_fear_greed_scraper import AlternativeFearGreedScraper
from scrapers.macromicro_scraper import MacroMicroScraper
from scrapers.fred_api_scraper import FREDAPIScraper

class Layer1Collector:
    """第一層數據收集器"""
    
    def __init__(self):
        self.fear_greed_scraper = AlternativeFearGreedScraper()
        self.macromicro_scraper = MacroMicroScraper()
        self.fred_scraper = FREDAPIScraper()
    
    def collect_all_data(self):
        """收集所有第一層數據"""
        logger.info("🚀 開始收集第一層總經數據")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'layer': 'Layer 1 - 總經與市場環境',
            'data_sources': {},
            'analysis': {}
        }
        
        # 1. 收集 Fear & Greed Index
        logger.info("📊 收集市場情緒數據...")
        try:
            fear_greed_data = self.fear_greed_scraper.scrape()
            if fear_greed_data:
                results['data_sources']['fear_greed'] = fear_greed_data
                logger.info(f"✅ Fear & Greed Index: {fear_greed_data['index_value']} ({fear_greed_data['sentiment']})")
            else:
                logger.warning("⚠️ Fear & Greed Index 數據獲取失敗")
        except Exception as e:
            logger.error(f"❌ Fear & Greed Index 收集失敗: {str(e)}")
        
        # 隨機延遲
        time.sleep(random.uniform(1, 3))
        
        # 2. 收集 FRED 經濟數據
        logger.info("🏛️ 收集聯準會經濟數據...")
        try:
            fred_data = self.fred_scraper.scrape()
            if fred_data:
                results['data_sources']['fred'] = fred_data
                logger.info("✅ FRED 經濟數據收集成功")
            else:
                logger.warning("⚠️ FRED 經濟數據獲取失敗")
        except Exception as e:
            logger.error(f"❌ FRED 數據收集失敗: {str(e)}")
        
        # 隨機延遲
        time.sleep(random.uniform(2, 4))
        
        # 3. 收集 MacroMicro 數據（可選，因為可能會失敗）
        logger.info("📈 嘗試收集 MacroMicro 數據...")
        try:
            macromicro_data = self.macromicro_scraper.scrape()
            if macromicro_data:
                results['data_sources']['macromicro'] = macromicro_data
                logger.info("✅ MacroMicro 數據收集成功")
            else:
                logger.warning("⚠️ MacroMicro 數據獲取失敗（這是正常的，網站可能有反爬蟲機制）")
        except Exception as e:
            logger.warning(f"⚠️ MacroMicro 數據收集失敗: {str(e)}")
        
        # 4. 進行綜合分析
        logger.info("🧠 進行市場環境分析...")
        analysis = self._analyze_market_environment(results['data_sources'])
        results['analysis'] = analysis
        
        logger.info("✅ 第一層數據收集完成")
        return results
    
    def _analyze_market_environment(self, data_sources):
        """分析市場環境"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'market_sentiment': 'Unknown',
            'economic_phase': 'Unknown',
            'investment_recommendation': 'Unknown',
            'risk_level': 'Unknown',
            'key_factors': []
        }
        
        try:
            # 分析市場情緒
            if 'fear_greed' in data_sources:
                fg_data = data_sources['fear_greed']
                fg_value = fg_data['index_value']
                
                if fg_value <= 25:
                    analysis['market_sentiment'] = 'Extreme Fear'
                    analysis['investment_recommendation'] = '考慮逢低買入'
                    analysis['risk_level'] = 'High Opportunity'
                elif fg_value <= 45:
                    analysis['market_sentiment'] = 'Fear'
                    analysis['investment_recommendation'] = '謹慎樂觀'
                    analysis['risk_level'] = 'Medium'
                elif fg_value <= 55:
                    analysis['market_sentiment'] = 'Neutral'
                    analysis['investment_recommendation'] = '持續觀察'
                    analysis['risk_level'] = 'Medium'
                elif fg_value <= 75:
                    analysis['market_sentiment'] = 'Greed'
                    analysis['investment_recommendation'] = '注意風險'
                    analysis['risk_level'] = 'Medium-High'
                else:
                    analysis['market_sentiment'] = 'Extreme Greed'
                    analysis['investment_recommendation'] = '考慮獲利了結'
                    analysis['risk_level'] = 'High Risk'
                
                analysis['key_factors'].append(f"市場情緒指數: {fg_value} ({fg_data['sentiment']})")
            
            # 分析經濟基本面
            if 'fred' in data_sources:
                fred_data = data_sources['fred']
                
                # 分析失業率
                if 'unemployment' in fred_data and fred_data['unemployment']['value'] != '.':
                    unemployment = float(fred_data['unemployment']['value'])
                    if unemployment < 4:
                        analysis['key_factors'].append(f"失業率低 ({unemployment}%) - 經濟強勁")
                    elif unemployment > 6:
                        analysis['key_factors'].append(f"失業率高 ({unemployment}%) - 經濟疲軟")
                
                # 分析聯邦基金利率
                if 'fed_funds_rate' in fred_data and fred_data['fed_funds_rate']['value'] != '.':
                    fed_rate = float(fred_data['fed_funds_rate']['value'])
                    if fed_rate > 4:
                        analysis['key_factors'].append(f"高利率環境 ({fed_rate}%) - 緊縮政策")
                    elif fed_rate < 2:
                        analysis['key_factors'].append(f"低利率環境 ({fed_rate}%) - 寬鬆政策")
            
            # 綜合判斷經濟階段
            if len(analysis['key_factors']) > 0:
                if any('經濟強勁' in factor for factor in analysis['key_factors']):
                    if analysis['market_sentiment'] in ['Greed', 'Extreme Greed']:
                        analysis['economic_phase'] = '擴張後期 - 注意過熱'
                    else:
                        analysis['economic_phase'] = '健康擴張期'
                elif any('經濟疲軟' in factor for factor in analysis['key_factors']):
                    analysis['economic_phase'] = '衰退期或復甦初期'
                else:
                    analysis['economic_phase'] = '穩定期'
            
            # 如果沒有足夠數據，使用模擬分析
            if analysis['market_sentiment'] == 'Unknown':
                analysis['market_sentiment'] = 'Neutral (數據不足)'
                analysis['investment_recommendation'] = '等待更多數據'
                analysis['key_factors'].append('數據收集不完整，建議手動檢查數據源')
                
        except Exception as e:
            logger.error(f"市場環境分析失敗: {str(e)}")
            analysis['key_factors'].append(f'分析錯誤: {str(e)}')
        
        return analysis
    
    def get_summary_report(self):
        """獲取摘要報告"""
        data = self.collect_all_data()
        
        report = {
            'timestamp': data['timestamp'],
            'summary': {},
            'recommendations': [],
            'data_quality': {}
        }
        
        # 數據品質評估
        total_sources = 3  # fear_greed, fred, macromicro
        successful_sources = len(data['data_sources'])
        
        report['data_quality'] = {
            'total_sources': total_sources,
            'successful_sources': successful_sources,
            'success_rate': f"{(successful_sources/total_sources)*100:.1f}%",
            'available_data': list(data['data_sources'].keys())
        }
        
        # 摘要信息
        if 'fear_greed' in data['data_sources']:
            fg_data = data['data_sources']['fear_greed']
            report['summary']['market_sentiment'] = f"{fg_data['index_value']} ({fg_data['sentiment']})"
        
        if 'analysis' in data:
            analysis = data['analysis']
            report['summary']['economic_phase'] = analysis.get('economic_phase', 'Unknown')
            report['summary']['investment_recommendation'] = analysis.get('investment_recommendation', 'Unknown')
            report['summary']['risk_level'] = analysis.get('risk_level', 'Unknown')
            
            # 建議
            if analysis.get('investment_recommendation') != 'Unknown':
                report['recommendations'].append(analysis['investment_recommendation'])
            
            for factor in analysis.get('key_factors', []):
                report['recommendations'].append(factor)
        
        return report
    
    def close(self):
        """關閉所有資源"""
        try:
            self.fear_greed_scraper.__exit__(None, None, None)
            self.macromicro_scraper.close()
            self.fred_scraper.__exit__(None, None, None)
        except:
            pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def main():
    """主函數 - 演示用法"""
    with Layer1Collector() as collector:
        # 獲取完整數據
        full_data = collector.collect_all_data()
        
        print("\n" + "="*60)
        print("📊 第一層總經數據收集結果")
        print("="*60)
        
        # 顯示摘要報告
        summary = collector.get_summary_report()
        
        print(f"\n🕐 時間: {summary['timestamp'][:19]}")
        print(f"📈 市場情緒: {summary['summary'].get('market_sentiment', 'N/A')}")
        print(f"🏛️ 經濟階段: {summary['summary'].get('economic_phase', 'N/A')}")
        print(f"💡 投資建議: {summary['summary'].get('investment_recommendation', 'N/A')}")
        print(f"⚠️ 風險等級: {summary['summary'].get('risk_level', 'N/A')}")
        
        print(f"\n📊 數據品質:")
        print(f"   成功率: {summary['data_quality']['success_rate']}")
        print(f"   可用數據源: {', '.join(summary['data_quality']['available_data'])}")
        
        if summary['recommendations']:
            print(f"\n💡 關鍵因素:")
            for i, rec in enumerate(summary['recommendations'][:5], 1):
                print(f"   {i}. {rec}")

if __name__ == "__main__":
    main() 