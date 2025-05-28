import requests
from datetime import datetime, timedelta
from loguru import logger
from config import Config

class FREDAPIScraper:
    """FRED (Federal Reserve Economic Data) API 爬蟲"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or Config.FRED_API_KEY
        self.base_url = "https://api.stlouisfed.org/fred"
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """設置請求會話"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        self.session.headers.update(headers)
    
    def get_series_data(self, series_id, limit=1):
        """
        獲取 FRED 數據系列
        
        Args:
            series_id (str): FRED 數據系列 ID
            limit (int): 獲取數據點數量
        
        Returns:
            dict: 數據結果
        """
        if not self.api_key or self.api_key == 'demo':
            logger.warning("FRED API 密鑰未設置，跳過 FRED 數據獲取")
            return None
        
        try:
            # 獲取最近的數據
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            
            params = {
                'series_id': series_id,
                'api_key': self.api_key,
                'file_type': 'json',
                'start_date': start_date,
                'end_date': end_date,
                'sort_order': 'desc',
                'limit': limit
            }
            
            url = f"{self.base_url}/series/observations"
            response = self.session.get(url, params=params, timeout=Config.TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
            
            if 'observations' in data and data['observations']:
                latest_observation = data['observations'][0]
                
                return {
                    'series_id': series_id,
                    'date': latest_observation['date'],
                    'value': latest_observation['value'],
                    'timestamp': datetime.now().isoformat(),
                    'source': 'FRED API'
                }
            else:
                logger.warning(f"FRED API 沒有返回 {series_id} 的數據")
                return None
                
        except requests.RequestException as e:
            logger.error(f"FRED API 請求失敗: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"獲取 FRED 數據失敗: {str(e)}")
            return None
    
    def scrape(self):
        """爬取主要經濟指標"""
        logger.info("開始獲取 FRED 經濟數據")
        
        if not self.api_key or self.api_key == 'demo':
            logger.info("FRED API 密鑰未設置，返回模擬數據")
            return self._get_mock_data()
        
        results = {}
        
        # 主要經濟指標的 FRED 系列 ID
        indicators = {
            'gdp': 'GDP',  # GDP
            'unemployment': 'UNRATE',  # 失業率
            'inflation': 'CPIAUCSL',  # CPI
            'fed_funds_rate': 'FEDFUNDS',  # 聯邦基金利率
            'nonfarm_payrolls': 'PAYEMS'  # 非農就業
        }
        
        for indicator_name, series_id in indicators.items():
            try:
                data = self.get_series_data(series_id)
                if data:
                    results[indicator_name] = data
                    logger.info(f"成功獲取 {indicator_name}: {data['value']}")
                else:
                    logger.warning(f"無法獲取 {indicator_name} 數據")
            except Exception as e:
                logger.error(f"獲取 {indicator_name} 數據失敗: {str(e)}")
        
        if results:
            results['timestamp'] = datetime.now().isoformat()
            results['source'] = 'FRED API'
            return results
        else:
            return None
    
    def _get_mock_data(self):
        """返回模擬數據（當沒有 API 密鑰時）"""
        return {
            'gdp': {
                'series_id': 'GDP',
                'date': '2024-12-31',
                'value': '2.8',
                'timestamp': datetime.now().isoformat(),
                'source': 'FRED API (Mock)'
            },
            'unemployment': {
                'series_id': 'UNRATE',
                'date': '2024-12-31',
                'value': '4.1',
                'timestamp': datetime.now().isoformat(),
                'source': 'FRED API (Mock)'
            },
            'inflation': {
                'series_id': 'CPIAUCSL',
                'date': '2024-12-31',
                'value': '3.2',
                'timestamp': datetime.now().isoformat(),
                'source': 'FRED API (Mock)'
            },
            'fed_funds_rate': {
                'series_id': 'FEDFUNDS',
                'date': '2024-12-31',
                'value': '5.25',
                'timestamp': datetime.now().isoformat(),
                'source': 'FRED API (Mock)'
            },
            'timestamp': datetime.now().isoformat(),
            'source': 'FRED API (Mock Data)',
            'note': '這是模擬數據，請設置 FRED_API_KEY 以獲取真實數據'
        }
    
    def analyze_economic_conditions(self):
        """分析經濟狀況"""
        data = self.scrape()
        
        if not data:
            return None
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'economic_phase': 'Unknown',
            'inflation_pressure': 'Unknown',
            'employment_health': 'Unknown',
            'monetary_policy': 'Unknown'
        }
        
        try:
            # 分析通膨壓力
            if 'inflation' in data and data['inflation']['value'] != '.':
                inflation_rate = float(data['inflation']['value'])
                if inflation_rate > 4:
                    analysis['inflation_pressure'] = '高通膨壓力'
                elif inflation_rate > 2.5:
                    analysis['inflation_pressure'] = '中度通膨壓力'
                elif inflation_rate > 1:
                    analysis['inflation_pressure'] = '溫和通膨'
                else:
                    analysis['inflation_pressure'] = '低通膨風險'
            
            # 分析就業狀況
            if 'unemployment' in data and data['unemployment']['value'] != '.':
                unemployment_rate = float(data['unemployment']['value'])
                if unemployment_rate < 4:
                    analysis['employment_health'] = '充分就業'
                elif unemployment_rate < 6:
                    analysis['employment_health'] = '健康就業'
                elif unemployment_rate < 8:
                    analysis['employment_health'] = '就業疲軟'
                else:
                    analysis['employment_health'] = '高失業率'
            
            # 分析貨幣政策
            if 'fed_funds_rate' in data and data['fed_funds_rate']['value'] != '.':
                fed_rate = float(data['fed_funds_rate']['value'])
                if fed_rate > 4:
                    analysis['monetary_policy'] = '緊縮政策'
                elif fed_rate > 2:
                    analysis['monetary_policy'] = '中性政策'
                elif fed_rate > 0.5:
                    analysis['monetary_policy'] = '寬鬆政策'
                else:
                    analysis['monetary_policy'] = '極度寬鬆'
            
            # 綜合判斷經濟階段
            if (analysis['inflation_pressure'] in ['高通膨壓力', '中度通膨壓力'] and 
                analysis['employment_health'] in ['充分就業', '健康就業']):
                analysis['economic_phase'] = '擴張期'
            elif (analysis['inflation_pressure'] in ['低通膨風險'] and 
                  analysis['employment_health'] in ['高失業率', '就業疲軟']):
                analysis['economic_phase'] = '衰退期'
            elif analysis['employment_health'] in ['充分就業', '健康就業']:
                analysis['economic_phase'] = '穩定成長期'
            else:
                analysis['economic_phase'] = '轉折期'
                
        except (ValueError, KeyError) as e:
            logger.warning(f"經濟狀況分析失敗: {str(e)}")
        
        return analysis
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self.session, 'close'):
            self.session.close() 