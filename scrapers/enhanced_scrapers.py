#!/usr/bin/env python3
"""
增強版數據爬蟲 - 整合多個數據源提高可信度
包含：FX678、CME FedWatch、Investing.com、CNN Fear & Greed等
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random
from datetime import datetime
from loguru import logger
from typing import Dict, List, Any, Optional
from config import Config

class EnhancedDataScraper:
    """增強版數據爬蟲"""
    
    def __init__(self):
        self.session = requests.Session()
        self._setup_session()
        
        # 新增數據源URL
        self.enhanced_urls = {
            'fx678_cpi': 'https://rl.fx678.com/content/id/112015032410000087.html',
            'cme_fedwatch': 'https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html',
            'investing_nonfarm': 'https://hk.investing.com/economic-calendar/nonfarm-payrolls-227',
            'cnn_fear_greed': 'https://edition.cnn.com/markets/fear-and-greed'
        }
    
    def _setup_session(self):
        """設置請求會話"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        self.session.headers.update(headers)
    
    def get_page_safely(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        """安全獲取網頁內容"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                # 隨機延遲避免被封
                time.sleep(random.uniform(1, 3))
                
                return BeautifulSoup(response.content, 'html.parser')
                
            except Exception as e:
                logger.warning(f"獲取頁面失敗 (嘗試 {attempt + 1}/{retries}): {url}, 錯誤: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # 指數退避
                else:
                    logger.error(f"最終獲取失敗: {url}")
                    return None
    
    def scrape_fx678_cpi(self) -> Optional[Dict[str, Any]]:
        """爬取FX678 CPI數據"""
        logger.info("🏛️ 開始爬取 FX678 CPI 數據...")
        
        try:
            soup = self.get_page_safely(self.enhanced_urls['fx678_cpi'])
            if not soup:
                return None
            
            # 提取CPI數據
            cpi_data = self._extract_fx678_cpi_data(soup)
            
            if cpi_data:
                logger.info(f"✅ FX678 CPI 數據獲取成功: {cpi_data}")
                return {
                    'source': 'FX678',
                    'timestamp': datetime.now().isoformat(),
                    'data': cpi_data,
                    'reliability': 'high'
                }
            else:
                logger.warning("⚠️ FX678 CPI 數據提取失敗")
                return None
                
        except Exception as e:
            logger.error(f"❌ FX678 CPI 爬取失敗: {str(e)}")
            return None
    
    def scrape_cme_fedwatch(self) -> Optional[Dict[str, Any]]:
        """爬取CME FedWatch利率預期數據"""
        logger.info("📈 開始爬取 CME FedWatch 數據...")
        
        try:
            soup = self.get_page_safely(self.enhanced_urls['cme_fedwatch'])
            if not soup:
                return None
            
            # 提取利率預期數據
            fed_data = self._extract_cme_fedwatch_data(soup)
            
            if fed_data:
                logger.info(f"✅ CME FedWatch 數據獲取成功: {fed_data}")
                return {
                    'source': 'CME FedWatch',
                    'timestamp': datetime.now().isoformat(),
                    'data': fed_data,
                    'reliability': 'very_high'
                }
            else:
                logger.warning("⚠️ CME FedWatch 數據提取失敗")
                return None
                
        except Exception as e:
            logger.error(f"❌ CME FedWatch 爬取失敗: {str(e)}")
            return None
    
    def scrape_investing_employment(self) -> Optional[Dict[str, Any]]:
        """爬取Investing.com就業數據"""
        logger.info("👥 開始爬取 Investing.com 就業數據...")
        
        try:
            soup = self.get_page_safely(self.enhanced_urls['investing_nonfarm'])
            if not soup:
                return None
            
            # 提取就業數據
            employment_data = self._extract_investing_employment_data(soup)
            
            if employment_data:
                logger.info(f"✅ Investing.com 就業數據獲取成功: {employment_data}")
                return {
                    'source': 'Investing.com',
                    'timestamp': datetime.now().isoformat(),
                    'data': employment_data,
                    'reliability': 'high'
                }
            else:
                logger.warning("⚠️ Investing.com 就業數據提取失敗")
                return None
                
        except Exception as e:
            logger.error(f"❌ Investing.com 就業數據爬取失敗: {str(e)}")
            return None
    
    def scrape_cnn_fear_greed(self) -> Optional[Dict[str, Any]]:
        """爬取CNN Fear & Greed Index"""
        logger.info("😨 開始爬取 CNN Fear & Greed Index...")
        
        try:
            soup = self.get_page_safely(self.enhanced_urls['cnn_fear_greed'])
            if not soup:
                return None
            
            # 提取恐懼貪婪指數
            fear_greed_data = self._extract_cnn_fear_greed_data(soup)
            
            if fear_greed_data:
                logger.info(f"✅ CNN Fear & Greed 數據獲取成功: {fear_greed_data}")
                return {
                    'source': 'CNN Fear & Greed',
                    'timestamp': datetime.now().isoformat(),
                    'data': fear_greed_data,
                    'reliability': 'high'
                }
            else:
                logger.warning("⚠️ CNN Fear & Greed 數據提取失敗")
                return None
                
        except Exception as e:
            logger.error(f"❌ CNN Fear & Greed 爬取失敗: {str(e)}")
            return None
    
    def scrape_all_enhanced_sources(self) -> Dict[str, Any]:
        """爬取所有增強數據源"""
        logger.info("🚀 開始爬取所有增強數據源...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'sources': {},
            'summary': {},
            'reliability_score': 0
        }
        
        # 爬取各個數據源
        scrapers = [
            ('fx678_cpi', self.scrape_fx678_cpi),
            ('cme_fedwatch', self.scrape_cme_fedwatch),
            ('investing_employment', self.scrape_investing_employment),
            ('cnn_fear_greed', self.scrape_cnn_fear_greed)
        ]
        
        successful_sources = 0
        total_sources = len(scrapers)
        
        for source_name, scraper_func in scrapers:
            try:
                data = scraper_func()
                if data:
                    results['sources'][source_name] = data
                    successful_sources += 1
                    
                    # 根據可靠性加分
                    reliability = data.get('reliability', 'medium')
                    if reliability == 'very_high':
                        results['reliability_score'] += 30
                    elif reliability == 'high':
                        results['reliability_score'] += 25
                    else:
                        results['reliability_score'] += 15
                
                # 隨機延遲避免過於頻繁請求
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                logger.error(f"❌ {source_name} 爬取失敗: {str(e)}")
        
        # 生成摘要
        results['summary'] = {
            'total_sources': total_sources,
            'successful_sources': successful_sources,
            'success_rate': f"{(successful_sources/total_sources)*100:.1f}%",
            'reliability_score': results['reliability_score'],
            'data_quality': self._assess_data_quality(results['sources'])
        }
        
        logger.info(f"✅ 增強數據源爬取完成，成功率: {results['summary']['success_rate']}")
        return results
    
    def _extract_fx678_cpi_data(self, soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """提取FX678 CPI數據"""
        try:
            text = soup.get_text()
            
            # 尋找CPI相關數據的多種模式
            patterns = [
                r'CPI.*?年率.*?([+-]?\d+\.?\d*)%',
                r'CPI.*?([+-]?\d+\.?\d*)%',
                r'通膨.*?([+-]?\d+\.?\d*)%',
                r'消費者物價.*?([+-]?\d+\.?\d*)%',
                r'核心CPI.*?([+-]?\d+\.?\d*)%'
            ]
            
            cpi_values = []
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    try:
                        value = float(match)
                        if -5 <= value <= 15:  # 合理的CPI範圍
                            cpi_values.append(value)
                    except ValueError:
                        continue
            
            if cpi_values:
                # 取最常見的值或平均值
                avg_cpi = sum(cpi_values) / len(cpi_values)
                return {
                    'cpi_annual': round(avg_cpi, 1),
                    'values_found': cpi_values,
                    'status': self._classify_inflation_status(avg_cpi),
                    'indicator': 'CPI Annual Rate'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"FX678 CPI數據提取失敗: {str(e)}")
            return None
    
    def _extract_cme_fedwatch_data(self, soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """提取CME FedWatch數據"""
        try:
            text = soup.get_text()
            
            # 尋找利率預期相關數據
            patterns = [
                r'(\d+\.?\d*)%.*?probability',
                r'probability.*?(\d+\.?\d*)%',
                r'(\d+\.?\d*)\s*basis\s*points',
                r'(\d+\.?\d*)%.*?chance',
                r'(\d+\.?\d*)\s*bps'
            ]
            
            probabilities = []
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    try:
                        value = float(match)
                        if 0 <= value <= 100:  # 概率範圍
                            probabilities.append(value)
                    except ValueError:
                        continue
            
            if probabilities:
                # 找出最高概率
                max_prob = max(probabilities)
                return {
                    'max_probability': max_prob,
                    'all_probabilities': probabilities,
                    'fed_outlook': self._interpret_fed_probability(max_prob),
                    'indicator': 'Fed Rate Probability'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"CME FedWatch數據提取失敗: {str(e)}")
            return None
    
    def _extract_investing_employment_data(self, soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """提取Investing.com就業數據"""
        try:
            text = soup.get_text()
            
            # 尋找就業相關數據
            patterns = [
                r'非農.*?(\d+\.?\d*)[KM]?',
                r'nonfarm.*?(\d+\.?\d*)[KM]?',
                r'unemployment.*?(\d+\.?\d*)%',
                r'失業率.*?(\d+\.?\d*)%',
                r'(\d+\.?\d*)[KM]?\s*jobs'
            ]
            
            employment_data = {}
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    try:
                        value = float(match)
                        if 'unemployment' in pattern.lower() or '失業' in pattern:
                            if 0 <= value <= 20:  # 失業率合理範圍
                                employment_data['unemployment_rate'] = value
                        else:
                            if 0 <= value <= 1000:  # 就業人數合理範圍
                                employment_data['nonfarm_payrolls'] = value
                    except ValueError:
                        continue
            
            if employment_data:
                return {
                    **employment_data,
                    'employment_health': self._assess_employment_health(employment_data),
                    'indicator': 'Employment Data'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Investing.com就業數據提取失敗: {str(e)}")
            return None
    
    def _extract_cnn_fear_greed_data(self, soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """提取CNN Fear & Greed數據"""
        try:
            text = soup.get_text()
            
            # 尋找恐懼貪婪指數
            patterns = [
                r'fear.*?greed.*?(\d+)',
                r'(\d+).*?fear.*?greed',
                r'index.*?(\d+)',
                r'greed.*?(\d+)',
                r'fear.*?(\d+)'
            ]
            
            index_values = []
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    try:
                        value = int(match)
                        if 0 <= value <= 100:  # 指數範圍
                            index_values.append(value)
                    except ValueError:
                        continue
            
            if index_values:
                # 取最可能的值（出現頻率最高或中位數）
                avg_index = sum(index_values) / len(index_values)
                return {
                    'fear_greed_index': round(avg_index),
                    'values_found': index_values,
                    'sentiment': self._classify_market_sentiment(avg_index),
                    'interpretation': self._interpret_sentiment(avg_index),
                    'indicator': 'Fear & Greed Index'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"CNN Fear & Greed數據提取失敗: {str(e)}")
            return None
    
    def _classify_inflation_status(self, cpi_value: float) -> str:
        """分類通膨狀況"""
        if cpi_value >= 5:
            return "高通膨"
        elif cpi_value >= 3:
            return "中度通膨"
        elif cpi_value >= 2:
            return "目標通膨"
        elif cpi_value >= 0:
            return "低通膨"
        else:
            return "通縮"
    
    def _interpret_fed_probability(self, probability: float) -> str:
        """解讀聯準會利率預期"""
        if probability >= 80:
            return "高度確定"
        elif probability >= 60:
            return "很可能"
        elif probability >= 40:
            return "可能"
        elif probability >= 20:
            return "不太可能"
        else:
            return "極不可能"
    
    def _assess_employment_health(self, data: Dict) -> str:
        """評估就業市場健康度"""
        unemployment = data.get('unemployment_rate', 5)
        nonfarm = data.get('nonfarm_payrolls', 200)
        
        if unemployment < 4 and nonfarm > 250:
            return "強勁"
        elif unemployment < 5 and nonfarm > 150:
            return "健康"
        elif unemployment < 6:
            return "溫和"
        else:
            return "疲弱"
    
    def _classify_market_sentiment(self, index_value: float) -> str:
        """分類市場情緒"""
        if index_value >= 75:
            return "極度貪婪"
        elif index_value >= 55:
            return "貪婪"
        elif index_value >= 45:
            return "中性"
        elif index_value >= 25:
            return "恐懼"
        else:
            return "極度恐懼"
    
    def _interpret_sentiment(self, score: float) -> str:
        """解讀市場情緒"""
        if score > 75:
            return "市場極度貪婪，建議謹慎，可能接近頂部"
        elif score > 60:
            return "市場偏向貪婪，適度參與但需設定停損"
        elif score > 40:
            return "市場情緒中性，平衡操作等待明確信號"
        elif score > 25:
            return "市場偏向恐懼，可尋找優質標的逢低布局"
        else:
            return "市場極度恐懼，往往是買入機會但需分批進場"
    
    def _assess_data_quality(self, sources: Dict) -> str:
        """評估數據品質"""
        if len(sources) >= 3:
            return "優秀"
        elif len(sources) >= 2:
            return "良好"
        elif len(sources) >= 1:
            return "一般"
        else:
            return "不足" 