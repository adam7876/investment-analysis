#!/usr/bin/env python3
"""
第二層數據收集器：事件與產業選股（催化劑層）
追蹤財經事件、新聞情緒和產業動態，發掘投資機會和風險
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from loguru import logger
import yfinance as yf
import pandas as pd
from textblob import TextBlob
import time

class Layer2Collector:
    """第二層數據收集器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # 美股11大產業ETF代碼
        self.sector_etfs = {
            'XLK': '科技',
            'XLF': '金融',
            'XLV': '醫療保健',
            'XLY': '非必需消費',
            'XLP': '必需消費',
            'XLE': '能源',
            'XLI': '工業',
            'XLB': '原材料',
            'XLRE': '房地產',
            'XLU': '公用事業',
            'XLC': '通訊服務'
        }
        
    def get_economic_calendar(self) -> Dict[str, Any]:
        """獲取財經事件日曆"""
        try:
            logger.info("📅 正在獲取財經事件日曆...")
            
            # 使用Trading Economics API (免費版本)
            events = []
            
            # 模擬一些重要的財經事件
            today = datetime.now()
            
            # 聯準會會議日期 (通常每6-8週一次)
            fed_meetings = [
                {"date": "2025-01-29", "event": "聯準會利率決議", "importance": "高"},
                {"date": "2025-03-19", "event": "聯準會利率決議", "importance": "高"},
                {"date": "2025-05-01", "event": "聯準會利率決議", "importance": "高"},
            ]
            
            # 重要經濟數據
            economic_data = [
                {"date": "2025-01-31", "event": "GDP年化季率", "importance": "高"},
                {"date": "2025-02-07", "event": "非農就業人數", "importance": "高"},
                {"date": "2025-02-13", "event": "CPI年率", "importance": "高"},
                {"date": "2025-02-14", "event": "PPI年率", "importance": "中"},
                {"date": "2025-02-28", "event": "PCE物價指數", "importance": "高"},
            ]
            
            # 財報季重要日期
            earnings_season = [
                {"date": "2025-01-15", "event": "大型銀行財報週", "importance": "中"},
                {"date": "2025-01-30", "event": "科技巨頭財報週", "importance": "高"},
                {"date": "2025-04-15", "event": "Q1財報季開始", "importance": "中"},
            ]
            
            all_events = fed_meetings + economic_data + earnings_season
            
            # 過濾未來30天的事件
            future_events = []
            for event in all_events:
                event_date = datetime.strptime(event["date"], "%Y-%m-%d")
                if event_date >= today and event_date <= today + timedelta(days=30):
                    days_until = (event_date - today).days
                    event["days_until"] = days_until
                    future_events.append(event)
            
            # 按日期排序
            future_events.sort(key=lambda x: x["days_until"])
            
            return {
                "success": True,
                "events": future_events[:10],  # 返回最近10個事件
                "total_events": len(future_events),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"財經事件日曆獲取失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "events": []
            }
    
    def get_news_sentiment(self) -> Dict[str, Any]:
        """獲取新聞情緒分析"""
        try:
            logger.info("📰 正在分析新聞情緒...")
            
            # 使用Yahoo Finance獲取市場新聞
            tickers = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA']
            all_news = []
            
            for ticker in tickers[:3]:  # 限制請求數量
                try:
                    stock = yf.Ticker(ticker)
                    news = stock.news
                    
                    for article in news[:5]:  # 每個股票取5篇新聞
                        # 簡單的情緒分析
                        title = article.get('title', '')
                        summary = article.get('summary', '')
                        
                        # 使用TextBlob進行情緒分析
                        text = f"{title} {summary}"
                        blob = TextBlob(text)
                        sentiment_score = blob.sentiment.polarity
                        
                        # 分類情緒
                        if sentiment_score > 0.1:
                            sentiment = "正面"
                        elif sentiment_score < -0.1:
                            sentiment = "負面"
                        else:
                            sentiment = "中性"
                        
                        all_news.append({
                            "title": title,
                            "summary": summary[:200] + "..." if len(summary) > 200 else summary,
                            "sentiment": sentiment,
                            "sentiment_score": round(sentiment_score, 3),
                            "ticker": ticker,
                            "published": article.get('providerPublishTime', int(time.time())),
                            "url": article.get('link', '')
                        })
                    
                    time.sleep(0.5)  # 避免請求過快
                    
                except Exception as e:
                    logger.warning(f"獲取 {ticker} 新聞失敗: {str(e)}")
                    continue
            
            # 計算整體情緒
            if all_news:
                sentiment_scores = [news['sentiment_score'] for news in all_news]
                avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
                
                positive_count = len([s for s in sentiment_scores if s > 0.1])
                negative_count = len([s for s in sentiment_scores if s < -0.1])
                neutral_count = len(sentiment_scores) - positive_count - negative_count
                
                overall_sentiment = "正面" if avg_sentiment > 0.1 else "負面" if avg_sentiment < -0.1 else "中性"
            else:
                avg_sentiment = 0
                positive_count = negative_count = neutral_count = 0
                overall_sentiment = "中性"
            
            return {
                "success": True,
                "overall_sentiment": overall_sentiment,
                "average_score": round(avg_sentiment, 3),
                "sentiment_distribution": {
                    "positive": positive_count,
                    "negative": negative_count,
                    "neutral": neutral_count
                },
                "news": all_news[:15],  # 返回最新15篇新聞
                "total_analyzed": len(all_news),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"新聞情緒分析失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "overall_sentiment": "中性",
                "news": []
            }
    
    def get_sector_rotation(self) -> Dict[str, Any]:
        """獲取產業輪動分析"""
        try:
            logger.info("🏭 正在分析產業輪動...")
            
            sector_data = []
            
            for etf_symbol, sector_name in self.sector_etfs.items():
                try:
                    # 獲取ETF數據
                    etf = yf.Ticker(etf_symbol)
                    hist = etf.history(period="1mo")  # 最近一個月
                    
                    if len(hist) > 0:
                        # 計算績效
                        current_price = hist['Close'].iloc[-1]
                        start_price = hist['Close'].iloc[0]
                        performance_1m = ((current_price - start_price) / start_price) * 100
                        
                        # 計算波動率
                        returns = hist['Close'].pct_change().dropna()
                        volatility = returns.std() * (252 ** 0.5) * 100  # 年化波動率
                        
                        # 計算相對強弱 (vs SPY)
                        spy = yf.Ticker('SPY')
                        spy_hist = spy.history(period="1mo")
                        if len(spy_hist) > 0:
                            spy_performance = ((spy_hist['Close'].iloc[-1] - spy_hist['Close'].iloc[0]) / spy_hist['Close'].iloc[0]) * 100
                            relative_strength = performance_1m - spy_performance
                        else:
                            relative_strength = 0
                        
                        sector_data.append({
                            "sector": sector_name,
                            "symbol": etf_symbol,
                            "performance_1m": round(performance_1m, 2),
                            "volatility": round(volatility, 2),
                            "relative_strength": round(relative_strength, 2),
                            "current_price": round(current_price, 2)
                        })
                    
                    time.sleep(0.2)  # 避免請求過快
                    
                except Exception as e:
                    logger.warning(f"獲取 {etf_symbol} 數據失敗: {str(e)}")
                    continue
            
            # 排序：按相對強弱排序
            sector_data.sort(key=lambda x: x['relative_strength'], reverse=True)
            
            # 分析趨勢
            if sector_data:
                top_sectors = sector_data[:3]
                bottom_sectors = sector_data[-3:]
                
                analysis = {
                    "trend": "科技主導" if any("科技" in s["sector"] for s in top_sectors) else "價值輪動",
                    "top_performing": [s["sector"] for s in top_sectors],
                    "underperforming": [s["sector"] for s in bottom_sectors],
                    "market_breadth": "強勢" if len([s for s in sector_data if s["relative_strength"] > 0]) > 6 else "弱勢"
                }
            else:
                analysis = {
                    "trend": "數據不足",
                    "top_performing": [],
                    "underperforming": [],
                    "market_breadth": "未知"
                }
            
            return {
                "success": True,
                "sectors": sector_data,
                "analysis": analysis,
                "total_sectors": len(sector_data),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"產業輪動分析失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "sectors": []
            }
    
    def get_stock_screener(self) -> Dict[str, Any]:
        """獲取選股篩選結果"""
        try:
            logger.info("🔍 正在執行選股篩選...")
            
            # 熱門股票列表
            popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX']
            screened_stocks = []
            
            for symbol in popular_stocks[:5]:  # 限制數量
                try:
                    stock = yf.Ticker(symbol)
                    info = stock.info
                    hist = stock.history(period="5d")
                    
                    if len(hist) > 0:
                        # 計算指標
                        current_price = hist['Close'].iloc[-1]
                        volume_avg = hist['Volume'].mean()
                        price_change_5d = ((current_price - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
                        
                        # 獲取基本面數據
                        market_cap = info.get('marketCap', 0)
                        pe_ratio = info.get('trailingPE', 0)
                        
                        # 簡單評分系統
                        score = 0
                        reasons = []
                        
                        if price_change_5d > 5:
                            score += 2
                            reasons.append("近期強勢上漲")
                        elif price_change_5d > 2:
                            score += 1
                            reasons.append("溫和上漲")
                        
                        if volume_avg > 10000000:  # 高成交量
                            score += 1
                            reasons.append("高成交量")
                        
                        if 0 < pe_ratio < 25:  # 合理估值
                            score += 1
                            reasons.append("估值合理")
                        
                        screened_stocks.append({
                            "symbol": symbol,
                            "name": info.get('longName', symbol),
                            "current_price": round(current_price, 2),
                            "price_change_5d": round(price_change_5d, 2),
                            "market_cap": market_cap,
                            "pe_ratio": round(pe_ratio, 2) if pe_ratio else "N/A",
                            "score": score,
                            "reasons": reasons,
                            "recommendation": "買入" if score >= 3 else "觀察" if score >= 2 else "避免"
                        })
                    
                    time.sleep(0.3)
                    
                except Exception as e:
                    logger.warning(f"分析 {symbol} 失敗: {str(e)}")
                    continue
            
            # 按評分排序
            screened_stocks.sort(key=lambda x: x['score'], reverse=True)
            
            return {
                "success": True,
                "stocks": screened_stocks,
                "total_analyzed": len(screened_stocks),
                "buy_recommendations": len([s for s in screened_stocks if s["recommendation"] == "買入"]),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"選股篩選失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "stocks": []
            }
    
    def collect_all_data(self) -> Dict[str, Any]:
        """收集所有第二層數據"""
        logger.info("🚀 開始收集第二層數據...")
        
        start_time = datetime.now()
        
        # 收集各項數據
        economic_calendar = self.get_economic_calendar()
        news_sentiment = self.get_news_sentiment()
        sector_rotation = self.get_sector_rotation()
        stock_screener = self.get_stock_screener()
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # 計算成功率
        modules = [economic_calendar, news_sentiment, sector_rotation, stock_screener]
        success_count = sum(1 for module in modules if module.get("success", False))
        success_rate = (success_count / len(modules)) * 100
        
        return {
            "timestamp": datetime.now().isoformat(),
            "processing_time": round(processing_time, 2),
            "success_rate": round(success_rate, 1),
            "economic_calendar": economic_calendar,
            "news_sentiment": news_sentiment,
            "sector_rotation": sector_rotation,
            "stock_screener": stock_screener,
            "summary": {
                "total_events": economic_calendar.get("total_events", 0),
                "news_analyzed": news_sentiment.get("total_analyzed", 0),
                "sectors_analyzed": sector_rotation.get("total_sectors", 0),
                "stocks_screened": stock_screener.get("total_analyzed", 0),
                "overall_sentiment": news_sentiment.get("overall_sentiment", "中性"),
                "market_trend": sector_rotation.get("analysis", {}).get("trend", "未知")
            }
        }
    
    def get_summary_report(self) -> Dict[str, Any]:
        """獲取第二層摘要報告"""
        data = self.collect_all_data()
        
        # 生成投資建議
        sentiment = data["summary"]["overall_sentiment"]
        trend = data["summary"]["market_trend"]
        
        if sentiment == "正面" and "科技" in trend:
            investment_advice = "市場情緒正面，科技股主導，建議關注成長股機會"
            risk_level = "中等"
        elif sentiment == "負面":
            investment_advice = "市場情緒偏負面，建議謹慎操作，關注防禦性產業"
            risk_level = "偏高"
        else:
            investment_advice = "市場情緒中性，建議均衡配置，等待明確信號"
            risk_level = "中等"
        
        return {
            "layer": "第二層：事件與產業選股",
            "status": "運行中",
            "success_rate": data["success_rate"],
            "key_insights": {
                "market_sentiment": sentiment,
                "sector_trend": trend,
                "upcoming_events": data["economic_calendar"].get("total_events", 0),
                "investment_advice": investment_advice,
                "risk_level": risk_level
            },
            "data_sources": {
                "economic_calendar": data["economic_calendar"]["success"],
                "news_sentiment": data["news_sentiment"]["success"],
                "sector_rotation": data["sector_rotation"]["success"],
                "stock_screener": data["stock_screener"]["success"]
            },
            "last_updated": data["timestamp"]
        }

if __name__ == "__main__":
    collector = Layer2Collector()
    
    print("🚀 美股投資分析系統 - 第二層數據收集")
    print("=" * 50)
    
    # 收集數據
    data = collector.collect_all_data()
    
    # 顯示摘要
    summary = collector.get_summary_report()
    print(f"\n📊 第二層分析摘要:")
    print(f"成功率: {summary['success_rate']}%")
    print(f"市場情緒: {summary['key_insights']['market_sentiment']}")
    print(f"產業趨勢: {summary['key_insights']['sector_trend']}")
    print(f"投資建議: {summary['key_insights']['investment_advice']}")
    print(f"風險等級: {summary['key_insights']['risk_level']}")
    
    # 保存數據
    with open('logs/layer2_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 數據已保存到 logs/layer2_data.json") 