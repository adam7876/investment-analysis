import re
import time
import random
from datetime import datetime
from loguru import logger
from config import Config
from scrapers.base_scraper import BaseScraper

class MacroMicroScraper(BaseScraper):
    """MacroMicro 總經數據爬蟲"""
    
    def __init__(self):
        super().__init__()
        self.gdp_url = Config.URLS['macromicro_gdp']
        self.cpi_url = Config.URLS['macromicro_cpi']
    
    def scrape_gdp(self):
        """爬取美國 GDP 成長率數據"""
        logger.info("開始爬取 MacroMicro GDP 數據")
        
        try:
            soup = self.get_page(self.gdp_url, use_selenium=False)
            
            if not soup:
                logger.warning("requests 方式無法獲取 GDP 頁面，嘗試使用 Selenium")
                soup = self.get_page(self.gdp_url, use_selenium=True)
            
            if not soup:
                logger.error("無法獲取 MacroMicro GDP 頁面")
                return None
            
            gdp_data = self._extract_gdp_data(soup)
            
            if gdp_data:
                logger.info(f"成功獲取 GDP 數據: {gdp_data}")
                return gdp_data
            else:
                logger.warning("未能提取到 GDP 數據")
                return None
                
        except Exception as e:
            logger.error(f"爬取 MacroMicro GDP 數據失敗: {str(e)}")
            return None
    
    def scrape_cpi(self):
        """爬取美國 CPI 數據"""
        logger.info("開始爬取 MacroMicro CPI 數據")
        
        try:
            soup = self.get_page(self.cpi_url, use_selenium=False)
            
            if not soup:
                logger.warning("requests 方式無法獲取 CPI 頁面，嘗試使用 Selenium")
                soup = self.get_page(self.cpi_url, use_selenium=True)
            
            if not soup:
                logger.error("無法獲取 MacroMicro CPI 頁面")
                return None
            
            cpi_data = self._extract_cpi_data(soup)
            
            if cpi_data:
                logger.info(f"成功獲取 CPI 數據: {cpi_data}")
                return cpi_data
            else:
                logger.warning("未能提取到 CPI 數據")
                return None
                
        except Exception as e:
            logger.error(f"爬取 MacroMicro CPI 數據失敗: {str(e)}")
            return None
    
    def scrape(self):
        """爬取所有 MacroMicro 數據"""
        logger.info("開始爬取 MacroMicro 總經數據")
        
        results = {}
        
        # 爬取 GDP 數據
        gdp_data = self.scrape_gdp()
        if gdp_data:
            results['gdp'] = gdp_data
        
        # 隨機延遲避免過於頻繁請求
        time.sleep(random.uniform(2, 4))
        
        # 爬取 CPI 數據
        cpi_data = self.scrape_cpi()
        if cpi_data:
            results['cpi'] = cpi_data
        
        if results:
            results['timestamp'] = datetime.now().isoformat()
            results['source'] = 'MacroMicro'
            return results
        else:
            return None
    
    def _extract_gdp_data(self, soup):
        """提取 GDP 數據"""
        try:
            # 尋找 GDP 相關數據的多種選擇器
            selectors = [
                '.chart-value',
                '.data-value',
                '.latest-value',
                '[class*="value"]',
                '.number',
                '.percentage'
            ]
            
            # 尋找包含百分比的文本
            gdp_value = None
            gdp_text = None
            
            # 先嘗試從頁面文本中提取
            page_text = soup.get_text()
            
            # 尋找 GDP 成長率的模式
            patterns = [
                r'GDP.*?([+-]?\d+\.?\d*)%',
                r'成長率.*?([+-]?\d+\.?\d*)%',
                r'([+-]?\d+\.?\d*)%.*?GDP',
                r'Real GDP.*?([+-]?\d+\.?\d*)%',
                r'實質.*?([+-]?\d+\.?\d*)%'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    try:
                        gdp_value = float(match.group(1))
                        break
                    except ValueError:
                        continue
            
            # 如果沒找到，嘗試從特定元素中提取
            if gdp_value is None:
                for selector in selectors:
                    elements = soup.select(selector)
                    for element in elements:
                        text = element.get_text().strip()
                        if '%' in text:
                            number = self._extract_number_with_sign(text)
                            if number is not None and -20 <= number <= 20:  # GDP 成長率合理範圍
                                gdp_value = number
                                gdp_text = text
                                break
                    if gdp_value is not None:
                        break
            
            if gdp_value is not None:
                # 判斷經濟狀況
                economic_status = self._classify_gdp_status(gdp_value)
                
                return {
                    'value': gdp_value,
                    'text': gdp_text or f"{gdp_value}%",
                    'status': economic_status,
                    'indicator': 'GDP Growth Rate',
                    'unit': '%'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"提取 GDP 數據失敗: {str(e)}")
            return None
    
    def _extract_cpi_data(self, soup):
        """提取 CPI 數據"""
        try:
            page_text = soup.get_text()
            
            # 尋找 CPI 相關的模式
            patterns = [
                r'CPI.*?([+-]?\d+\.?\d*)%',
                r'通膨.*?([+-]?\d+\.?\d*)%',
                r'([+-]?\d+\.?\d*)%.*?CPI',
                r'Consumer Price.*?([+-]?\d+\.?\d*)%',
                r'物價.*?([+-]?\d+\.?\d*)%'
            ]
            
            cpi_value = None
            cpi_text = None
            
            for pattern in patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    try:
                        cpi_value = float(match.group(1))
                        break
                    except ValueError:
                        continue
            
            # 如果沒找到，嘗試從特定元素中提取
            if cpi_value is None:
                selectors = [
                    '.chart-value',
                    '.data-value',
                    '.latest-value',
                    '[class*="value"]'
                ]
                
                for selector in selectors:
                    elements = soup.select(selector)
                    for element in elements:
                        text = element.get_text().strip()
                        if '%' in text:
                            number = self._extract_number_with_sign(text)
                            if number is not None and -5 <= number <= 15:  # CPI 合理範圍
                                cpi_value = number
                                cpi_text = text
                                break
                    if cpi_value is not None:
                        break
            
            if cpi_value is not None:
                # 判斷通膨狀況
                inflation_status = self._classify_inflation_status(cpi_value)
                
                return {
                    'value': cpi_value,
                    'text': cpi_text or f"{cpi_value}%",
                    'status': inflation_status,
                    'indicator': 'CPI Inflation Rate',
                    'unit': '%'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"提取 CPI 數據失敗: {str(e)}")
            return None
    
    def _extract_number_with_sign(self, text):
        """從文本中提取帶符號的數字"""
        if not text:
            return None
        
        # 移除所有非數字、小數點、正負號的字符
        numbers = re.findall(r'[+-]?\d+\.?\d*', text.strip())
        
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return None
        
        return None
    
    def _classify_gdp_status(self, gdp_value):
        """根據 GDP 成長率分類經濟狀況"""
        if gdp_value >= 4:
            return "強勁成長"
        elif gdp_value >= 2:
            return "穩定成長"
        elif gdp_value >= 0:
            return "緩慢成長"
        elif gdp_value >= -2:
            return "輕微衰退"
        else:
            return "嚴重衰退"
    
    def _classify_inflation_status(self, cpi_value):
        """根據 CPI 分類通膨狀況"""
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