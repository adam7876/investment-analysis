#!/usr/bin/env python3
"""
第一層數據收集器 - 總經與市場環境（增強版）
整合多個數據源，提供更可靠的總經數據收集介面
"""

import time
import random
from datetime import datetime
from loguru import logger

from scrapers.alternative_fear_greed_scraper import AlternativeFearGreedScraper
from scrapers.macromicro_scraper import MacroMicroScraper
from scrapers.fred_api_scraper import FREDAPIScraper
from scrapers.enhanced_scrapers import EnhancedDataScraper

class Layer1Collector:
    """第一層數據收集器（增強版）"""
    
    def __init__(self):
        self.fear_greed_scraper = AlternativeFearGreedScraper()
        self.macromicro_scraper = MacroMicroScraper()
        self.fred_scraper = FREDAPIScraper()
        self.enhanced_scraper = EnhancedDataScraper()  # 新增增強爬蟲
    
    def collect_all_data(self):
        """收集所有第一層數據（增強版）"""
        logger.info("🚀 開始收集第一層總經數據（增強版）")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'layer': 'Layer 1 - 總經與市場環境（增強版）',
            'data_sources': {},
            'enhanced_sources': {},
            'analysis': {},
            'reliability_assessment': {}
        }
        
        # === 原有數據源 ===
        
        # 1. 收集 Fear & Greed Index (Alternative.me)
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
        
        # 3. 收集 MacroMicro 數據（可選）
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
        
        # === 新增增強數據源 ===
        
        # 隨機延遲
        time.sleep(random.uniform(3, 5))
        
        # 4. 收集增強數據源
        logger.info("🔥 收集增強數據源（FX678、CME、Investing.com、CNN）...")
        try:
            enhanced_data = self.enhanced_scraper.scrape_all_enhanced_sources()
            if enhanced_data and enhanced_data.get('sources'):
                results['enhanced_sources'] = enhanced_data
                logger.info(f"✅ 增強數據源收集成功，成功率: {enhanced_data['summary']['success_rate']}")
                logger.info(f"📊 可靠性評分: {enhanced_data['summary']['reliability_score']}/100")
            else:
                logger.warning("⚠️ 增強數據源獲取失敗")
        except Exception as e:
            logger.error(f"❌ 增強數據源收集失敗: {str(e)}")
        
        # 5. 進行綜合分析（整合所有數據源）
        logger.info("🧠 進行市場環境綜合分析...")
        analysis = self._analyze_market_environment_enhanced(
            results['data_sources'], 
            results['enhanced_sources']
        )
        results['analysis'] = analysis
        
        # 6. 評估數據可靠性
        reliability = self._assess_data_reliability(
            results['data_sources'], 
            results['enhanced_sources']
        )
        results['reliability_assessment'] = reliability
        
        logger.info("✅ 第一層數據收集完成（增強版）")
        logger.info(f"📈 總體可靠性: {reliability['overall_reliability']}")
        
        return results
    
    def _analyze_market_environment_enhanced(self, original_sources, enhanced_sources):
        """增強版市場環境分析"""
        analysis = {
            'market_sentiment': 'Unknown',
            'economic_indicators': {},
            'market_phase': '未知',
            'risk_appetite': '中性',
            'investment_environment': '謹慎',
            'confidence_level': 50,
            'key_factors': [],
            'data_cross_validation': {}
        }
        
        try:
            # === 市場情緒分析（多源交叉驗證）===
            sentiment_sources = []
            
            # Alternative.me Fear & Greed
            if 'fear_greed' in original_sources:
                fg_data = original_sources['fear_greed']
                sentiment_sources.append({
                    'source': 'Alternative.me',
                    'value': fg_data['index_value'],
                    'sentiment': fg_data['sentiment'],
                    'weight': 0.4
                })
            
            # CNN Fear & Greed
            if enhanced_sources and 'cnn_fear_greed' in enhanced_sources.get('sources', {}):
                cnn_data = enhanced_sources['sources']['cnn_fear_greed']['data']
                sentiment_sources.append({
                    'source': 'CNN',
                    'value': cnn_data['fear_greed_index'],
                    'sentiment': cnn_data['sentiment'],
                    'weight': 0.3
                })
            
            # 計算加權平均情緒指數
            if sentiment_sources:
                weighted_sentiment = sum(s['value'] * s['weight'] for s in sentiment_sources)
                total_weight = sum(s['weight'] for s in sentiment_sources)
                avg_sentiment = weighted_sentiment / total_weight if total_weight > 0 else 50
                
                analysis['market_sentiment'] = self._classify_sentiment(avg_sentiment)
                analysis['sentiment_index'] = round(avg_sentiment)
                analysis['data_cross_validation']['sentiment'] = {
                    'sources': sentiment_sources,
                    'weighted_average': round(avg_sentiment),
                    'consensus': len(sentiment_sources) >= 2
                }
            
            # === 經濟指標分析（多源整合）===
            economic_data = {}
            
            # FRED數據
            if 'fred' in original_sources:
                fred_data = original_sources['fred']
                economic_data.update({
                    'gdp_growth': fred_data.get('gdp_growth', 2.0),
                    'unemployment_rate': fred_data.get('unemployment_rate', 4.0),
                    'inflation_rate': fred_data.get('inflation_rate', 3.0)
                })
            
            # FX678 CPI數據
            if enhanced_sources and 'fx678_cpi' in enhanced_sources.get('sources', {}):
                fx678_data = enhanced_sources['sources']['fx678_cpi']['data']
                economic_data['cpi_fx678'] = fx678_data['cpi_annual']
                economic_data['inflation_status'] = fx678_data['status']
            
            # Investing.com就業數據
            if enhanced_sources and 'investing_employment' in enhanced_sources.get('sources', {}):
                inv_data = enhanced_sources['sources']['investing_employment']['data']
                if 'unemployment_rate' in inv_data:
                    economic_data['unemployment_investing'] = inv_data['unemployment_rate']
                if 'nonfarm_payrolls' in inv_data:
                    economic_data['nonfarm_payrolls'] = inv_data['nonfarm_payrolls']
                economic_data['employment_health'] = inv_data['employment_health']
            
            # CME FedWatch利率預期
            if enhanced_sources and 'cme_fedwatch' in enhanced_sources.get('sources', {}):
                cme_data = enhanced_sources['sources']['cme_fedwatch']['data']
                economic_data['fed_rate_probability'] = cme_data['max_probability']
                economic_data['fed_outlook'] = cme_data['fed_outlook']
            
            analysis['economic_indicators'] = economic_data
            
            # === 市場階段判斷 ===
            market_phase = self._determine_market_phase_enhanced(analysis)
            analysis['market_phase'] = market_phase
            
            # === 風險偏好評估 ===
            risk_appetite = self._assess_risk_appetite_enhanced(analysis)
            analysis['risk_appetite'] = risk_appetite
            
            # === 投資環境評估 ===
            investment_env = self._assess_investment_environment_enhanced(analysis)
            analysis['investment_environment'] = investment_env
            
            # === 信心水準計算 ===
            confidence = self._calculate_confidence_level_enhanced(
                original_sources, enhanced_sources, analysis
            )
            analysis['confidence_level'] = confidence
            
            # === 關鍵因素識別 ===
            key_factors = self._identify_key_factors_enhanced(analysis)
            analysis['key_factors'] = key_factors
            
        except Exception as e:
            logger.error(f"增強版市場環境分析失敗: {str(e)}")
            analysis['key_factors'].append(f'分析錯誤: {str(e)}')
        
        return analysis
    
    def _assess_data_reliability(self, original_sources, enhanced_sources):
        """評估數據可靠性"""
        reliability = {
            'original_sources_count': len(original_sources),
            'enhanced_sources_count': len(enhanced_sources.get('sources', {})) if enhanced_sources else 0,
            'total_sources': 0,
            'reliability_score': 0,
            'overall_reliability': '低',
            'source_details': {}
        }
        
        # 計算總數據源數量
        reliability['total_sources'] = reliability['original_sources_count'] + reliability['enhanced_sources_count']
        
        # 計算可靠性評分
        base_score = reliability['original_sources_count'] * 20  # 原始數據源每個20分
        enhanced_score = enhanced_sources.get('summary', {}).get('reliability_score', 0) if enhanced_sources else 0
        
        reliability['reliability_score'] = base_score + enhanced_score
        
        # 評估整體可靠性
        if reliability['reliability_score'] >= 80:
            reliability['overall_reliability'] = '很高'
        elif reliability['reliability_score'] >= 60:
            reliability['overall_reliability'] = '高'
        elif reliability['reliability_score'] >= 40:
            reliability['overall_reliability'] = '中等'
        elif reliability['reliability_score'] >= 20:
            reliability['overall_reliability'] = '低'
        else:
            reliability['overall_reliability'] = '很低'
        
        # 詳細來源信息
        for source in original_sources:
            reliability['source_details'][source] = {
                'type': 'original',
                'status': 'success',
                'reliability': 'medium'
            }
        
        if enhanced_sources and 'sources' in enhanced_sources:
            for source, data in enhanced_sources['sources'].items():
                reliability['source_details'][source] = {
                    'type': 'enhanced',
                    'status': 'success',
                    'reliability': data.get('reliability', 'medium')
                }
        
        return reliability
    
    def _classify_sentiment(self, score):
        """分類市場情緒"""
        if score >= 75:
            return "極度貪婪"
        elif score >= 55:
            return "貪婪"
        elif score >= 45:
            return "中性"
        elif score >= 25:
            return "恐懼"
        else:
            return "極度恐懼"
    
    def _determine_market_phase_enhanced(self, analysis):
        """增強版市場階段判斷"""
        sentiment_index = analysis.get('sentiment_index', 50)
        economic_indicators = analysis.get('economic_indicators', {})
        
        # 基於多個指標判斷
        if sentiment_index > 70 and economic_indicators.get('gdp_growth', 0) > 3:
            return "牛市後期"
        elif sentiment_index > 55 and economic_indicators.get('unemployment_rate', 10) < 5:
            return "牛市中期"
        elif sentiment_index < 30:
            return "熊市"
        elif sentiment_index < 45:
            return "修正期"
        else:
            return "盤整期"
    
    def _assess_risk_appetite_enhanced(self, analysis):
        """增強版風險偏好評估"""
        sentiment_index = analysis.get('sentiment_index', 50)
        
        if sentiment_index > 70:
            return "高風險偏好"
        elif sentiment_index > 55:
            return "中高風險偏好"
        elif sentiment_index > 45:
            return "中性"
        elif sentiment_index > 30:
            return "低風險偏好"
        else:
            return "極低風險偏好"
    
    def _assess_investment_environment_enhanced(self, analysis):
        """增強版投資環境評估"""
        sentiment = analysis.get('market_sentiment', '中性')
        phase = analysis.get('market_phase', '盤整期')
        
        if sentiment in ['極度貪婪'] or phase == '牛市後期':
            return "謹慎"
        elif sentiment in ['貪婪'] or phase == '牛市中期':
            return "積極"
        elif sentiment in ['極度恐懼'] or phase == '熊市':
            return "機會"
        else:
            return "平衡"
    
    def _calculate_confidence_level_enhanced(self, original_sources, enhanced_sources, analysis):
        """增強版信心水準計算"""
        base_confidence = 30
        
        # 數據源數量加分
        source_count = len(original_sources) + len(enhanced_sources.get('sources', {})) if enhanced_sources else 0
        source_bonus = min(source_count * 10, 40)
        
        # 數據一致性加分
        consistency_bonus = 0
        if 'data_cross_validation' in analysis:
            if analysis['data_cross_validation'].get('sentiment', {}).get('consensus'):
                consistency_bonus += 20
        
        # 可靠性評分加分
        reliability_bonus = 0
        if enhanced_sources:
            reliability_score = enhanced_sources.get('summary', {}).get('reliability_score', 0)
            reliability_bonus = min(reliability_score // 5, 10)
        
        total_confidence = base_confidence + source_bonus + consistency_bonus + reliability_bonus
        return min(total_confidence, 95)  # 最高95%
    
    def _identify_key_factors_enhanced(self, analysis):
        """增強版關鍵因素識別"""
        factors = []
        
        # 市場情緒因素
        sentiment = analysis.get('market_sentiment', '中性')
        if sentiment in ['極度貪婪', '極度恐懼']:
            factors.append(f'市場情緒{sentiment}，需特別關注')
        
        # 經濟指標因素
        economic = analysis.get('economic_indicators', {})
        if 'inflation_status' in economic:
            factors.append(f'通膨狀況：{economic["inflation_status"]}')
        
        if 'employment_health' in economic:
            factors.append(f'就業市場：{economic["employment_health"]}')
        
        if 'fed_outlook' in economic:
            factors.append(f'聯準會政策：{economic["fed_outlook"]}')
        
        # 市場階段因素
        phase = analysis.get('market_phase', '盤整期')
        if phase in ['牛市後期', '熊市']:
            factors.append(f'市場處於{phase}，需調整策略')
        
        return factors
    
    def get_summary_report(self):
        """獲取摘要報告（增強版）"""
        data = self.collect_all_data()
        
        report = {
            'timestamp': data['timestamp'],
            'summary': {},
            'recommendations': [],
            'data_quality': {},
            'reliability': data.get('reliability_assessment', {})
        }
        
        # 數據品質評估
        original_count = len(data['data_sources'])
        enhanced_count = len(data['enhanced_sources'].get('sources', {})) if data['enhanced_sources'] else 0
        total_sources = original_count + enhanced_count
        
        report['data_quality'] = {
            'original_sources': original_count,
            'enhanced_sources': enhanced_count,
            'total_sources': total_sources,
            'success_rate': f"{(total_sources/6)*100:.1f}%",  # 總共6個可能的數據源
            'available_data': list(data['data_sources'].keys()) + list(data['enhanced_sources'].get('sources', {}).keys()) if data['enhanced_sources'] else []
        }
        
        # 摘要信息
        analysis = data.get('analysis', {})
        if analysis:
            report['summary'] = {
                'market_sentiment': analysis.get('market_sentiment', '未知'),
                'sentiment_index': analysis.get('sentiment_index', 50),
                'market_phase': analysis.get('market_phase', '未知'),
                'investment_environment': analysis.get('investment_environment', '謹慎'),
                'confidence_level': analysis.get('confidence_level', 50)
            }
            
            # 投資建議
            env = analysis.get('investment_environment', '謹慎')
            if env == '機會':
                report['recommendations'].append('市場恐慌提供買入機會，建議分批進場')
            elif env == '積極':
                report['recommendations'].append('市場情緒良好，可積極參與但需設定停損')
            elif env == '謹慎':
                report['recommendations'].append('市場過熱，建議謹慎操作或獲利了結')
            else:
                report['recommendations'].append('市場情緒中性，建議平衡配置等待明確信號')
        
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
        print(f"🏛️ 經濟階段: {summary['summary'].get('market_phase', 'N/A')}")
        print(f"💡 投資建議: {summary['summary'].get('investment_environment', 'N/A')}")
        print(f"⚠️ 風險等級: {summary['summary'].get('risk_appetite', 'N/A')}")
        
        print(f"\n📊 數據品質:")
        print(f"   成功率: {summary['data_quality']['success_rate']}")
        print(f"   可用數據源: {', '.join(summary['data_quality']['available_data'])}")
        
        if summary['recommendations']:
            print(f"\n💡 關鍵因素:")
            for i, rec in enumerate(summary['recommendations'][:5], 1):
                print(f"   {i}. {rec}")

if __name__ == "__main__":
    main() 