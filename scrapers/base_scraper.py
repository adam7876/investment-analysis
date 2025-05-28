import time
import random
import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from loguru import logger
from config import Config

# 嘗試導入selenium，如果失敗則設為None（Railway環境可能沒有）
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import undetected_chromedriver as uc
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logger.warning("Selenium不可用，將只使用requests進行爬蟲")

class BaseScraper(ABC):
    """基礎爬蟲類"""
    
    def __init__(self):
        self.session = requests.Session()
        self.driver = None
        self._setup_session()
    
    def _setup_session(self):
        """設置請求會話"""
        headers = {
            'User-Agent': random.choice(Config.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(headers)
    
    def get_page(self, url, use_selenium=False):
        """獲取網頁內容"""
        logger.info(f"正在獲取頁面: {url}")
        
        try:
            if use_selenium and SELENIUM_AVAILABLE:
                return self._get_page_selenium(url)
            else:
                if use_selenium and not SELENIUM_AVAILABLE:
                    logger.warning("Selenium不可用，改用requests")
                return self._get_page_requests(url)
        except Exception as e:
            logger.error(f"獲取頁面失敗: {url}, 錯誤: {str(e)}")
            return None
    
    def _get_page_requests(self, url):
        """使用 requests 獲取頁面"""
        for attempt in range(Config.MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=Config.TIMEOUT)
                response.raise_for_status()
                
                # 隨機延遲
                time.sleep(random.uniform(1, Config.REQUEST_DELAY))
                
                return BeautifulSoup(response.content, 'html.parser')
                
            except requests.RequestException as e:
                logger.warning(f"請求失敗 (嘗試 {attempt + 1}/{Config.MAX_RETRIES}): {str(e)}")
                if attempt < Config.MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)  # 指數退避
                else:
                    raise
    
    def _get_page_selenium(self, url):
        """使用 Selenium 獲取頁面"""
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium不可用")
            
        if not self.driver:
            self._setup_driver()
        
        try:
            self.driver.get(url)
            # 等待頁面載入
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 隨機延遲
            time.sleep(random.uniform(2, 5))
            
            return BeautifulSoup(self.driver.page_source, 'html.parser')
            
        except Exception as e:
            logger.error(f"Selenium 獲取頁面失敗: {str(e)}")
            raise
    
    def _setup_driver(self):
        """設置 Chrome 驅動"""
        if not SELENIUM_AVAILABLE:
            raise ImportError("Selenium不可用")
            
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument(f'--user-agent={random.choice(Config.USER_AGENTS)}')
            
            self.driver = uc.Chrome(options=options)
            logger.info("Chrome 驅動初始化成功")
            
        except Exception as e:
            logger.error(f"Chrome 驅動初始化失敗: {str(e)}")
            raise
    
    def close(self):
        """關閉資源"""
        if self.driver:
            self.driver.quit()
            logger.info("Chrome 驅動已關閉")
    
    @abstractmethod
    def scrape(self):
        """抽象方法：具體的爬蟲邏輯"""
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 