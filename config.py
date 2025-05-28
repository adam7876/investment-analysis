import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

class Config:
    """配置管理類"""
    
    # API 密鑰
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', '')
    FRED_API_KEY = os.getenv('FRED_API_KEY', 'demo')
    
    # 爬蟲設定
    REQUEST_DELAY = 2  # 請求間隔秒數
    MAX_RETRIES = 3    # 最大重試次數
    TIMEOUT = 30       # 請求超時時間
    
    # 用戶代理
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
    
    # 數據存儲路徑
    DATA_DIR = 'data'
    CACHE_DIR = 'cache'
    LOG_DIR = 'logs'
    
    # 網站 URL
    URLS = {
        'macromicro_gdp': 'https://www.macromicro.me/collections/2/us-gdp-relative/12/real-gdp-growth',
        'macromicro_cpi': 'https://www.macromicro.me/collections/5/us-price-relative/68/cpi-items',
        'cnn_fear_greed': 'https://edition.cnn.com/markets/fear-and-greed',
        'cme_fedwatch': 'https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html',
        'investing_nonfarm': 'https://hk.investing.com/economic-calendar/nonfarm-payrolls-227'
    } 