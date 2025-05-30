#!/usr/bin/env python3
"""
增強版第一層數據收集器
整合改進版數據收集器，保持API兼容性，大幅提升數據準確性
"""

import sys
import os
from datetime import datetime
from typing import Dict, Any, List
from loguru import logger

# 添加項目路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 導入改進版數據收集器
from scrapers.improved_data_collector import ImprovedDataCollector

class EnhancedLayer1Collector:
    """增強版第一層收集器"""
    
    def __init__(self):
        self.collector = ImprovedDataCollector()
        logger.info("🚀 初始化增強版第一層數據收集器")
    
    def collect_all_data(self) -> Dict[str, Any]:
        """
        收集所有第一層數據
        保持與原有API的兼容性，但使用改進版數據收集器
        """
        logger.info("🚀 開始收集第一層總經數據（增強版）")
        
        try:
            # 使用改進版收集器獲取所有數據
            enhanced_data = self.collector.collect_all_data()
            
            # 轉換為原有API格式，保持兼容性
            compatible_result = self._convert_to_compatible_format(enhanced_data)
            
            logger.info(f"✅ 增強版第一層數據收集完成 - 可靠性: {enhanced_data['overall_reliability']}%")
            
            return compatible_result
            
        except Exception as e:
            logger.error(f"❌ 增強版數據收集失敗: {str(e)}")
            # 返回兼容格式的錯誤結果
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'data': {},
                'analysis': {
                    'market_environment': 'Unknown',
                    'investment_recommendation': 'Neutral',
                    'confidence_level': 0
                }
            }
    
    def _convert_to_compatible_format(self, enhanced_data: Dict) -> Dict[str, Any]:
        """將增強版數據轉換為與原有API兼容的格式"""
        
        # 提取關鍵數據
        fear_greed_data = enhanced_data['data']['fear_greed_index']
        market_data = enhanced_data['data']['market_data']
        economic_data = enhanced_data['data']['economic_indicators']
        sentiment_data = enhanced_data['data']['news_sentiment']
        market_sentiment = enhanced_data['analysis']['market_sentiment']
        
        # 構建兼容格式
        compatible_data = {
            'success': True,
            'timestamp': enhanced_data['collection_timestamp'],
            'collection_time': enhanced_data['collection_time'],
            'overall_reliability': enhanced_data['overall_reliability'],
            'data_quality': enhanced_data['analysis']['data_quality'],
            
            # 原有格式的數據結構
            'data': {
                # Fear & Greed Index（保持原格式）
                'fear_greed': {
                    'success': fear_greed_data['success'],
                    'value': fear_greed_data['data'].get('value', 50) if fear_greed_data['success'] else 50,
                    'classification': fear_greed_data['data'].get('classification', 'Neutral') if fear_greed_data['success'] else 'Neutral',
                    'reliability': fear_greed_data['reliability']
                },
                
                # 市場數據（轉換格式）
                'market_indices': self._convert_market_data(market_data),
                
                # 經濟指標（轉換格式）
                'economic_indicators': self._convert_economic_data(economic_data),
                
                # 新聞情緒（新增）
                'news_sentiment': {
                    'success': sentiment_data['success'],
                    'sentiment_score': sentiment_data['data'].get('average_sentiment', 0) if sentiment_data['success'] else 0,
                    'sentiment_label': sentiment_data['data'].get('sentiment_label', 'Neutral') if sentiment_data['success'] else 'Neutral',
                    'reliability': sentiment_data['reliability']
                }
            },
            
            # 分析結果（增強版）
            'analysis': {
                'market_environment': self._determine_market_environment(market_sentiment),
                'investment_recommendation': self._generate_investment_recommendation(market_sentiment),
                'confidence_level': market_sentiment['confidence'],
                'market_sentiment': market_sentiment,
                'key_factors': self._extract_key_factors(enhanced_data),
                'risk_assessment': self._assess_risk_level(market_sentiment, enhanced_data['overall_reliability'])
            },
            
            # 增強信息
            'enhancement_info': {
                'version': '2.0_enhanced',
                'successful_sources': enhanced_data['successful_sources'],
                'total_sources': enhanced_data['total_sources'],
                'data_coverage': f"{enhanced_data['successful_sources']}/{enhanced_data['total_sources']} ({enhanced_data['successful_sources']/enhanced_data['total_sources']*100:.1f}%)"
            }
        }
        
        return compatible_data
    
    def _convert_market_data(self, market_data: Dict) -> Dict:
        """轉換市場數據格式"""
        if not market_data['success']:
            return {'success': False, 'data': {}}
        
        converted = {
            'success': True,
            'reliability': market_data['reliability'],
            'data': {}
        }
        
        # 轉換各個指數數據
        for symbol, data in market_data['data'].items():
            # 標準化符號名稱
            if symbol == '^GSPC':
                key = 'sp500'
            elif symbol == '^DJI':
                key = 'dow_jones'
            elif symbol == '^IXIC':
                key = 'nasdaq'
            elif symbol == '^VIX':
                key = 'vix'
            else:
                key = symbol.replace('^', '').lower()
            
            converted['data'][key] = {
                'current_price': data['current_price'],
                'change': data['change'],
                'change_percent': data['change_percent'],
                'volume': data.get('volume', 0),
                'name': data.get('name', symbol)
            }
        
        return converted
    
    def _convert_economic_data(self, economic_data: Dict) -> Dict:
        """轉換經濟指標格式"""
        if not economic_data['success']:
            return {'success': False, 'data': {}}
        
        converted = {
            'success': True,
            'reliability': economic_data['reliability'],
            'data': {}
        }
        
        # 轉換各個經濟指標
        for indicator, data in economic_data['data'].items():
            converted['data'][indicator] = {
                'current_value': data.get('current_value') or data.get('current_price') or data.get('current_yield'),
                'change': data.get('change', 0),
                'change_percent': data.get('change_percent', 0),
                'name': data.get('name', indicator)
            }
        
        return converted
    
    def _determine_market_environment(self, market_sentiment: Dict) -> str:
        """根據市場情緒確定市場環境"""
        sentiment_label = market_sentiment['sentiment_label']
        
        if sentiment_label == 'Bullish':
            return 'Bull Market'
        elif sentiment_label == 'Slightly Bullish':
            return 'Mild Bull Market'
        elif sentiment_label == 'Neutral':
            return 'Sideways Market'
        elif sentiment_label == 'Slightly Bearish':
            return 'Mild Bear Market'
        else:
            return 'Bear Market'
    
    def _generate_investment_recommendation(self, market_sentiment: Dict) -> str:
        """生成投資建議"""
        sentiment_score = market_sentiment['overall_score']
        confidence = market_sentiment['confidence']
        
        if sentiment_score > 0.2 and confidence >= 70:
            return 'Aggressive Buy'
        elif sentiment_score > 0.05 and confidence >= 60:
            return 'Buy'
        elif sentiment_score > -0.05:
            return 'Hold'
        elif sentiment_score > -0.2 and confidence >= 60:
            return 'Reduce Position'
        else:
            return 'Defensive'
    
    def _extract_key_factors(self, enhanced_data: Dict) -> List[str]:
        """提取關鍵影響因素"""
        factors = []
        
        # Fear & Greed Index
        fg_data = enhanced_data['data']['fear_greed_index']
        if fg_data['success']:
            fg_value = fg_data['data']['value']
            factors.append(f"市場情緒指數: {fg_value} ({fg_data['data']['classification']})")
        
        # 市場表現
        market_data = enhanced_data['data']['market_data']
        if market_data['success']:
            changes = [data['change_percent'] for data in market_data['data'].values() if 'change_percent' in data]
            if changes:
                avg_change = sum(changes) / len(changes)
                factors.append(f"主要指數平均變化: {avg_change:+.1f}%")
        
        # 經濟指標
        econ_data = enhanced_data['data']['economic_indicators']
        if econ_data['success']:
            factors.append(f"經濟指標覆蓋: {len(econ_data['data'])}項指標")
        
        # 新聞情緒
        news_data = enhanced_data['data']['news_sentiment']
        if news_data['success']:
            sentiment = news_data['data']['sentiment_label']
            factors.append(f"新聞情緒: {sentiment}")
        
        return factors
    
    def _assess_risk_level(self, market_sentiment: Dict, overall_reliability: float) -> str:
        """評估風險水平"""
        sentiment_score = abs(market_sentiment['overall_score'])
        confidence = market_sentiment['confidence']
        
        # 綜合評估風險
        if overall_reliability >= 80 and confidence >= 80:
            if sentiment_score > 0.3:
                return 'High Volatility'
            elif sentiment_score > 0.1:
                return 'Moderate Risk'
            else:
                return 'Low Risk'
        elif overall_reliability >= 60:
            return 'Moderate Risk'
        else:
            return 'High Uncertainty'

# 為了保持向後兼容性，提供原有的函數接口
def collect_all_data() -> Dict[str, Any]:
    """
    原有API兼容函數
    """
    collector = EnhancedLayer1Collector()
    return collector.collect_all_data()

def main():
    """測試增強版收集器"""
    print("\n" + "="*60)
    print("🚀 增強版第一層數據收集器測試")
    print("="*60)
    
    collector = EnhancedLayer1Collector()
    results = collector.collect_all_data()
    
    if results['success']:
        print(f"\n✅ 收集成功")
        print(f"⏱️ 收集時間: {results['collection_time']}秒")
        print(f"🎯 總體可靠性: {results['overall_reliability']}%")
        print(f"📊 數據品質: {results['data_quality']}")
        print(f"📈 數據覆蓋: {results['enhancement_info']['data_coverage']}")
        
        print(f"\n🎭 分析結果:")
        analysis = results['analysis']
        print(f"   市場環境: {analysis['market_environment']}")
        print(f"   投資建議: {analysis['investment_recommendation']}")
        print(f"   信心度: {analysis['confidence_level']}%")
        print(f"   風險評估: {analysis['risk_assessment']}")
        
        print(f"\n🔍 關鍵因素:")
        for factor in analysis['key_factors']:
            print(f"   • {factor}")
    else:
        print(f"❌ 收集失敗: {results.get('error', '未知錯誤')}")

if __name__ == "__main__":
    main() 