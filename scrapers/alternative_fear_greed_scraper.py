import requests
from datetime import datetime
from loguru import logger
from config import Config

class AlternativeFearGreedScraper:
    """Alternative.me Fear & Greed Index API 爬蟲"""
    
    def __init__(self):
        self.api_url = "https://api.alternative.me/fng/"
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """設置請求會話"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        self.session.headers.update(headers)
    
    def scrape(self, limit=1):
        """
        爬取 Alternative.me Fear & Greed Index
        
        Args:
            limit (int): 獲取數據的數量，默認為1（最新數據）
        
        Returns:
            dict: 包含恐慌貪婪指數的數據
        """
        logger.info("開始獲取 Alternative.me Fear & Greed Index")
        
        try:
            # 構建 API 請求 URL
            params = {
                'limit': limit,
                'format': 'json'
            }
            
            response = self.session.get(
                self.api_url, 
                params=params, 
                timeout=Config.TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            
            # 檢查 API 響應
            if 'data' not in data or not data['data']:
                logger.error("API 響應中沒有數據")
                return None
            
            # 提取最新的恐慌貪婪指數
            latest_data = data['data'][0]
            
            fear_greed_data = {
                'timestamp': datetime.now().isoformat(),
                'index_value': int(latest_data['value']),
                'index_text': latest_data['value_classification'],
                'sentiment': latest_data['value_classification'],
                'source': 'Alternative.me Fear & Greed Index',
                'api_timestamp': latest_data['timestamp'],
                'time_until_update': latest_data.get('time_until_update', None)
            }
            
            logger.info(f"成功獲取 Fear & Greed Index: {fear_greed_data}")
            return fear_greed_data
            
        except requests.RequestException as e:
            logger.error(f"API 請求失敗: {str(e)}")
            return None
        except (KeyError, ValueError, TypeError) as e:
            logger.error(f"數據解析失敗: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"獲取 Alternative.me Fear & Greed Index 失敗: {str(e)}")
            return None
    
    def get_historical_data(self, limit=10):
        """
        獲取歷史恐慌貪婪指數數據
        
        Args:
            limit (int): 獲取歷史數據的數量
        
        Returns:
            list: 歷史數據列表
        """
        logger.info(f"開始獲取 {limit} 天的歷史 Fear & Greed Index 數據")
        
        try:
            params = {
                'limit': limit,
                'format': 'json'
            }
            
            response = self.session.get(
                self.api_url, 
                params=params, 
                timeout=Config.TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' not in data or not data['data']:
                logger.error("API 響應中沒有歷史數據")
                return []
            
            historical_data = []
            for item in data['data']:
                historical_data.append({
                    'date': datetime.fromtimestamp(int(item['timestamp'])).isoformat(),
                    'index_value': int(item['value']),
                    'sentiment': item['value_classification'],
                    'timestamp': item['timestamp']
                })
            
            logger.info(f"成功獲取 {len(historical_data)} 天的歷史數據")
            return historical_data
            
        except Exception as e:
            logger.error(f"獲取歷史數據失敗: {str(e)}")
            return []
    
    def analyze_trend(self, days=7):
        """
        分析最近幾天的趨勢
        
        Args:
            days (int): 分析的天數
        
        Returns:
            dict: 趨勢分析結果
        """
        historical_data = self.get_historical_data(days)
        
        if len(historical_data) < 2:
            return None
        
        # 計算趨勢
        current_value = historical_data[0]['index_value']
        previous_value = historical_data[-1]['index_value']
        change = current_value - previous_value
        change_percent = (change / previous_value) * 100 if previous_value != 0 else 0
        
        # 計算平均值
        avg_value = sum(item['index_value'] for item in historical_data) / len(historical_data)
        
        # 判斷趨勢方向
        if change > 5:
            trend = "上升"
        elif change < -5:
            trend = "下降"
        else:
            trend = "穩定"
        
        return {
            'current_value': current_value,
            'previous_value': previous_value,
            'change': change,
            'change_percent': round(change_percent, 2),
            'average_value': round(avg_value, 2),
            'trend': trend,
            'analysis_period': f"{days} 天",
            'data_points': len(historical_data)
        }
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self.session, 'close'):
            self.session.close() 