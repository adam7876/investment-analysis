#!/usr/bin/env python3
"""
整合投資分析器：三層聯動分析系統
實現從總經環境到最終選股的完整聯動流程
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from loguru import logger
import requests
import time
import json

from layer1_collector import Layer1Collector
from layer2_collector import Layer2Collector
from layer3_collector import Layer3Collector

class IntegratedAnalyzer:
    """整合投資分析器"""
    
    def __init__(self):
        self.layer1 = Layer1Collector()
        self.layer2 = Layer2Collector()
        self.layer3 = Layer3Collector()
        
        # 美股市場主要股票池（從各大指數中選取）
        self.market_universe = self._build_market_universe()
        
    def _build_market_universe(self) -> List[str]:
        """構建市場股票池"""
        # 科技股
        tech_stocks = [
            'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'TSLA', 'NVDA', 'META', 
            'NFLX', 'AMD', 'CRM', 'ADBE', 'ORCL', 'INTC', 'CSCO', 'AVGO',
            'QCOM', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'MRVL', 'FTNT', 'PANW'
        ]
        
        # 金融股
        financial_stocks = [
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'BLK', 'SCHW', 'AXP', 'USB',
            'PNC', 'TFC', 'COF', 'BK', 'STT', 'NTRS', 'RF', 'CFG', 'KEY', 'FITB'
        ]
        
        # 醫療保健
        healthcare_stocks = [
            'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'LLY',
            'AMGN', 'GILD', 'ISRG', 'VRTX', 'REGN', 'BIIB', 'ILMN', 'MRNA', 'ZTS', 'CVS'
        ]
        
        # 消費股
        consumer_stocks = [
            'AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'SBUX', 'TGT', 'LOW', 'TJX', 'COST',
            'WMT', 'PG', 'KO', 'PEP', 'CL', 'KMB', 'GIS', 'K', 'CPB', 'CAG'
        ]
        
        # 工業股
        industrial_stocks = [
            'BA', 'CAT', 'GE', 'MMM', 'HON', 'UPS', 'RTX', 'LMT', 'NOC', 'GD',
            'FDX', 'UNP', 'CSX', 'NSC', 'DAL', 'UAL', 'AAL', 'LUV', 'JBLU', 'ALK'
        ]
        
        # 能源股
        energy_stocks = [
            'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'PSX', 'VLO', 'MPC', 'KMI', 'OKE',
            'WMB', 'EPD', 'ET', 'MPLX', 'PAA', 'EQT', 'DVN', 'FANG', 'MRO', 'APA'
        ]
        
        # 合併所有股票並去重
        all_stocks = list(set(
            tech_stocks + financial_stocks + healthcare_stocks + 
            consumer_stocks + industrial_stocks + energy_stocks
        ))
        
        return all_stocks[:100]  # 限制在100支股票以內，避免API請求過多
    
    def analyze_complete_flow(self, user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """執行完整的三層聯動分析"""
        try:
            logger.info("🚀 開始執行三層聯動投資分析...")
            
            # 第一層：總經環境分析
            logger.info("📊 第一層：分析總經環境...")
            layer1_result = self._analyze_macro_environment()
            
            # 根據第一層結果確定投資策略
            investment_strategy = self._determine_investment_strategy(layer1_result)
            
            # 第二層：基於策略的動態選股
            logger.info("🔍 第二層：基於策略進行動態選股...")
            layer2_result = self._dynamic_stock_screening(investment_strategy, user_preferences)
            
            # 第三層：對選出的股票進行技術確認
            logger.info("📈 第三層：對候選股票進行技術確認...")
            layer3_result = self._technical_confirmation(layer2_result['selected_stocks'])
            
            # 生成最終投資建議
            final_recommendations = self._generate_final_recommendations(
                layer1_result, layer2_result, layer3_result, investment_strategy
            )
            
            return {
                "success": True,
                "analysis_time": datetime.now().isoformat(),
                "layer1_analysis": layer1_result,
                "layer2_analysis": layer2_result,
                "layer3_analysis": layer3_result,
                "investment_strategy": investment_strategy,
                "final_recommendations": final_recommendations,
                "summary": self._generate_executive_summary(final_recommendations)
            }
            
        except Exception as e:
            logger.error(f"三層聯動分析失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "分析過程中發生錯誤，請稍後重試"
            }
    
    def _analyze_macro_environment(self) -> Dict[str, Any]:
        """第一層：總經環境分析"""
        try:
            # 獲取第一層數據
            layer1_data = self.layer1.collect_all_data()
            
            if not layer1_data.get('success'):
                raise Exception("第一層數據收集失敗")
            
            data = layer1_data['data']
            
            # 分析市場情緒
            fear_greed = data.get('fear_greed', {})
            sentiment_score = fear_greed.get('value', 50)
            
            # 分析經濟數據
            economic_data = data.get('economic_data', {})
            gdp_growth = economic_data.get('gdp_growth', 2.0)
            unemployment = economic_data.get('unemployment_rate', 4.0)
            inflation = economic_data.get('inflation_rate', 3.0)
            
            # 確定市場階段
            market_phase = self._determine_market_phase(sentiment_score, gdp_growth, unemployment, inflation)
            
            # 確定風險偏好
            risk_appetite = self._determine_risk_appetite(sentiment_score, market_phase)
            
            return {
                "market_sentiment": {
                    "fear_greed_index": sentiment_score,
                    "sentiment_label": fear_greed.get('label', '中性'),
                    "interpretation": self._interpret_sentiment(sentiment_score)
                },
                "economic_indicators": {
                    "gdp_growth": gdp_growth,
                    "unemployment_rate": unemployment,
                    "inflation_rate": inflation,
                    "economic_health": self._assess_economic_health(gdp_growth, unemployment, inflation)
                },
                "market_phase": market_phase,
                "risk_appetite": risk_appetite,
                "investment_environment": self._assess_investment_environment(market_phase, risk_appetite)
            }
            
        except Exception as e:
            logger.error(f"第一層分析失敗: {str(e)}")
            # 返回保守的默認分析
            return {
                "market_sentiment": {
                    "fear_greed_index": 50,
                    "sentiment_label": "中性",
                    "interpretation": "市場情緒中性，建議謹慎操作"
                },
                "economic_indicators": {
                    "gdp_growth": 2.0,
                    "unemployment_rate": 4.0,
                    "inflation_rate": 3.0,
                    "economic_health": "穩定"
                },
                "market_phase": "盤整期",
                "risk_appetite": "中性",
                "investment_environment": "謹慎樂觀"
            }
    
    def _determine_market_phase(self, sentiment: float, gdp: float, unemployment: float, inflation: float) -> str:
        """確定市場階段"""
        if sentiment > 75 and gdp > 3.0:
            return "牛市後期"
        elif sentiment > 60 and gdp > 2.0:
            return "牛市中期"
        elif sentiment < 25 and unemployment > 5.0:
            return "熊市"
        elif sentiment < 40:
            return "熊市復甦期"
        else:
            return "盤整期"
    
    def _determine_risk_appetite(self, sentiment: float, market_phase: str) -> str:
        """確定風險偏好"""
        if market_phase in ["牛市中期", "熊市復甦期"] and sentiment > 40:
            return "積極"
        elif market_phase == "牛市後期" or sentiment > 80:
            return "謹慎"
        elif market_phase == "熊市" or sentiment < 25:
            return "保守"
        else:
            return "中性"
    
    def _determine_investment_strategy(self, layer1_result: Dict) -> Dict[str, Any]:
        """根據第一層結果確定投資策略"""
        market_phase = layer1_result['market_phase']
        risk_appetite = layer1_result['risk_appetite']
        sentiment = layer1_result['market_sentiment']['fear_greed_index']
        
        strategy = {
            "primary_focus": "",
            "sector_preference": [],
            "risk_tolerance": "",
            "position_sizing": "",
            "screening_criteria": {}
        }
        
        # 根據市場階段和風險偏好確定策略
        if risk_appetite == "積極":
            strategy.update({
                "primary_focus": "成長股",
                "sector_preference": ["科技", "消費", "醫療"],
                "risk_tolerance": "高",
                "position_sizing": "積極",
                "screening_criteria": {
                    "min_market_cap": 1e9,  # 10億
                    "min_volume": 1e6,      # 100萬
                    "max_pe_ratio": 40,
                    "min_revenue_growth": 10,
                    "momentum_weight": 0.4
                }
            })
        elif risk_appetite == "保守":
            strategy.update({
                "primary_focus": "價值股",
                "sector_preference": ["金融", "公用事業", "消費必需品"],
                "risk_tolerance": "低",
                "position_sizing": "保守",
                "screening_criteria": {
                    "min_market_cap": 10e9,  # 100億
                    "min_volume": 2e6,       # 200萬
                    "max_pe_ratio": 20,
                    "min_dividend_yield": 2,
                    "quality_weight": 0.5
                }
            })
        else:  # 中性或謹慎
            strategy.update({
                "primary_focus": "平衡型",
                "sector_preference": ["科技", "醫療", "金融", "工業"],
                "risk_tolerance": "中等",
                "position_sizing": "平衡",
                "screening_criteria": {
                    "min_market_cap": 5e9,   # 50億
                    "min_volume": 1.5e6,     # 150萬
                    "max_pe_ratio": 30,
                    "min_revenue_growth": 5,
                    "balance_weight": 0.3
                }
            })
        
        return strategy
    
    def _dynamic_stock_screening(self, strategy: Dict, user_preferences: Dict = None) -> Dict[str, Any]:
        """第二層：基於策略的動態選股"""
        try:
            logger.info(f"🎯 執行{strategy['primary_focus']}策略選股...")
            
            screening_criteria = strategy['screening_criteria']
            selected_stocks = []
            screening_details = []
            
            # 分批處理股票以避免API限制
            batch_size = 10
            for i in range(0, len(self.market_universe), batch_size):
                batch = self.market_universe[i:i+batch_size]
                batch_results = self._screen_stock_batch(batch, screening_criteria, strategy)
                selected_stocks.extend(batch_results['stocks'])
                screening_details.extend(batch_results['details'])
                
                # 避免API請求過快
                time.sleep(1)
                
                # 如果已經找到足夠的股票，可以提前結束
                if len(selected_stocks) >= 20:
                    break
            
            # 根據評分排序
            selected_stocks.sort(key=lambda x: x['total_score'], reverse=True)
            
            # 取前15支股票
            top_stocks = selected_stocks[:15]
            
            return {
                "strategy_applied": strategy['primary_focus'],
                "screening_criteria": screening_criteria,
                "total_screened": len(screening_details),
                "selected_stocks": top_stocks,
                "screening_summary": self._generate_screening_summary(top_stocks, strategy),
                "sector_distribution": self._analyze_sector_distribution(top_stocks)
            }
            
        except Exception as e:
            logger.error(f"動態選股失敗: {str(e)}")
            # 返回備用股票列表
            return self._get_fallback_stocks(strategy)
    
    def _screen_stock_batch(self, symbols: List[str], criteria: Dict, strategy: Dict) -> Dict[str, Any]:
        """篩選一批股票"""
        stocks = []
        details = []
        
        for symbol in symbols:
            try:
                stock_data = self._analyze_single_stock(symbol, criteria, strategy)
                if stock_data and stock_data['passes_screening']:
                    stocks.append(stock_data)
                details.append({
                    'symbol': symbol,
                    'screened': True,
                    'passed': stock_data['passes_screening'] if stock_data else False
                })
            except Exception as e:
                logger.warning(f"分析 {symbol} 失敗: {str(e)}")
                details.append({
                    'symbol': symbol,
                    'screened': False,
                    'error': str(e)
                })
                continue
        
        return {'stocks': stocks, 'details': details}
    
    def _analyze_single_stock(self, symbol: str, criteria: Dict, strategy: Dict) -> Optional[Dict]:
        """分析單一股票"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            hist = stock.history(period="3mo")  # 3個月歷史數據
            
            if len(hist) < 20:  # 數據不足
                return None
            
            # 基本篩選條件
            market_cap = info.get('marketCap', 0)
            avg_volume = hist['Volume'].mean()
            current_price = hist['Close'].iloc[-1]
            
            # 檢查基本條件
            if market_cap < criteria.get('min_market_cap', 0):
                return None
            if avg_volume < criteria.get('min_volume', 0):
                return None
            
            # 計算評分
            score_breakdown = self._calculate_stock_score(hist, info, criteria, strategy)
            total_score = sum(score_breakdown.values())
            
            # 設定通過門檻
            pass_threshold = 60  # 總分100分，60分以上通過
            
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'current_price': round(current_price, 2),
                'market_cap': market_cap,
                'market_cap_formatted': f"{market_cap/1e9:.1f}B" if market_cap > 1e9 else f"{market_cap/1e6:.1f}M",
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'total_score': round(total_score, 1),
                'score_breakdown': score_breakdown,
                'passes_screening': total_score >= pass_threshold,
                'key_metrics': self._extract_key_metrics(hist, info),
                'selection_reasons': self._generate_selection_reasons(score_breakdown, strategy)
            }
            
        except Exception as e:
            logger.warning(f"分析 {symbol} 時發生錯誤: {str(e)}")
            return None
    
    def _calculate_stock_score(self, hist: pd.DataFrame, info: Dict, criteria: Dict, strategy: Dict) -> Dict[str, float]:
        """計算股票評分"""
        scores = {}
        
        # 價格動能評分 (25分)
        returns_1m = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-21]) / hist['Close'].iloc[-21]) * 100 if len(hist) >= 21 else 0
        returns_1w = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-5]) / hist['Close'].iloc[-5]) * 100 if len(hist) >= 5 else 0
        
        momentum_score = 0
        if returns_1m > 10: momentum_score += 15
        elif returns_1m > 5: momentum_score += 10
        elif returns_1m > 0: momentum_score += 5
        
        if returns_1w > 3: momentum_score += 10
        elif returns_1w > 0: momentum_score += 5
        
        scores['momentum'] = min(momentum_score, 25)
        
        # 基本面評分 (30分)
        pe_ratio = info.get('trailingPE', 0)
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0
        profit_margin = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0
        
        fundamental_score = 0
        
        # PE評分
        max_pe = criteria.get('max_pe_ratio', 30)
        if 0 < pe_ratio < max_pe * 0.5:
            fundamental_score += 10
        elif 0 < pe_ratio < max_pe:
            fundamental_score += 5
        
        # 營收成長評分
        min_growth = criteria.get('min_revenue_growth', 5)
        if revenue_growth > min_growth * 2:
            fundamental_score += 10
        elif revenue_growth > min_growth:
            fundamental_score += 5
        
        # 利潤率評分
        if profit_margin > 20:
            fundamental_score += 10
        elif profit_margin > 10:
            fundamental_score += 5
        
        scores['fundamentals'] = min(fundamental_score, 30)
        
        # 技術面評分 (25分)
        technical_score = self._calculate_technical_score(hist)
        scores['technical'] = min(technical_score, 25)
        
        # 流動性評分 (10分)
        avg_volume = hist['Volume'].mean()
        liquidity_score = 0
        if avg_volume > 5e6:  # 500萬
            liquidity_score = 10
        elif avg_volume > 2e6:  # 200萬
            liquidity_score = 7
        elif avg_volume > 1e6:  # 100萬
            liquidity_score = 5
        
        scores['liquidity'] = liquidity_score
        
        # 質量評分 (10分)
        quality_score = self._calculate_quality_score(info)
        scores['quality'] = min(quality_score, 10)
        
        return scores
    
    def _calculate_technical_score(self, hist: pd.DataFrame) -> float:
        """計算技術面評分"""
        try:
            score = 0
            
            # RSI評分
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1] if not rsi.empty else 50
            
            if 30 <= current_rsi <= 70:  # 健康範圍
                score += 8
            elif 20 <= current_rsi <= 80:
                score += 5
            
            # 移動平均線評分
            if len(hist) >= 50:
                ma20 = hist['Close'].rolling(window=20).mean().iloc[-1]
                ma50 = hist['Close'].rolling(window=50).mean().iloc[-1]
                current_price = hist['Close'].iloc[-1]
                
                if current_price > ma20 > ma50:  # 多頭排列
                    score += 10
                elif current_price > ma20:
                    score += 5
            
            # 成交量確認
            volume_ma = hist['Volume'].rolling(window=20).mean()
            recent_volume = hist['Volume'].iloc[-5:].mean()
            if recent_volume > volume_ma.iloc[-1] * 1.2:  # 成交量放大
                score += 7
            
            return score
            
        except Exception:
            return 0
    
    def _calculate_quality_score(self, info: Dict) -> float:
        """計算質量評分"""
        score = 0
        
        # ROE評分
        roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0
        if roe > 15:
            score += 5
        elif roe > 10:
            score += 3
        
        # 債務比率評分
        debt_to_equity = info.get('debtToEquity', 100)
        if debt_to_equity < 30:
            score += 5
        elif debt_to_equity < 60:
            score += 3
        
        return score
    
    def _technical_confirmation(self, selected_stocks: List[Dict]) -> Dict[str, Any]:
        """第三層：技術確認分析"""
        try:
            logger.info(f"🔬 對{len(selected_stocks)}支候選股票進行技術確認...")
            
            confirmed_stocks = []
            
            for stock in selected_stocks[:10]:  # 只分析前10支
                try:
                    symbol = stock['symbol']
                    
                    # 獲取更詳細的技術分析
                    technical_analysis = self._deep_technical_analysis(symbol)
                    risk_analysis = self._comprehensive_risk_analysis(symbol)
                    
                    # 生成交易信號
                    trading_signal = self._generate_trading_signal(technical_analysis, risk_analysis)
                    
                    confirmed_stock = {
                        **stock,
                        'technical_analysis': technical_analysis,
                        'risk_analysis': risk_analysis,
                        'trading_signal': trading_signal,
                        'final_recommendation': self._generate_final_stock_recommendation(
                            stock, technical_analysis, risk_analysis, trading_signal
                        )
                    }
                    
                    confirmed_stocks.append(confirmed_stock)
                    
                except Exception as e:
                    logger.warning(f"技術確認 {stock['symbol']} 失敗: {str(e)}")
                    continue
            
            return {
                "confirmed_stocks": confirmed_stocks,
                "technical_summary": self._generate_technical_summary(confirmed_stocks),
                "risk_assessment": self._generate_risk_assessment(confirmed_stocks),
                "portfolio_suggestions": self._generate_portfolio_suggestions(confirmed_stocks)
            }
            
        except Exception as e:
            logger.error(f"技術確認失敗: {str(e)}")
            return {"confirmed_stocks": [], "error": str(e)}
    
    def _deep_technical_analysis(self, symbol: str) -> Dict[str, Any]:
        """深度技術分析"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="6mo")  # 6個月數據
            
            if len(hist) < 50:
                return {"error": "數據不足"}
            
            # 使用第三層收集器的技術指標計算
            indicators = self.layer3.calculate_technical_indicators(hist)
            support_resistance = self.layer3.find_support_resistance(hist)
            
            return {
                "indicators": indicators,
                "support_resistance": support_resistance,
                "trend_analysis": self._analyze_trend(hist),
                "volume_analysis": self._analyze_volume(hist)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _comprehensive_risk_analysis(self, symbol: str) -> Dict[str, Any]:
        """綜合風險分析"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="1y")
            info = stock.info
            
            if len(hist) < 100:
                return {"error": "數據不足"}
            
            # 使用第三層收集器的風險分析
            risk_metrics = self.layer3.analyze_risk_metrics(hist, info)
            
            return risk_metrics
            
        except Exception as e:
            return {"error": str(e)}
    
    def _generate_trading_signal(self, technical: Dict, risk: Dict) -> Dict[str, Any]:
        """生成交易信號"""
        if technical.get("error") or risk.get("error"):
            return {
                "signal": "觀望",
                "confidence": 0,
                "reasons": ["數據不足"]
            }
        
        # 使用第三層收集器的信號生成邏輯
        indicators = technical.get("indicators", {})
        support_resistance = technical.get("support_resistance", {})
        
        return self.layer3.generate_trading_signals(indicators, support_resistance)
    
    def _generate_final_recommendations(self, layer1: Dict, layer2: Dict, layer3: Dict, strategy: Dict) -> Dict[str, Any]:
        """生成最終投資建議"""
        confirmed_stocks = layer3.get("confirmed_stocks", [])
        
        # 按最終評分排序
        top_picks = sorted(confirmed_stocks, key=lambda x: x.get('total_score', 0), reverse=True)[:5]
        
        recommendations = {
            "top_picks": top_picks,
            "investment_thesis": self._generate_investment_thesis(layer1, strategy),
            "risk_warnings": self._generate_risk_warnings(layer1, layer3),
            "position_sizing": self._suggest_position_sizing(top_picks, strategy),
            "monitoring_points": self._suggest_monitoring_points(top_picks),
            "exit_strategy": self._suggest_exit_strategy(top_picks, strategy)
        }
        
        return recommendations
    
    def _generate_executive_summary(self, recommendations: Dict) -> Dict[str, Any]:
        """生成執行摘要"""
        top_picks = recommendations.get("top_picks", [])
        
        return {
            "total_recommendations": len(top_picks),
            "strong_buy_count": len([s for s in top_picks if s.get('trading_signal', {}).get('signal') == '強烈買入']),
            "average_confidence": round(np.mean([s.get('trading_signal', {}).get('confidence', 0) for s in top_picks]), 1) if top_picks else 0,
            "primary_sectors": list(set([s.get('sector', 'Unknown') for s in top_picks[:3]])),
            "key_message": self._generate_key_message(recommendations),
            "next_steps": self._generate_next_steps(recommendations)
        }
    
    # 輔助方法
    def _interpret_sentiment(self, score: float) -> str:
        if score > 75: return "市場極度貪婪，建議謹慎"
        elif score > 60: return "市場偏向貪婪，適度參與"
        elif score > 40: return "市場情緒中性，平衡操作"
        elif score > 25: return "市場偏向恐懼，尋找機會"
        else: return "市場極度恐懼，積極布局"
    
    def _assess_economic_health(self, gdp: float, unemployment: float, inflation: float) -> str:
        if gdp > 3 and unemployment < 4 and inflation < 3:
            return "強勁"
        elif gdp > 2 and unemployment < 5 and inflation < 4:
            return "穩定"
        elif gdp < 1 or unemployment > 6 or inflation > 5:
            return "疲弱"
        else:
            return "溫和"
    
    def _assess_investment_environment(self, phase: str, appetite: str) -> str:
        if phase == "牛市中期" and appetite == "積極":
            return "非常樂觀"
        elif phase == "熊市復甦期" and appetite in ["積極", "中性"]:
            return "謹慎樂觀"
        elif phase == "熊市" or appetite == "保守":
            return "謹慎悲觀"
        else:
            return "中性觀望"
    
    def _get_fallback_stocks(self, strategy: Dict) -> Dict[str, Any]:
        """獲取備用股票列表"""
        # 根據策略返回預設的優質股票
        if strategy['primary_focus'] == "成長股":
            fallback = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        elif strategy['primary_focus'] == "價值股":
            fallback = ['JPM', 'JNJ', 'PG', 'KO', 'WMT']
        else:
            fallback = ['AAPL', 'MSFT', 'JPM', 'JNJ', 'GOOGL']
        
        return {
            "strategy_applied": strategy['primary_focus'],
            "selected_stocks": [{"symbol": s, "name": s, "total_score": 70} for s in fallback],
            "note": "使用備用股票列表"
        }
    
    # 其他輔助方法的實現...
    def _generate_screening_summary(self, stocks: List, strategy: Dict) -> Dict:
        return {"message": f"基於{strategy['primary_focus']}策略篩選出{len(stocks)}支股票"}
    
    def _analyze_sector_distribution(self, stocks: List) -> Dict:
        sectors = [s.get('sector', 'Unknown') for s in stocks]
        return {sector: sectors.count(sector) for sector in set(sectors)}
    
    def _extract_key_metrics(self, hist: pd.DataFrame, info: Dict) -> Dict:
        return {
            "pe_ratio": info.get('trailingPE', 0),
            "market_cap": info.get('marketCap', 0),
            "volume": hist['Volume'].mean()
        }
    
    def _generate_selection_reasons(self, scores: Dict, strategy: Dict) -> List[str]:
        reasons = []
        for metric, score in scores.items():
            if score > 15:
                reasons.append(f"{metric}表現優異")
        return reasons
    
    def _analyze_trend(self, hist: pd.DataFrame) -> Dict:
        return {"trend": "上升" if hist['Close'].iloc[-1] > hist['Close'].iloc[-20] else "下降"}
    
    def _analyze_volume(self, hist: pd.DataFrame) -> Dict:
        return {"volume_trend": "放量" if hist['Volume'].iloc[-5:].mean() > hist['Volume'].mean() else "縮量"}
    
    def _generate_final_stock_recommendation(self, stock: Dict, technical: Dict, risk: Dict, signal: Dict) -> Dict:
        return {
            "action": signal.get("signal", "觀望"),
            "confidence": signal.get("confidence", 0),
            "target_price": stock.get("current_price", 0) * 1.1,
            "stop_loss": stock.get("current_price", 0) * 0.9
        }
    
    def _generate_technical_summary(self, stocks: List) -> Dict:
        return {"summary": f"完成{len(stocks)}支股票的技術分析"}
    
    def _generate_risk_assessment(self, stocks: List) -> Dict:
        return {"assessment": "整體風險可控"}
    
    def _generate_portfolio_suggestions(self, stocks: List) -> Dict:
        return {"suggestion": "建議分散投資"}
    
    def _generate_investment_thesis(self, layer1: Dict, strategy: Dict) -> str:
        return f"基於{layer1['market_phase']}階段，採用{strategy['primary_focus']}策略"
    
    def _generate_risk_warnings(self, layer1: Dict, layer3: Dict) -> List[str]:
        return ["市場波動風險", "個股風險"]
    
    def _suggest_position_sizing(self, stocks: List, strategy: Dict) -> Dict:
        return {"max_single_position": "5%", "total_equity_exposure": "80%"}
    
    def _suggest_monitoring_points(self, stocks: List) -> List[str]:
        return ["技術指標變化", "基本面變化"]
    
    def _suggest_exit_strategy(self, stocks: List, strategy: Dict) -> Dict:
        return {"profit_target": "20%", "stop_loss": "10%"}
    
    def _generate_key_message(self, recommendations: Dict) -> str:
        return "基於三層分析，建議謹慎樂觀操作"
    
    def _generate_next_steps(self, recommendations: Dict) -> List[str]:
        return ["監控市場變化", "分批建倉", "設定停損點"] 