#!/usr/bin/env python3
"""
Web介面功能測試腳本
"""

import requests
import json
import time
from loguru import logger

def test_web_interface():
    """測試Web介面功能"""
    base_url = "http://localhost:5000"
    
    logger.info("🧪 開始測試Web介面功能...")
    
    # 測試結果
    results = {
        'homepage': False,
        'dashboard': False,
        'layer2': False,
        'layer3': False,
        'api_summary': False,
        'api_collect': False
    }
    
    try:
        # 測試首頁
        logger.info("📱 測試首頁...")
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200 and "美股投資分析系統" in response.text:
            results['homepage'] = True
            logger.info("✅ 首頁測試通過")
        else:
            logger.error(f"❌ 首頁測試失敗: {response.status_code}")
        
        # 測試儀表板
        logger.info("📊 測試儀表板...")
        response = requests.get(f"{base_url}/dashboard", timeout=10)
        if response.status_code == 200 and "儀表板" in response.text:
            results['dashboard'] = True
            logger.info("✅ 儀表板測試通過")
        else:
            logger.error(f"❌ 儀表板測試失敗: {response.status_code}")
        
        # 測試第二層頁面
        logger.info("📰 測試第二層頁面...")
        response = requests.get(f"{base_url}/layer2", timeout=10)
        if response.status_code == 200 and "事件選股" in response.text:
            results['layer2'] = True
            logger.info("✅ 第二層頁面測試通過")
        else:
            logger.error(f"❌ 第二層頁面測試失敗: {response.status_code}")
        
        # 測試第三層頁面
        logger.info("📈 測試第三層頁面...")
        response = requests.get(f"{base_url}/layer3", timeout=10)
        if response.status_code == 200 and "技術確認" in response.text:
            results['layer3'] = True
            logger.info("✅ 第三層頁面測試通過")
        else:
            logger.error(f"❌ 第三層頁面測試失敗: {response.status_code}")
        
        # 測試API - 摘要
        logger.info("🔌 測試API摘要端點...")
        response = requests.get(f"{base_url}/api/layer1/summary", timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                results['api_summary'] = True
                logger.info("✅ API摘要測試通過")
                logger.info(f"📊 市場情緒: {data['data']['summary'].get('market_sentiment', 'N/A')}")
                logger.info(f"💡 投資建議: {data['data']['summary'].get('investment_recommendation', 'N/A')}")
            else:
                logger.warning(f"⚠️ API摘要返回錯誤: {data.get('error', 'Unknown')}")
        else:
            logger.error(f"❌ API摘要測試失敗: {response.status_code}")
        
        # 測試API - 數據收集
        logger.info("🔄 測試API數據收集端點...")
        response = requests.post(f"{base_url}/api/layer1/collect", timeout=60)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                results['api_collect'] = True
                logger.info("✅ API數據收集測試通過")
            else:
                logger.warning(f"⚠️ API數據收集返回錯誤: {data.get('error', 'Unknown')}")
        else:
            logger.error(f"❌ API數據收集測試失敗: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        logger.error("❌ 無法連接到Web服務器，請確認服務器已啟動")
        return False
    except Exception as e:
        logger.error(f"❌ 測試過程中發生錯誤: {str(e)}")
        return False
    
    # 輸出測試結果
    logger.info("\n" + "="*50)
    logger.info("📋 測試結果摘要:")
    logger.info("="*50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ 通過" if result else "❌ 失敗"
        logger.info(f"{test_name:15} : {status}")
    
    logger.info(f"\n🎯 總體結果: {passed}/{total} 項測試通過")
    
    if passed == total:
        logger.info("🎉 所有測試都通過了！Web介面運行正常")
        return True
    else:
        logger.warning(f"⚠️ 有 {total - passed} 項測試失敗")
        return False

def main():
    """主函數"""
    logger.info("🚀 Web介面測試工具")
    logger.info("請確保Web服務器已在 http://localhost:5000 啟動")
    
    # 等待用戶確認
    input("\n按 Enter 鍵開始測試...")
    
    success = test_web_interface()
    
    if success:
        logger.info("\n✅ 測試完成！您可以在瀏覽器中訪問 http://localhost:5000")
    else:
        logger.info("\n❌ 測試未完全通過，請檢查錯誤信息")

if __name__ == '__main__':
    main() 