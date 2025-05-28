import os
from loguru import logger
from config import Config

def setup_logger():
    """設置日誌配置"""
    # 創建日誌目錄
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    
    # 移除默認處理器
    logger.remove()
    
    # 添加控制台輸出
    logger.add(
        sink=lambda msg: print(msg, end=""),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # 添加文件輸出
    logger.add(
        f"{Config.LOG_DIR}/app.log",
        rotation="1 day",
        retention="7 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG"
    )
    
    return logger

# 初始化日誌
setup_logger() 