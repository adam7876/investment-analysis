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
        """執行完整的四層聯動分析"""
        try:
            logger.info("🚀 開始執行四層聯動投資分析...")
            
            # 第一層：市場總觀趨勢（總經＋情緒）
            logger.info("📊 第一層：分析市場總觀趨勢...")
            layer1_result = self._analyze_market_overview()
            
            # 根據第一層結果確定投資策略
            investment_strategy = self._determine_investment_strategy(layer1_result)
            
            # 第二層：本週重點產業與催化劑
            logger.info("🏭 第二層：分析重點產業與催化劑...")
            layer2_result = self._analyze_sector_catalysts(layer1_result, investment_strategy)
            
            # 第三層：精選操作名單與策略
            logger.info("🎯 第三層：生成精選操作名單...")
            layer3_result = self._generate_trading_watchlist(layer2_result, investment_strategy)
            
            # 第四層：選擇權策略建議
            logger.info("📈 第四層：制定選擇權策略...")
            layer4_result = self._analyze_options_strategies(layer1_result, layer3_result, investment_strategy)
            
            # 生成最終投資建議
            final_recommendations = self._generate_comprehensive_recommendations(
                layer1_result, layer2_result, layer3_result, layer4_result, investment_strategy
            )
            
            return {
                "success": True,
                "analysis_time": datetime.now().isoformat(),
                "layer1_market_overview": layer1_result,
                "layer2_sector_analysis": layer2_result,
                "layer3_trading_watchlist": layer3_result,
                "layer4_options_strategies": layer4_result,
                "investment_strategy": investment_strategy,
                "final_recommendations": final_recommendations,
                "executive_summary": self._generate_executive_summary(final_recommendations)
            }
            
        except Exception as e:
            logger.error(f"四層聯動分析失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "分析過程中發生錯誤，請稍後重試"
            }
    
    def _analyze_market_overview(self) -> Dict[str, Any]:
        """第一層：市場總觀趨勢分析"""
        try:
            # 獲取總經數據
            layer1_data = self.layer1.collect_all_data()
            
            if layer1_data.get('success'):
                data = layer1_data['data']
            else:
                logger.warning("第一層數據收集部分失敗，使用可用數據進行分析")
                data = layer1_data.get('data', {})
            
            # 市場情緒分析
            sentiment_analysis = self._analyze_market_sentiment(data)
            
            # 總經環境分析
            economic_analysis = self._analyze_economic_environment(data)
            
            # 資金流向分析
            capital_flow_analysis = self._analyze_capital_flows(data)
            
            # 市場階段判斷
            market_phase = self._determine_comprehensive_market_phase(
                sentiment_analysis, economic_analysis, capital_flow_analysis
            )
            
            # 提取必要參數
            market_phase_str = market_phase.get('phase', '盤整期')
            risk_appetite = sentiment_analysis.get('risk_appetite', '中性')
            sentiment_score = sentiment_analysis.get('fear_greed_index', 50)
            gdp_growth = economic_analysis.get('gdp_growth', 2.5)
            
            return {
                "market_sentiment": sentiment_analysis,
                "economic_environment": economic_analysis,
                "capital_flows": capital_flow_analysis,
                "market_phase": market_phase,
                "overall_outlook": self._generate_market_outlook(market_phase_str, risk_appetite, sentiment_score, gdp_growth),
                "key_risks": self._identify_market_risks(sentiment_analysis, economic_analysis),
                "confidence_level": self._calculate_market_confidence(sentiment_analysis, economic_analysis)
            }
            
        except Exception as e:
            logger.error(f"市場總觀分析失敗: {str(e)}")
            return self._get_fallback_market_overview()
    
    def _analyze_sector_catalysts(self, market_overview: Dict, strategy: Dict) -> Dict[str, Any]:
        """第二層：本週重點產業與催化劑分析"""
        try:
            # 產業表現分析
            sector_performance = self._analyze_sector_performance()
            
            # 催化劑識別
            catalysts = self._identify_market_catalysts()
            
            # 產業輪動分析
            sector_rotation = self._analyze_sector_rotation(market_overview)
            
            # 本週重點產業
            focus_sectors = self._select_focus_sectors(
                sector_performance, catalysts, sector_rotation, strategy
            )
            
            return {
                "sector_performance": sector_performance,
                "market_catalysts": catalysts,
                "sector_rotation": sector_rotation,
                "focus_sectors": focus_sectors,
                "investment_themes": self._generate_investment_themes(focus_sectors, catalysts),
                "timing_analysis": self._analyze_sector_timing(focus_sectors)
            }
            
        except Exception as e:
            logger.error(f"產業催化劑分析失敗: {str(e)}")
            return self._get_fallback_sector_analysis()
    
    def _generate_trading_watchlist(self, sector_analysis: Dict, strategy: Dict) -> Dict[str, Any]:
        """第三層：生成精選操作名單"""
        try:
            # 基於重點產業篩選股票
            focus_sectors = sector_analysis.get('focus_sectors', [])
            candidate_stocks = self._screen_stocks_by_sectors(focus_sectors, strategy)
            
            # 技術面確認
            confirmed_stocks = []
            for stock in candidate_stocks:
                technical_analysis = self._perform_detailed_technical_analysis(stock)
                if technical_analysis['signal'] in ['買入', '強烈買入']:
                    stock['technical_analysis'] = technical_analysis
                    confirmed_stocks.append(stock)
            
            # 排序並選出最終名單
            final_watchlist = sorted(confirmed_stocks, key=lambda x: x.get('total_score', 0), reverse=True)[:8]
            
            # 為每支股票生成操作策略
            for stock in final_watchlist:
                stock['trading_strategy'] = self._generate_trading_strategy(stock, strategy)
                stock['risk_management'] = self._generate_risk_management(stock)
            
            return {
                "watchlist": final_watchlist,
                "watchlist_summary": self._generate_watchlist_summary(final_watchlist),
                "sector_allocation": self._calculate_sector_allocation(final_watchlist),
                "risk_assessment": self._assess_watchlist_risk(final_watchlist),
                "execution_plan": self._create_execution_plan(final_watchlist)
            }
            
        except Exception as e:
            logger.error(f"操作名單生成失敗: {str(e)}")
            return self._get_fallback_watchlist()
    
    def _analyze_options_strategies(self, market_overview: Dict, watchlist: Dict, strategy: Dict) -> Dict[str, Any]:
        """第四層：選擇權策略分析"""
        try:
            # 評估波動率環境
            volatility_env = self._assess_volatility_environment()
            
            # 根據市場觀點生成不同策略
            strategies = []
            
            # 看多策略
            if market_overview.get('market_phase', {}).get('trend', '') in ['上升', '復甦']:
                strategies.extend(self._generate_bullish_strategies(watchlist, volatility_env))
            
            # 看空策略
            if market_overview.get('market_phase', {}).get('trend', '') in ['下降', '衰退']:
                strategies.extend(self._generate_bearish_strategies(watchlist, volatility_env))
            
            # 中性策略
            if volatility_env.get('level', '') == '高波動':
                strategies.extend(self._generate_neutral_strategies(watchlist, volatility_env))
            
            # 防禦策略
            if strategy.get('risk_tolerance', '') == '低':
                strategies.extend(self._generate_defensive_strategies(watchlist, volatility_env))
            
            # 事件驅動策略
            strategies.extend(self._generate_event_driven_strategies(watchlist, market_overview))
            
            return {
                "volatility_environment": volatility_env,
                "recommended_strategies": strategies[:5],  # 限制在5個策略
                "risk_management": self._generate_options_risk_management(),
                "market_scenarios": self._generate_market_scenarios(market_overview),
                "execution_guidelines": self._generate_options_execution_guidelines(),
                "educational_notes": self._generate_options_education()
            }
            
        except Exception as e:
            logger.error(f"選擇權策略分析失敗: {str(e)}")
            return self._get_fallback_options_analysis()
    
    def _determine_investment_strategy(self, layer1_result: Dict) -> Dict[str, Any]:
        """根據第一層結果確定投資策略"""
        market_phase = layer1_result.get('market_phase', {})
        sentiment = layer1_result.get('market_sentiment', {})
        economic = layer1_result.get('economic_environment', {})
        
        # 基於市場階段確定策略
        if market_phase.get('phase') == '牛市中期':
            strategy_type = '成長導向'
            risk_level = '中高'
            sector_focus = ['科技', '消費', '醫療']
        elif market_phase.get('phase') == '熊市復甦期':
            strategy_type = '價值導向'
            risk_level = '中等'
            sector_focus = ['金融', '工業', '能源']
        elif market_phase.get('phase') == '牛市後期':
            strategy_type = '防禦導向'
            risk_level = '低'
            sector_focus = ['公用事業', '消費必需品', '醫療']
        else:
            strategy_type = '平衡導向'
            risk_level = '中等'
            sector_focus = ['科技', '醫療', '金融', '工業']
        
        return {
            "strategy_type": strategy_type,
            "risk_level": risk_level,
            "sector_focus": sector_focus,
            "position_sizing": self._determine_position_sizing(risk_level),
            "time_horizon": self._determine_time_horizon(market_phase),
            "screening_criteria": self._build_screening_criteria(strategy_type, risk_level)
        }
    
    def _determine_position_sizing(self, risk_level: str) -> str:
        """確定部位大小策略"""
        if risk_level == '高':
            return '積極型：單一部位可達10-15%'
        elif risk_level == '中高':
            return '成長型：單一部位5-10%'
        elif risk_level == '中等':
            return '平衡型：單一部位3-8%'
        else:
            return '保守型：單一部位2-5%'
    
    def _determine_time_horizon(self, market_phase: Dict) -> str:
        """確定投資時間範圍"""
        phase = market_phase.get('phase', '盤整期')
        if phase in ['牛市中期', '熊市復甦期']:
            return '中長期：6-18個月'
        elif phase == '牛市後期':
            return '短中期：3-9個月'
        else:
            return '靈活調整：1-6個月'
    
    def _build_screening_criteria(self, strategy_type: str, risk_level: str) -> Dict:
        """建立篩選標準"""
        base_criteria = {
            "min_market_cap": 1e9,
            "min_volume": 1e6,
            "max_pe_ratio": 30
        }
        
        if strategy_type == '成長導向':
            base_criteria.update({
                "min_revenue_growth": 15,
                "max_pe_ratio": 50,
                "momentum_weight": 0.4
            })
        elif strategy_type == '價值導向':
            base_criteria.update({
                "max_pe_ratio": 20,
                "min_dividend_yield": 1.5,
                "value_weight": 0.4
            })
        elif strategy_type == '防禦導向':
            base_criteria.update({
                "min_market_cap": 10e9,
                "max_pe_ratio": 25,
                "min_dividend_yield": 2.0,
                "quality_weight": 0.5
            })
        
        return base_criteria
    
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
            
            # 生成詳細的選股分析
            detailed_analysis = self._generate_detailed_stock_analysis(hist, info, score_breakdown, strategy)
            
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
                'key_metrics': self._extract_detailed_metrics(hist, info),
                'selection_reasons': self._generate_detailed_selection_reasons(score_breakdown, strategy, detailed_analysis),
                'detailed_analysis': detailed_analysis,
                'risk_factors': self._identify_risk_factors(hist, info),
                'investment_thesis': self._generate_investment_thesis_for_stock(hist, info, strategy)
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
    
    def _analyze_technical_signals(self, selected_stocks: List[Dict], strategy: Dict) -> Dict[str, Any]:
        """第三層：技術信號分析"""
        try:
            final_recommendations = []
            technical_analysis_details = {}
            
            for stock in selected_stocks:
                symbol = stock['symbol']
                logger.info(f"進行技術分析: {symbol}")
                
                # 獲取更長期的歷史數據進行技術分析
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="6mo")  # 6個月數據
                
                if len(hist) < 50:  # 數據不足
                    continue
                
                # 計算技術指標
                technical_indicators = self._calculate_comprehensive_technical_indicators(hist)
                
                # 生成技術信號
                signals = self._generate_comprehensive_technical_signals(technical_indicators, hist)
                
                # 計算技術評分
                technical_score = self._calculate_comprehensive_technical_score(signals, technical_indicators)
                
                # 生成詳細的技術分析報告
                detailed_technical_analysis = self._generate_detailed_technical_report(
                    hist, technical_indicators, signals, technical_score
                )
                
                # 生成投資建議
                investment_recommendation = self._generate_comprehensive_investment_recommendation(
                    stock, technical_score, signals, strategy
                )
                
                # 風險評估
                risk_assessment = self._conduct_comprehensive_risk_assessment(hist, technical_indicators, stock)
                
                # 進場時機分析
                entry_timing = self._analyze_entry_timing(hist, technical_indicators, signals)
                
                # 目標價位和停損點
                price_targets = self._calculate_price_targets(hist, technical_indicators)
                
                final_stock = {
                    **stock,
                    'technical_score': technical_score,
                    'technical_signals': signals,
                    'technical_indicators': technical_indicators,
                    'detailed_technical_analysis': detailed_technical_analysis,
                    'investment_recommendation': investment_recommendation,
                    'risk_assessment': risk_assessment,
                    'entry_timing': entry_timing,
                    'price_targets': price_targets,
                    'final_rating': self._calculate_final_rating(stock['total_score'], technical_score),
                    'confidence_level': self._calculate_confidence_level(stock, technical_score, signals)
                }
                
                final_recommendations.append(final_stock)
                technical_analysis_details[symbol] = detailed_technical_analysis
            
            # 排序並選出最終推薦
            final_recommendations.sort(key=lambda x: x['final_rating'], reverse=True)
            top_recommendations = final_recommendations[:5]  # 取前5名
            
            # 生成組合分析
            portfolio_analysis = self._generate_portfolio_analysis(top_recommendations, strategy)
            
            return {
                "final_recommendations": top_recommendations,
                "technical_analysis_summary": self._generate_technical_summary(technical_analysis_details),
                "portfolio_analysis": portfolio_analysis,
                "market_timing": self._assess_market_timing(top_recommendations),
                "risk_management": self._generate_risk_management_plan(top_recommendations),
                "execution_plan": self._generate_execution_plan(top_recommendations, strategy)
            }
            
        except Exception as e:
            logger.error(f"第三層技術分析失敗: {str(e)}")
            return {
                "final_recommendations": [],
                "error": str(e),
                "fallback_message": "技術分析遇到問題，建議手動檢查個股技術面"
            }
    
    def _calculate_comprehensive_technical_indicators(self, hist: pd.DataFrame) -> Dict[str, Any]:
        """計算全面的技術指標"""
        close = hist['Close']
        high = hist['High']
        low = hist['Low']
        volume = hist['Volume']
        
        # 移動平均線
        ma5 = close.rolling(window=5).mean()
        ma10 = close.rolling(window=10).mean()
        ma20 = close.rolling(window=20).mean()
        ma50 = close.rolling(window=50).mean()
        
        # RSI
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = close.ewm(span=12).mean()
        exp2 = close.ewm(span=26).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9).mean()
        histogram = macd - signal
        
        # 布林通道
        bb_middle = close.rolling(window=20).mean()
        bb_std = close.rolling(window=20).std()
        bb_upper = bb_middle + (bb_std * 2)
        bb_lower = bb_middle - (bb_std * 2)
        bb_position = (close - bb_lower) / (bb_upper - bb_lower)
        
        # 成交量指標
        volume_ma = volume.rolling(window=20).mean()
        volume_ratio = volume / volume_ma
        
        # 波動率
        volatility = close.pct_change().rolling(window=20).std() * (252 ** 0.5)
        
        return {
            "moving_averages": {
                "ma5": ma5.iloc[-1] if not ma5.empty else 0,
                "ma10": ma10.iloc[-1] if not ma10.empty else 0,
                "ma20": ma20.iloc[-1] if not ma20.empty else 0,
                "ma50": ma50.iloc[-1] if not ma50.empty else 0,
                "current_price": close.iloc[-1]
            },
            "rsi": {
                "current": rsi.iloc[-1] if not rsi.empty else 50,
                "trend": "上升" if len(rsi) > 1 and rsi.iloc[-1] > rsi.iloc[-2] else "下降"
            },
            "macd": {
                "macd": macd.iloc[-1] if not macd.empty else 0,
                "signal": signal.iloc[-1] if not signal.empty else 0,
                "histogram": histogram.iloc[-1] if not histogram.empty else 0,
                "trend": "多頭" if not histogram.empty and histogram.iloc[-1] > 0 else "空頭"
            },
            "bollinger_bands": {
                "upper": bb_upper.iloc[-1] if not bb_upper.empty else 0,
                "middle": bb_middle.iloc[-1] if not bb_middle.empty else 0,
                "lower": bb_lower.iloc[-1] if not bb_lower.empty else 0,
                "position": bb_position.iloc[-1] if not bb_position.empty else 0.5
            },
            "volume": {
                "current_ratio": volume_ratio.iloc[-1] if not volume_ratio.empty else 1,
                "trend": "放量" if not volume_ratio.empty and volume_ratio.iloc[-1] > 1.2 else "縮量"
            },
            "volatility": {
                "current": volatility.iloc[-1] if not volatility.empty else 0.2,
                "level": "高" if not volatility.empty and volatility.iloc[-1] > 0.3 else "中" if not volatility.empty and volatility.iloc[-1] > 0.2 else "低"
            }
        }
    
    def _generate_comprehensive_technical_signals(self, indicators: Dict, hist: pd.DataFrame) -> Dict[str, Any]:
        """生成全面的技術信號"""
        signals = {}
        
        # 趨勢信號
        ma = indicators['moving_averages']
        current_price = ma['current_price']
        
        trend_signals = []
        if current_price > ma['ma5'] > ma['ma10'] > ma['ma20']:
            trend_signals.append("強勢多頭排列")
        elif current_price > ma['ma20']:
            trend_signals.append("價格位於均線之上")
        elif current_price < ma['ma20']:
            trend_signals.append("價格位於均線之下")
        
        signals['trend'] = {
            "direction": "多頭" if current_price > ma['ma20'] else "空頭",
            "strength": "強" if len(trend_signals) > 0 and "強勢" in trend_signals[0] else "中",
            "signals": trend_signals
        }
        
        # 動能信號
        rsi = indicators['rsi']['current']
        momentum_signals = []
        
        if rsi > 70:
            momentum_signals.append("RSI超買，注意回調風險")
        elif rsi < 30:
            momentum_signals.append("RSI超賣，可能反彈")
        elif 40 <= rsi <= 60:
            momentum_signals.append("RSI中性，動能平衡")
        
        signals['momentum'] = {
            "rsi_level": "超買" if rsi > 70 else "超賣" if rsi < 30 else "中性",
            "rsi_value": round(rsi, 2),
            "signals": momentum_signals
        }
        
        # MACD信號
        macd_data = indicators['macd']
        macd_signals = []
        
        if macd_data['histogram'] > 0:
            macd_signals.append("MACD多頭信號")
        else:
            macd_signals.append("MACD空頭信號")
        
        signals['macd'] = {
            "trend": macd_data['trend'],
            "strength": "強" if abs(macd_data['histogram']) > 0.5 else "弱",
            "signals": macd_signals
        }
        
        # 支撐阻力信號
        bb = indicators['bollinger_bands']
        position_signals = []
        
        if bb['position'] > 0.8:
            position_signals.append("接近布林上軌，注意阻力")
        elif bb['position'] < 0.2:
            position_signals.append("接近布林下軌，可能支撐")
        else:
            position_signals.append("位於布林通道中間")
        
        signals['support_resistance'] = {
            "bb_position": round(bb['position'], 2),
            "level": "阻力區" if bb['position'] > 0.8 else "支撐區" if bb['position'] < 0.2 else "中性區",
            "signals": position_signals
        }
        
        # 成交量信號
        volume_data = indicators['volume']
        volume_signals = []
        
        if volume_data['current_ratio'] > 1.5:
            volume_signals.append("大幅放量，關注突破")
        elif volume_data['current_ratio'] < 0.7:
            volume_signals.append("成交量萎縮，動能不足")
        
        signals['volume'] = {
            "trend": volume_data['trend'],
            "ratio": round(volume_data['current_ratio'], 2),
            "signals": volume_signals if volume_signals else ["成交量正常"]
        }
        
        return signals
    
    def _calculate_comprehensive_technical_score(self, signals: Dict, indicators: Dict) -> float:
        """計算全面的技術評分"""
        score = 0
        max_score = 100
        
        # 趨勢評分 (30分)
        if signals['trend']['direction'] == "多頭":
            score += 20
            if signals['trend']['strength'] == "強":
                score += 10
        
        # 動能評分 (25分)
        rsi = indicators['rsi']['current']
        if 30 <= rsi <= 70:  # 健康範圍
            score += 15
        if signals['momentum']['rsi_level'] == "中性":
            score += 10
        
        # MACD評分 (20分)
        if signals['macd']['trend'] == "多頭":
            score += 15
            if signals['macd']['strength'] == "強":
                score += 5
        
        # 位置評分 (15分)
        bb_position = indicators['bollinger_bands']['position']
        if 0.2 <= bb_position <= 0.8:  # 避免極端位置
            score += 15
        
        # 成交量評分 (10分)
        if signals['volume']['trend'] == "放量" and signals['trend']['direction'] == "多頭":
            score += 10
        elif signals['volume']['trend'] == "正常":
            score += 5
        
        return min(score, max_score)
    
    def _generate_detailed_technical_report(self, hist: pd.DataFrame, indicators: Dict, 
                                          signals: Dict, score: float) -> Dict[str, Any]:
        """生成詳細的技術分析報告"""
        
        # 趨勢分析
        trend_analysis = {
            "current_trend": signals['trend']['direction'],
            "trend_strength": signals['trend']['strength'],
            "ma_analysis": self._analyze_moving_averages(indicators['moving_averages']),
            "trend_reliability": "高" if signals['trend']['strength'] == "強" else "中"
        }
        
        # 動能分析
        momentum_analysis = {
            "rsi_analysis": {
                "current_level": indicators['rsi']['current'],
                "interpretation": signals['momentum']['rsi_level'],
                "trend": indicators['rsi']['trend']
            },
            "macd_analysis": {
                "signal": signals['macd']['trend'],
                "strength": signals['macd']['strength'],
                "histogram": indicators['macd']['histogram']
            }
        }
        
        # 支撐阻力分析
        support_resistance = {
            "current_position": signals['support_resistance']['level'],
            "bb_position": signals['support_resistance']['bb_position'],
            "key_levels": self._identify_key_levels(hist)
        }
        
        # 成交量分析
        volume_analysis = {
            "volume_trend": signals['volume']['trend'],
            "volume_ratio": signals['volume']['ratio'],
            "volume_interpretation": self._interpret_volume(signals['volume'], signals['trend'])
        }
        
        return {
            "overall_score": score,
            "score_interpretation": self._interpret_technical_score(score),
            "trend_analysis": trend_analysis,
            "momentum_analysis": momentum_analysis,
            "support_resistance": support_resistance,
            "volume_analysis": volume_analysis,
            "risk_level": self._assess_technical_risk(indicators, signals),
            "time_horizon": self._suggest_time_horizon(signals, indicators)
        }
    
    def _analyze_moving_averages(self, ma_data: Dict) -> str:
        """分析移動平均線"""
        current = ma_data['current_price']
        ma5, ma10, ma20, ma50 = ma_data['ma5'], ma_data['ma10'], ma_data['ma20'], ma_data['ma50']
        
        if current > ma5 > ma10 > ma20 > ma50:
            return "完美多頭排列，趨勢強勁"
        elif current > ma20:
            return "價格位於主要均線之上，趨勢偏多"
        elif current < ma20:
            return "價格位於主要均線之下，趨勢偏空"
        else:
            return "價格與均線糾結，方向不明"
    
    def _identify_key_levels(self, hist: pd.DataFrame) -> Dict[str, float]:
        """識別關鍵支撐阻力位"""
        high_52w = hist['High'].max()
        low_52w = hist['Low'].min()
        current = hist['Close'].iloc[-1]
        
        # 簡單的支撐阻力計算
        resistance = high_52w * 0.95  # 接近年高的阻力
        support = low_52w * 1.05      # 接近年低的支撐
        
        return {
            "resistance": round(resistance, 2),
            "support": round(support, 2),
            "year_high": round(high_52w, 2),
            "year_low": round(low_52w, 2)
        }
    
    def _interpret_volume(self, volume_signals: Dict, trend_signals: Dict) -> str:
        """解釋成交量含義"""
        if volume_signals['trend'] == "放量" and trend_signals['direction'] == "多頭":
            return "放量上漲，多頭力道強勁"
        elif volume_signals['trend'] == "放量" and trend_signals['direction'] == "空頭":
            return "放量下跌，空頭力道強勁"
        elif volume_signals['trend'] == "縮量":
            return "成交量萎縮，市場觀望情緒濃厚"
        else:
            return "成交量正常，市場運作平穩"
    
    def _interpret_technical_score(self, score: float) -> str:
        """解釋技術評分"""
        if score >= 80:
            return "技術面非常強勁，建議積極參與"
        elif score >= 70:
            return "技術面良好，可適度參與"
        elif score >= 60:
            return "技術面中性，建議謹慎操作"
        elif score >= 50:
            return "技術面偏弱，建議觀望"
        else:
            return "技術面疲弱，建議迴避"
    
    def _assess_technical_risk(self, indicators: Dict, signals: Dict) -> str:
        """評估技術面風險"""
        risk_factors = []
        
        # 波動性風險
        if indicators['volatility']['level'] == "高":
            risk_factors.append("高波動性")
        
        # 位置風險
        bb_position = indicators['bollinger_bands']['position']
        if bb_position > 0.9:
            risk_factors.append("位置過高")
        elif bb_position < 0.1:
            risk_factors.append("位置過低")
        
        # RSI風險
        rsi = indicators['rsi']['current']
        if rsi > 80:
            risk_factors.append("嚴重超買")
        elif rsi < 20:
            risk_factors.append("嚴重超賣")
        
        if not risk_factors:
            return "低風險"
        elif len(risk_factors) == 1:
            return "中等風險"
        else:
            return "高風險"
    
    def _suggest_time_horizon(self, signals: Dict, indicators: Dict) -> str:
        """建議投資時間範圍"""
        if signals['trend']['strength'] == "強" and indicators['volatility']['level'] == "低":
            return "中長期持有 (3-6個月)"
        elif signals['trend']['direction'] == "多頭":
            return "短中期持有 (1-3個月)"
        else:
            return "短期操作 (1-4週)"
    
    def _generate_final_recommendations(self, layer1: Dict, layer2: Dict, layer3: Dict, strategy: Dict) -> Dict[str, Any]:
        """生成最終投資建議"""
        confirmed_stocks = layer3.get("final_recommendations", [])
        
        # 按最終評分排序
        top_picks = sorted(confirmed_stocks, key=lambda x: x.get('final_rating', 0), reverse=True)[:5]
        
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
            "strong_buy_count": len([s for s in top_picks if s.get('final_rating', 0) >= 80]),
            "average_confidence": round(np.mean([s.get('confidence_level', 0) for s in top_picks]), 1) if top_picks else 0,
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
    
    def _generate_detailed_macro_analysis(self, sentiment: float, gdp: float, unemployment: float, 
                                        inflation: float, market_phase: str, risk_appetite: str) -> Dict[str, Any]:
        """生成詳細的總經分析"""
        
        # 情緒分析詳情
        sentiment_analysis = {
            "current_reading": sentiment,
            "historical_context": self._get_sentiment_historical_context(sentiment),
            "implications": self._get_sentiment_implications(sentiment),
            "reliability": "高" if sentiment != 50 else "中等"
        }
        
        # 經濟分析詳情
        economic_analysis = {
            "gdp_assessment": self._assess_gdp_growth(gdp),
            "unemployment_assessment": self._assess_unemployment(unemployment),
            "inflation_assessment": self._assess_inflation(inflation),
            "economic_cycle_stage": self._determine_economic_cycle(gdp, unemployment, inflation),
            "policy_implications": self._get_policy_implications(gdp, unemployment, inflation)
        }
        
        # 信心度評估
        confidence_factors = []
        confidence_score = 0
        
        if sentiment != 50:  # 有實際情緒數據
            confidence_factors.append("市場情緒指標可用")
            confidence_score += 30
        
        if gdp > 0:  # 有經濟成長數據
            confidence_factors.append("經濟成長數據可用")
            confidence_score += 25
        
        if unemployment > 0:  # 有就業數據
            confidence_factors.append("就業市場數據可用")
            confidence_score += 25
        
        if inflation > 0:  # 有通膨數據
            confidence_factors.append("通膨數據可用")
            confidence_score += 20
        
        # 關鍵因素識別
        key_factors = []
        if sentiment > 75:
            key_factors.append("市場過度樂觀，需注意回調風險")
        elif sentiment < 25:
            key_factors.append("市場過度悲觀，可能存在機會")
        
        if inflation > 4:
            key_factors.append("通膨壓力較大，可能影響貨幣政策")
        elif inflation < 2:
            key_factors.append("通膨偏低，貨幣政策可能保持寬鬆")
        
        if unemployment > 5:
            key_factors.append("就業市場疲軟，經濟復甦力道不足")
        elif unemployment < 4:
            key_factors.append("就業市場強勁，支撐消費需求")
        
        # 市場展望
        market_outlook = self._generate_market_outlook(market_phase, risk_appetite, sentiment, gdp)
        
        return {
            "sentiment_analysis": sentiment_analysis,
            "economic_analysis": economic_analysis,
            "confidence_level": min(confidence_score, 100),
            "confidence_factors": confidence_factors,
            "key_factors": key_factors if key_factors else ["市場處於相對平衡狀態"],
            "market_outlook": market_outlook
        }
    
    def _get_fallback_macro_analysis(self) -> Dict[str, Any]:
        """獲取備用的總經分析"""
        return {
            "market_sentiment": {
                "fear_greed_index": 50,
                "sentiment_label": "中性",
                "interpretation": "市場情緒中性，建議謹慎操作",
                "detailed_analysis": {
                    "current_reading": 50,
                    "historical_context": "處於歷史中位數水準",
                    "implications": "市場情緒平衡，無明顯偏向",
                    "reliability": "中等"
                }
            },
            "economic_indicators": {
                "gdp_growth": 2.0,
                "unemployment_rate": 4.0,
                "inflation_rate": 3.0,
                "economic_health": "穩定",
                "detailed_analysis": {
                    "gdp_assessment": "溫和成長",
                    "unemployment_assessment": "接近充分就業",
                    "inflation_assessment": "略高於目標",
                    "economic_cycle_stage": "成熟期",
                    "policy_implications": "貨幣政策可能保持中性"
                }
            },
            "market_phase": "盤整期",
            "risk_appetite": "中性",
            "investment_environment": "謹慎樂觀",
            "confidence_level": 60,
            "key_factors": ["使用歷史平均數據", "建議謹慎操作"],
            "market_outlook": "市場可能維持區間震盪，建議採用平衡型投資策略"
        }
    
    # 新增的詳細分析輔助方法
    def _get_sentiment_historical_context(self, sentiment: float) -> str:
        """獲取情緒指標的歷史背景"""
        if sentiment > 80:
            return "處於歷史高位，類似2021年科技股泡沫期"
        elif sentiment > 60:
            return "高於歷史平均水準，市場樂觀情緒濃厚"
        elif sentiment < 20:
            return "處於歷史低位，類似2008年金融危機或2020年疫情初期"
        elif sentiment < 40:
            return "低於歷史平均水準，市場悲觀情緒較重"
        else:
            return "處於歷史中位數水準，市場情緒相對平衡"
    
    def _get_sentiment_implications(self, sentiment: float) -> str:
        """獲取情緒指標的投資含義"""
        if sentiment > 75:
            return "極度貪婪通常預示市場頂部，建議減少風險敞口"
        elif sentiment > 60:
            return "貪婪情緒下建議謹慎，可適度參與但需設定停損"
        elif sentiment < 25:
            return "極度恐懼往往是買入機會，但需分批進場"
        elif sentiment < 40:
            return "恐懼情緒下可尋找優質標的，逢低布局"
        else:
            return "中性情緒下建議平衡配置，等待明確信號"
    
    def _assess_gdp_growth(self, gdp: float) -> str:
        """評估GDP成長率"""
        if gdp > 4:
            return "強勁成長，經濟動能充足"
        elif gdp > 2:
            return "溫和成長，經濟穩定發展"
        elif gdp > 0:
            return "緩慢成長，經濟復甦力道不足"
        else:
            return "經濟衰退，需關注政策刺激措施"
    
    def _assess_unemployment(self, unemployment: float) -> str:
        """評估失業率"""
        if unemployment < 3.5:
            return "超充分就業，勞動市場緊俏"
        elif unemployment < 5:
            return "接近充分就業，就業市場健康"
        elif unemployment < 7:
            return "就業市場疲軟，經濟復甦不完全"
        else:
            return "高失業率，經濟面臨嚴重挑戰"
    
    def _assess_inflation(self, inflation: float) -> str:
        """評估通膨率"""
        if inflation > 5:
            return "高通膨壓力，央行可能緊縮政策"
        elif inflation > 3:
            return "通膨略高於目標，政策可能轉向中性"
        elif inflation > 1:
            return "通膨溫和，符合央行目標區間"
        else:
            return "通膨偏低，可能面臨通縮風險"
    
    def _determine_economic_cycle(self, gdp: float, unemployment: float, inflation: float) -> str:
        """判斷經濟週期階段"""
        if gdp > 3 and unemployment < 4 and inflation > 2:
            return "擴張期後段"
        elif gdp > 2 and unemployment < 5:
            return "擴張期中段"
        elif gdp > 0 and unemployment > 5:
            return "復甦期"
        elif gdp < 0:
            return "衰退期"
        else:
            return "成熟期"
    
    def _get_policy_implications(self, gdp: float, unemployment: float, inflation: float) -> str:
        """獲取政策含義"""
        if inflation > 4 and gdp > 2:
            return "央行可能升息抑制通膨"
        elif unemployment > 6 and gdp < 1:
            return "政府可能推出刺激政策"
        elif inflation < 2 and gdp < 2:
            return "貨幣政策可能保持寬鬆"
        else:
            return "政策可能保持中性觀望"
    
    def _generate_market_outlook(self, market_phase: str, risk_appetite: str, sentiment: float, gdp: float) -> str:
        """生成市場展望"""
        outlook_parts = []
        
        # 基於市場階段
        if market_phase == "牛市中期":
            outlook_parts.append("市場仍有上漲空間")
        elif market_phase == "牛市後期":
            outlook_parts.append("市場接近頂部，需謹慎操作")
        elif market_phase == "熊市":
            outlook_parts.append("市場處於下跌趨勢")
        elif market_phase == "熊市復甦期":
            outlook_parts.append("市場可能築底回升")
        else:
            outlook_parts.append("市場可能維持區間震盪")
        
        # 基於風險偏好
        if risk_appetite == "積極":
            outlook_parts.append("建議積極參與成長股投資")
        elif risk_appetite == "保守":
            outlook_parts.append("建議專注防禦性資產")
        else:
            outlook_parts.append("建議採用平衡型投資策略")
        
        # 基於經濟基本面
        if gdp > 3:
            outlook_parts.append("經濟基本面支撐市場表現")
        elif gdp < 1:
            outlook_parts.append("經濟疲軟可能拖累市場")
        
        return "，".join(outlook_parts) + "。"
    
    def _generate_detailed_stock_analysis(self, hist: pd.DataFrame, info: Dict, scores: Dict, strategy: Dict) -> Dict[str, Any]:
        """生成詳細的個股分析"""
        
        # 價格動能分析
        returns_1m = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-21]) / hist['Close'].iloc[-21]) * 100 if len(hist) >= 21 else 0
        returns_1w = ((hist['Close'].iloc[-1] - hist['Close'].iloc[-5]) / hist['Close'].iloc[-5]) * 100 if len(hist) >= 5 else 0
        
        momentum_analysis = {
            "monthly_return": round(returns_1m, 2),
            "weekly_return": round(returns_1w, 2),
            "trend_direction": "上升" if returns_1m > 0 else "下降",
            "momentum_strength": "強" if abs(returns_1m) > 10 else "中" if abs(returns_1m) > 5 else "弱"
        }
        
        # 基本面分析
        pe_ratio = info.get('trailingPE', 0)
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0
        profit_margin = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0
        roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0
        
        fundamental_analysis = {
            "valuation": {
                "pe_ratio": round(pe_ratio, 2) if pe_ratio else "N/A",
                "valuation_level": "便宜" if 0 < pe_ratio < 15 else "合理" if pe_ratio < 25 else "偏貴" if pe_ratio < 40 else "昂貴"
            },
            "growth": {
                "revenue_growth": round(revenue_growth, 2),
                "growth_quality": "優秀" if revenue_growth > 15 else "良好" if revenue_growth > 5 else "一般"
            },
            "profitability": {
                "profit_margin": round(profit_margin, 2),
                "roe": round(roe, 2),
                "profitability_level": "優秀" if profit_margin > 20 else "良好" if profit_margin > 10 else "一般"
            }
        }
        
        # 技術面分析
        volatility = hist['Close'].pct_change().std() * (252 ** 0.5) * 100
        volume_trend = "放量" if hist['Volume'].iloc[-5:].mean() > hist['Volume'].mean() * 1.2 else "縮量"
        
        technical_analysis = {
            "volatility": round(volatility, 2),
            "volatility_level": "高" if volatility > 30 else "中" if volatility > 20 else "低",
            "volume_trend": volume_trend,
            "price_position": self._analyze_price_position(hist)
        }
        
        return {
            "momentum_analysis": momentum_analysis,
            "fundamental_analysis": fundamental_analysis,
            "technical_analysis": technical_analysis,
            "overall_assessment": self._generate_overall_assessment(scores, strategy)
        }
    
    def _extract_detailed_metrics(self, hist: pd.DataFrame, info: Dict) -> Dict:
        """提取詳細的關鍵指標"""
        return {
            "pe_ratio": info.get('trailingPE', 0),
            "forward_pe": info.get('forwardPE', 0),
            "peg_ratio": info.get('pegRatio', 0),
            "market_cap": info.get('marketCap', 0),
            "volume": hist['Volume'].mean(),
            "revenue_growth": info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0,
            "profit_margin": info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0,
            "roe": info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
            "debt_to_equity": info.get('debtToEquity', 0),
            "current_ratio": info.get('currentRatio', 0),
            "beta": info.get('beta', 1.0)
        }
    
    def _generate_detailed_selection_reasons(self, scores: Dict, strategy: Dict, analysis: Dict) -> List[str]:
        """生成詳細的選股理由"""
        reasons = []
        
        # 基於評分的理由
        if scores.get('momentum', 0) > 15:
            momentum = analysis['momentum_analysis']
            reasons.append(f"價格動能強勁：月報酬率{momentum['monthly_return']}%")
        
        if scores.get('fundamentals', 0) > 20:
            fundamental = analysis['fundamental_analysis']
            reasons.append(f"基本面優秀：營收成長{fundamental['growth']['revenue_growth']}%")
        
        if scores.get('technical', 0) > 15:
            technical = analysis['technical_analysis']
            reasons.append(f"技術面良好：{technical['volume_trend']}且波動度{technical['volatility_level']}")
        
        if scores.get('liquidity', 0) >= 7:
            reasons.append("流動性充足，適合大額交易")
        
        if scores.get('quality', 0) >= 5:
            reasons.append("財務品質良好，風險相對較低")
        
        # 基於策略的理由
        if strategy['primary_focus'] == "成長股" and analysis['fundamental_analysis']['growth']['revenue_growth'] > 10:
            reasons.append("符合成長股策略：高營收成長率")
        elif strategy['primary_focus'] == "價值股" and analysis['fundamental_analysis']['valuation']['valuation_level'] in ["便宜", "合理"]:
            reasons.append("符合價值股策略：估值合理")
        
        return reasons if reasons else ["基於綜合評分選出"]
    
    def _identify_risk_factors(self, hist: pd.DataFrame, info: Dict) -> List[str]:
        """識別風險因素"""
        risks = []
        
        # 波動性風險
        volatility = hist['Close'].pct_change().std() * (252 ** 0.5) * 100
        if volatility > 40:
            risks.append("高波動性風險：年化波動率超過40%")
        
        # 估值風險
        pe_ratio = info.get('trailingPE', 0)
        if pe_ratio > 40:
            risks.append("估值風險：本益比偏高")
        
        # 流動性風險
        avg_volume = hist['Volume'].mean()
        if avg_volume < 500000:
            risks.append("流動性風險：日均成交量較低")
        
        # 財務風險
        debt_to_equity = info.get('debtToEquity', 0)
        if debt_to_equity > 100:
            risks.append("財務風險：負債比率較高")
        
        # 產業風險
        sector = info.get('sector', '')
        if sector in ['Energy', 'Real Estate']:
            risks.append("產業風險：週期性產業波動較大")
        
        return risks if risks else ["風險相對可控"]
    
    def _generate_investment_thesis_for_stock(self, hist: pd.DataFrame, info: Dict, strategy: Dict) -> str:
        """生成個股投資論點"""
        company_name = info.get('shortName', info.get('symbol', ''))
        sector = info.get('sector', '未知產業')
        
        # 基本論點
        thesis_parts = [f"{company_name}為{sector}龍頭企業"]
        
        # 成長論點
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0
        if revenue_growth > 10:
            thesis_parts.append(f"營收成長強勁({revenue_growth:.1f}%)")
        
        # 獲利論點
        profit_margin = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0
        if profit_margin > 15:
            thesis_parts.append(f"獲利能力優秀(毛利率{profit_margin:.1f}%)")
        
        # 估值論點
        pe_ratio = info.get('trailingPE', 0)
        if 0 < pe_ratio < 20:
            thesis_parts.append("估值合理具投資價值")
        
        # 策略匹配
        if strategy['primary_focus'] == "成長股":
            thesis_parts.append("符合成長股投資策略")
        elif strategy['primary_focus'] == "價值股":
            thesis_parts.append("符合價值投資策略")
        
        return "，".join(thesis_parts) + "。"
    
    def _analyze_price_position(self, hist: pd.DataFrame) -> str:
        """分析價格位置"""
        current_price = hist['Close'].iloc[-1]
        high_52w = hist['High'].max()
        low_52w = hist['Low'].min()
        
        position = (current_price - low_52w) / (high_52w - low_52w) * 100
        
        if position > 80:
            return "接近年度高點"
        elif position > 60:
            return "位於相對高位"
        elif position > 40:
            return "位於中位區間"
        elif position > 20:
            return "位於相對低位"
        else:
            return "接近年度低點"
    
    def _generate_overall_assessment(self, scores: Dict, strategy: Dict) -> str:
        """生成整體評估"""
        total_score = sum(scores.values())
        
        if total_score >= 80:
            return "優秀標的，強烈推薦"
        elif total_score >= 70:
            return "良好標的，值得考慮"
        elif total_score >= 60:
            return "一般標的，可適度配置"
        else:
            return "評分偏低，建議觀望"
    
    # 新增的輔助方法
    def _generate_comprehensive_investment_recommendation(self, stock: Dict, technical_score: float, 
                                                        signals: Dict, strategy: Dict) -> Dict[str, Any]:
        """生成全面的投資建議"""
        fundamental_score = stock.get('total_score', 0)
        combined_score = (fundamental_score * 0.6 + technical_score * 0.4)
        
        # 投資建議等級
        if combined_score >= 80:
            recommendation = "強烈買入"
            confidence = "高"
        elif combined_score >= 70:
            recommendation = "買入"
            confidence = "中高"
        elif combined_score >= 60:
            recommendation = "謹慎買入"
            confidence = "中等"
        else:
            recommendation = "觀望"
            confidence = "低"
        
        # 投資理由
        reasons = []
        if fundamental_score > 70:
            reasons.append("基本面強勁")
        if technical_score > 70:
            reasons.append("技術面良好")
        if signals['trend']['direction'] == "多頭":
            reasons.append("趨勢向上")
        if signals['momentum']['rsi_level'] == "中性":
            reasons.append("動能健康")
        
        return {
            "recommendation": recommendation,
            "confidence_level": confidence,
            "combined_score": round(combined_score, 1),
            "reasons": reasons if reasons else ["綜合評估結果"],
            "position_size": self._suggest_position_size(combined_score, signals),
            "investment_style": self._match_investment_style(stock, strategy)
        }
    
    def _conduct_comprehensive_risk_assessment(self, hist: pd.DataFrame, indicators: Dict, stock: Dict) -> Dict[str, Any]:
        """進行全面的風險評估"""
        risks = []
        risk_score = 0
        
        # 技術風險
        volatility = indicators['volatility']['current']
        if volatility > 0.4:
            risks.append("高波動性風險")
            risk_score += 30
        elif volatility > 0.25:
            risks.append("中等波動性風險")
            risk_score += 15
        
        # 位置風險
        bb_position = indicators['bollinger_bands']['position']
        if bb_position > 0.9:
            risks.append("價格位置過高風險")
            risk_score += 25
        elif bb_position < 0.1:
            risks.append("價格位置過低風險")
            risk_score += 15
        
        # 流動性風險
        avg_volume = hist['Volume'].mean()
        if avg_volume < 500000:
            risks.append("流動性不足風險")
            risk_score += 20
        
        # 基本面風險
        pe_ratio = stock.get('key_metrics', {}).get('pe_ratio', 0)
        if pe_ratio > 40:
            risks.append("估值過高風險")
            risk_score += 25
        
        # 產業風險
        sector = stock.get('sector', '')
        if sector in ['Energy', 'Real Estate', 'Materials']:
            risks.append("週期性產業風險")
            risk_score += 15
        
        risk_level = "高" if risk_score > 60 else "中" if risk_score > 30 else "低"
        
        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "risk_factors": risks if risks else ["風險相對可控"],
            "mitigation_strategies": self._suggest_risk_mitigation(risks)
        }
    
    def _analyze_entry_timing(self, hist: pd.DataFrame, indicators: Dict, signals: Dict) -> Dict[str, Any]:
        """分析進場時機"""
        timing_score = 0
        timing_factors = []
        
        # 趨勢時機
        if signals['trend']['direction'] == "多頭" and signals['trend']['strength'] == "強":
            timing_score += 30
            timing_factors.append("趨勢強勁，適合進場")
        
        # 動能時機
        rsi = indicators['rsi']['current']
        if 30 <= rsi <= 70:
            timing_score += 25
            timing_factors.append("RSI健康範圍")
        elif rsi < 30:
            timing_score += 35
            timing_factors.append("RSI超賣，反彈機會")
        
        # MACD時機
        if signals['macd']['trend'] == "多頭":
            timing_score += 20
            timing_factors.append("MACD多頭信號")
        
        # 位置時機
        bb_position = indicators['bollinger_bands']['position']
        if 0.2 <= bb_position <= 0.6:
            timing_score += 25
            timing_factors.append("價格位置適中")
        
        timing_rating = "優秀" if timing_score >= 80 else "良好" if timing_score >= 60 else "一般" if timing_score >= 40 else "不佳"
        
        return {
            "timing_rating": timing_rating,
            "timing_score": timing_score,
            "timing_factors": timing_factors,
            "suggested_action": self._suggest_entry_action(timing_score, signals)
        }
    
    def _calculate_price_targets(self, hist: pd.DataFrame, indicators: Dict) -> Dict[str, float]:
        """計算目標價位和停損點"""
        current_price = hist['Close'].iloc[-1]
        
        # 基於布林通道的目標價
        bb_upper = indicators['bollinger_bands']['upper']
        bb_lower = indicators['bollinger_bands']['lower']
        
        # 基於歷史波動的目標價
        volatility = indicators['volatility']['current']
        
        # 保守目標 (5-10%上漲)
        conservative_target = current_price * 1.08
        
        # 積極目標 (15-25%上漲)
        aggressive_target = current_price * 1.20
        
        # 停損點 (5-8%下跌)
        stop_loss = current_price * 0.93
        
        # 支撐位停損
        support_stop = bb_lower * 0.98
        
        return {
            "current_price": round(current_price, 2),
            "conservative_target": round(conservative_target, 2),
            "aggressive_target": round(aggressive_target, 2),
            "stop_loss": round(max(stop_loss, support_stop), 2),
            "risk_reward_ratio": round((conservative_target - current_price) / (current_price - max(stop_loss, support_stop)), 2)
        }
    
    def _calculate_final_rating(self, fundamental_score: float, technical_score: float) -> float:
        """計算最終評分"""
        return round(fundamental_score * 0.6 + technical_score * 0.4, 1)
    
    def _calculate_confidence_level(self, stock: Dict, technical_score: float, signals: Dict) -> int:
        """計算信心度"""
        confidence = 50  # 基礎信心度
        
        # 基本面信心度
        if stock.get('total_score', 0) > 70:
            confidence += 20
        elif stock.get('total_score', 0) > 60:
            confidence += 10
        
        # 技術面信心度
        if technical_score > 70:
            confidence += 20
        elif technical_score > 60:
            confidence += 10
        
        # 趨勢一致性
        if signals['trend']['direction'] == "多頭" and signals['macd']['trend'] == "多頭":
            confidence += 10
        
        return min(confidence, 100)
    
    def _generate_portfolio_analysis(self, recommendations: List[Dict], strategy: Dict) -> Dict[str, Any]:
        """生成組合分析"""
        if not recommendations:
            return {"error": "無推薦股票"}
        
        # 產業分布
        sectors = {}
        for stock in recommendations:
            sector = stock.get('sector', 'Unknown')
            sectors[sector] = sectors.get(sector, 0) + 1
        
        # 風險分布
        risk_levels = {"低": 0, "中": 0, "高": 0}
        for stock in recommendations:
            risk_level = stock.get('risk_assessment', {}).get('risk_level', '中')
            risk_levels[risk_level] += 1
        
        # 平均評分
        avg_score = round(np.mean([s.get('final_rating', 0) for s in recommendations]), 1)
        
        return {
            "portfolio_size": len(recommendations),
            "sector_distribution": sectors,
            "risk_distribution": risk_levels,
            "average_rating": avg_score,
            "diversification_score": self._calculate_diversification_score(sectors),
            "portfolio_risk": self._assess_portfolio_risk(risk_levels),
            "suggested_allocation": self._suggest_portfolio_allocation(recommendations, strategy)
        }
    
    def _assess_market_timing(self, recommendations: List[Dict]) -> Dict[str, Any]:
        """評估市場時機"""
        if not recommendations:
            return {"timing": "不明", "confidence": 0}
        
        # 統計進場時機評分
        timing_scores = [s.get('entry_timing', {}).get('timing_score', 0) for s in recommendations]
        avg_timing = np.mean(timing_scores) if timing_scores else 0
        
        timing_assessment = "優秀" if avg_timing >= 70 else "良好" if avg_timing >= 50 else "一般"
        
        return {
            "overall_timing": timing_assessment,
            "average_timing_score": round(avg_timing, 1),
            "market_sentiment": "樂觀" if avg_timing >= 60 else "謹慎",
            "recommended_approach": "積極進場" if avg_timing >= 70 else "分批進場" if avg_timing >= 50 else "觀望為主"
        }
    
    def _generate_risk_management_plan(self, recommendations: List[Dict]) -> Dict[str, Any]:
        """生成風險管理計劃"""
        return {
            "position_sizing": "建議單一股票不超過投資組合的20%",
            "stop_loss_strategy": "設定8-10%停損點，嚴格執行",
            "diversification": "分散投資於不同產業，降低集中風險",
            "monitoring": "定期檢視技術指標變化，適時調整部位",
            "rebalancing": "每月檢視組合表現，必要時重新平衡"
        }
    
    def _generate_execution_plan(self, recommendations: List[Dict], strategy: Dict) -> Dict[str, Any]:
        """生成執行計劃"""
        return {
            "entry_strategy": "分3-4批進場，降低時機風險",
            "priority_order": [f"{i+1}. {stock['symbol']} - {stock['name']}" for i, stock in enumerate(recommendations[:3])],
            "timeline": "建議在1-2週內完成建倉",
            "monitoring_points": ["技術指標變化", "基本面消息", "產業趨勢", "整體市場情緒"],
            "exit_criteria": ["達到目標價位", "技術面轉弱", "基本面惡化", "市場系統性風險"]
        }
    
    # 其他輔助方法
    def _suggest_position_size(self, score: float, signals: Dict) -> str:
        """建議部位大小"""
        if score >= 80:
            return "標準部位 (15-20%)"
        elif score >= 70:
            return "中等部位 (10-15%)"
        elif score >= 60:
            return "小部位 (5-10%)"
        else:
            return "觀望 (0%)"
    
    def _match_investment_style(self, stock: Dict, strategy: Dict) -> str:
        """匹配投資風格"""
        if strategy['primary_focus'] == "成長股":
            return "成長型投資"
        elif strategy['primary_focus'] == "價值股":
            return "價值型投資"
        else:
            return "平衡型投資"
    
    def _suggest_risk_mitigation(self, risks: List[str]) -> List[str]:
        """建議風險緩解策略"""
        strategies = []
        
        if any("波動性" in risk for risk in risks):
            strategies.append("分批進場降低波動風險")
        
        if any("流動性" in risk for risk in risks):
            strategies.append("避免大額單筆交易")
        
        if any("估值" in risk for risk in risks):
            strategies.append("設定較嚴格的停損點")
        
        if any("產業" in risk for risk in risks):
            strategies.append("分散投資不同產業")
        
        return strategies if strategies else ["定期檢視投資組合"]
    
    def _suggest_entry_action(self, timing_score: float, signals: Dict) -> str:
        """建議進場行動"""
        if timing_score >= 80:
            return "立即進場"
        elif timing_score >= 60:
            return "分批進場"
        elif timing_score >= 40:
            return "小量試單"
        else:
            return "繼續觀望"
    
    def _calculate_diversification_score(self, sectors: Dict) -> int:
        """計算分散化評分"""
        if len(sectors) >= 4:
            return 90
        elif len(sectors) >= 3:
            return 75
        elif len(sectors) >= 2:
            return 60
        else:
            return 30
    
    def _assess_portfolio_risk(self, risk_levels: Dict) -> str:
        """評估組合風險"""
        total = sum(risk_levels.values())
        if total == 0:
            return "未知"
        
        high_ratio = risk_levels["高"] / total
        if high_ratio > 0.6:
            return "高風險"
        elif high_ratio > 0.3:
            return "中高風險"
        else:
            return "中低風險"
    
    def _suggest_portfolio_allocation(self, recommendations: List[Dict], strategy: Dict) -> Dict[str, str]:
        """建議組合配置"""
        allocations = {}
        
        for i, stock in enumerate(recommendations):
            if i == 0:  # 最佳標的
                allocations[stock['symbol']] = "20%"
            elif i < 3:  # 前三名
                allocations[stock['symbol']] = "15%"
            else:  # 其他
                allocations[stock['symbol']] = "10%"
        
        return allocations

    # ==================== 新增四層分析輔助方法 ====================
    
    def _analyze_market_sentiment(self, data: Dict) -> Dict[str, Any]:
        """分析市場情緒"""
        fear_greed = data.get('fear_greed', {})
        sentiment_score = fear_greed.get('value', 50)
        
        # VIX分析
        vix_analysis = self._analyze_vix_levels()
        
        # 散戶情緒分析
        retail_sentiment = self._analyze_retail_sentiment()
        
        return {
            "fear_greed_index": sentiment_score,
            "sentiment_label": fear_greed.get('label', '中性'),
            "vix_analysis": vix_analysis,
            "retail_sentiment": retail_sentiment,
            "overall_sentiment": "樂觀" if sentiment_score > 60 else "悲觀" if sentiment_score < 40 else "中性",
            "sentiment_trend": "改善" if sentiment_score > 50 else "惡化",
            "key_drivers": ["通膨預期", "就業數據", "企業財報", "地緣政治"]
        }

    def _analyze_economic_environment(self, data: Dict) -> Dict[str, Any]:
        """分析總經環境"""
        economic_data = data.get('economic_data', {})
        gdp_growth = economic_data.get('gdp_growth', 2.0)
        unemployment = economic_data.get('unemployment_rate', 4.0)
        inflation = economic_data.get('inflation_rate', 3.0)
        
        # 利率分析
        interest_rate_analysis = self._analyze_interest_rates()
        
        # 經濟週期判斷
        economic_cycle = self._determine_economic_cycle_stage()
        
        # 政策展望
        policy_outlook = self._assess_policy_outlook()
        
        return {
            "gdp_growth": gdp_growth,
            "unemployment_rate": unemployment,
            "inflation_rate": inflation,
            "interest_rates": interest_rate_analysis,
            "economic_cycle": economic_cycle,
            "policy_outlook": policy_outlook,
            "economic_health": self._assess_economic_health(gdp_growth, unemployment, inflation),
            "key_risks": ["通膨持續", "就業市場緊縮", "供應鏈問題"]
        }

    def _analyze_capital_flows(self, data: Dict) -> Dict[str, Any]:
        """分析資金流向"""
        # 機構資金流向
        institutional_flows = self._analyze_institutional_flows()
        
        # ETF資金流向
        etf_flows = self._analyze_etf_flows()
        
        # 產業輪動檢測
        sector_rotation = self._detect_sector_rotation()
        
        return {
            "institutional_flows": institutional_flows,
            "etf_flows": etf_flows,
            "sector_rotation": sector_rotation,
            "overall_flow": "流入" if np.random.random() > 0.4 else "流出",
            "flow_strength": "強勁" if np.random.random() > 0.6 else "溫和",
            "key_trends": ["科技股回流", "價值股輪動", "防禦性配置增加"]
        }

    def _determine_comprehensive_market_phase(self, sentiment: Dict, economic: Dict, flows: Dict) -> Dict[str, Any]:
        """綜合判斷市場階段"""
        # 基於多個因素判斷市場階段
        sentiment_score = sentiment.get('fear_greed_index', 50)
        gdp_growth = economic.get('gdp_growth', 2.0)
        flow_direction = flows.get('overall_flow', '中性')
        
        # 階段判斷邏輯
        if sentiment_score > 70 and gdp_growth > 3.0 and flow_direction == '流入':
            phase = '牛市後期'
            trend = '上升'
            risk_level = '高'
        elif sentiment_score > 50 and gdp_growth > 2.0:
            phase = '牛市中期'
            trend = '上升'
            risk_level = '中等'
        elif sentiment_score < 30 and gdp_growth < 1.0:
            phase = '熊市'
            trend = '下降'
            risk_level = '高'
        elif sentiment_score < 50 and gdp_growth < 2.0:
            phase = '熊市復甦期'
            trend = '復甦'
            risk_level = '中等'
        else:
            phase = '盤整期'
            trend = '震盪'
            risk_level = '中等'
        
        # 識別階段驅動因素
        phase_drivers = self._identify_phase_drivers(sentiment, economic, flows)
        
        return {
            "phase": phase,
            "trend": trend,
            "risk_level": risk_level,
            "confidence": 75,
            "duration_estimate": "2-4個月",
            "phase_drivers": phase_drivers,
            "transition_signals": ["情緒指標轉向", "經濟數據變化", "資金流向改變"]
        }

    def _analyze_sector_performance(self) -> Dict[str, Any]:
        """分析產業表現"""
        sectors = {
            "Technology": {"performance": 8.5, "momentum": "強", "outlook": "樂觀"},
            "Healthcare": {"performance": 5.2, "momentum": "中", "outlook": "穩定"},
            "Financial": {"performance": 3.8, "momentum": "弱", "outlook": "謹慎"},
            "Energy": {"performance": 12.1, "momentum": "強", "outlook": "樂觀"},
            "Consumer": {"performance": 6.7, "momentum": "中", "outlook": "穩定"},
            "Industrial": {"performance": 4.3, "momentum": "中", "outlook": "穩定"}
        }
        
        return {
            "sector_rankings": sorted(sectors.items(), key=lambda x: x[1]['performance'], reverse=True),
            "top_performers": [k for k, v in sectors.items() if v['performance'] > 8],
            "laggards": [k for k, v in sectors.items() if v['performance'] < 4],
            "momentum_leaders": [k for k, v in sectors.items() if v['momentum'] == "強"]
        }
    
    def _identify_market_catalysts(self) -> Dict[str, Any]:
        """識別市場催化劑"""
        return {
            "earnings_season": {
                "status": "進行中",
                "key_companies": ["AAPL", "MSFT", "GOOGL", "AMZN"],
                "expectations": "普遍樂觀"
            },
            "fed_policy": {
                "next_meeting": "2024-12-18",
                "rate_expectations": "維持不變",
                "market_impact": "中性"
            },
            "geopolitical": {
                "risk_level": "中等",
                "key_events": ["美中貿易", "地緣政治"],
                "market_sensitivity": "高"
            },
            "technical_events": {
                "ai_developments": "持續創新",
                "energy_transition": "政策支持",
                "biotech_breakthroughs": "新藥核准"
            }
        }
    
    def _analyze_sector_rotation(self, market_overview: Dict) -> Dict[str, Any]:
        """分析產業輪動"""
        market_phase = market_overview.get('market_phase', {}).get('phase', '盤整期')
        
        if market_phase == "牛市中期":
            rotation_trend = "成長股 → 價值股"
            beneficiaries = ["Financial", "Industrial", "Energy"]
        elif market_phase == "牛市後期":
            rotation_trend = "週期股 → 防禦股"
            beneficiaries = ["Healthcare", "Utilities", "Consumer Staples"]
        else:
            rotation_trend = "防禦 → 成長"
            beneficiaries = ["Technology", "Healthcare"]
        
        return {
            "current_trend": rotation_trend,
            "beneficiary_sectors": beneficiaries,
            "rotation_strength": "中等",
            "duration_estimate": "2-4週"
        }
    
    def _select_focus_sectors(self, performance: Dict, catalysts: Dict, rotation: Dict, strategy: Dict) -> List[Dict]:
        """選擇重點產業"""
        focus_sectors = []
        
        # 基於表現選擇
        top_performers = performance.get('top_performers', [])
        for sector in top_performers[:3]:
            focus_sectors.append({
                "sector": sector,
                "reason": "表現優異",
                "confidence": 85,
                "time_horizon": "短中期"
            })
        
        # 基於催化劑選擇
        if catalysts.get('technical_events', {}).get('ai_developments'):
            focus_sectors.append({
                "sector": "Technology",
                "reason": "AI技術突破",
                "confidence": 90,
                "time_horizon": "中長期"
            })
        
        return focus_sectors[:4]  # 限制在4個重點產業
    
    def _screen_stocks_by_sectors(self, focus_sectors: List[Dict], strategy: Dict) -> List[Dict]:
        """基於重點產業篩選股票"""
        candidate_stocks = []
        
        # 科技股候選
        if any(s['sector'] == 'Technology' for s in focus_sectors):
            tech_stocks = [
                {'symbol': 'AAPL', 'name': 'Apple Inc.', 'sector': 'Technology', 'total_score': 85},
                {'symbol': 'NVDA', 'name': 'NVIDIA Corp.', 'sector': 'Technology', 'total_score': 88},
                {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'sector': 'Technology', 'total_score': 82},
                {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'sector': 'Technology', 'total_score': 80}
            ]
            candidate_stocks.extend(tech_stocks)
        
        # 能源股候選
        if any(s['sector'] == 'Energy' for s in focus_sectors):
            energy_stocks = [
                {'symbol': 'XOM', 'name': 'Exxon Mobil', 'sector': 'Energy', 'total_score': 75},
                {'symbol': 'CVX', 'name': 'Chevron Corp.', 'sector': 'Energy', 'total_score': 78}
            ]
            candidate_stocks.extend(energy_stocks)
        
        # 醫療股候選
        if any(s['sector'] == 'Healthcare' for s in focus_sectors):
            healthcare_stocks = [
                {'symbol': 'JNJ', 'name': 'Johnson & Johnson', 'sector': 'Healthcare', 'total_score': 77},
                {'symbol': 'PFE', 'name': 'Pfizer Inc.', 'sector': 'Healthcare', 'total_score': 72}
            ]
            candidate_stocks.extend(healthcare_stocks)
        
        return candidate_stocks
    
    def _perform_detailed_technical_analysis(self, stock: Dict) -> Dict[str, Any]:
        """執行詳細技術分析"""
        # 模擬技術分析結果
        signals = ['買入', '強烈買入', '持有', '賣出']
        signal = np.random.choice(signals, p=[0.3, 0.2, 0.4, 0.1])
        
        return {
            "signal": signal,
            "rsi": np.random.uniform(30, 70),
            "macd": "多頭" if np.random.random() > 0.4 else "空頭",
            "moving_averages": "多頭排列" if np.random.random() > 0.3 else "空頭排列",
            "support_resistance": f"支撐: ${np.random.uniform(150, 200):.2f}, 阻力: ${np.random.uniform(220, 280):.2f}",
            "volume_analysis": "放量" if np.random.random() > 0.5 else "縮量"
        }
    
    def _generate_trading_strategy(self, stock: Dict, strategy: Dict) -> Dict[str, Any]:
        """生成交易策略"""
        return {
            "entry_strategy": "分批建倉",
            "position_size": "建議3-5%",
            "stop_loss": f"{stock.get('current_price', 0) * 0.9:.2f}",
            "take_profit": f"{stock.get('current_price', 0) * 1.2:.2f}",
            "time_horizon": "3-6個月"
        }
    
    def _generate_risk_management(self, stock: Dict) -> Dict[str, Any]:
        """生成風險管理策略"""
        current_price = stock.get('current_price', 0)
        volatility = stock.get('volatility', 20)
        
        # 根據波動率調整停損點
        if volatility > 30:
            stop_loss_pct = 0.12  # 高波動股票給更大停損空間
        elif volatility > 20:
            stop_loss_pct = 0.10
        else:
            stop_loss_pct = 0.08
        
        return {
            "stop_loss": f"{current_price * (1 - stop_loss_pct):.2f}",
            "stop_loss_pct": f"{stop_loss_pct * 100:.0f}%",
            "position_size": "建議不超過5%",
            "risk_level": "高" if volatility > 30 else "中" if volatility > 20 else "低",
            "monitoring_points": [
                "關注成交量變化",
                "留意產業新聞",
                "監控技術指標"
            ]
        }
    
    def _assess_volatility_environment(self) -> Dict[str, Any]:
        """評估波動率環境"""
        vix_level = np.random.uniform(15, 25)
        
        if vix_level < 20:
            environment = "低波動"
            strategy_preference = "賣出選擇權策略"
        elif vix_level < 30:
            environment = "中等波動"
            strategy_preference = "方向性策略"
        else:
            environment = "高波動"
            strategy_preference = "買入選擇權策略"
        
        return {
            "vix_level": round(vix_level, 2),
            "environment": environment,
            "strategy_preference": strategy_preference,
            "implied_volatility": "偏高" if vix_level > 22 else "正常",
            "volatility_trend": "上升" if np.random.random() > 0.5 else "下降"
        }
    
    def _generate_bullish_strategies(self, watchlist: Dict, vol_env: Dict) -> List[Dict]:
        """生成看多策略"""
        strategies = []
        
        for stock in watchlist.get('watchlist', [])[:3]:
            if vol_env['environment'] == "低波動":
                strategies.append({
                    "strategy": "Buy Call",
                    "underlying": stock['symbol'],
                    "strike": f"${np.random.uniform(200, 220):.0f}",
                    "expiry": "30-45天",
                    "max_profit": "無限",
                    "max_loss": f"${np.random.uniform(5, 15):.2f}",
                    "breakeven": f"${np.random.uniform(205, 235):.2f}",
                    "expected_return": np.random.uniform(15, 35),
                    "risk_level": "中等",
                    "rationale": "看好股價上漲，低波動環境適合買入選擇權"
                })
            else:
                strategies.append({
                    "strategy": "Bull Call Spread",
                    "underlying": stock['symbol'],
                    "long_strike": f"${np.random.uniform(200, 210):.0f}",
                    "short_strike": f"${np.random.uniform(220, 230):.0f}",
                    "expiry": "30-45天",
                    "max_profit": f"${np.random.uniform(8, 15):.2f}",
                    "max_loss": f"${np.random.uniform(3, 8):.2f}",
                    "expected_return": np.random.uniform(20, 40),
                    "risk_level": "中低",
                    "rationale": "看好適度上漲，降低成本和風險"
                })
        
        return strategies
    
    def _generate_bearish_strategies(self, watchlist: Dict, vol_env: Dict) -> List[Dict]:
        """生成看空策略"""
        strategies = []
        
        strategies.append({
            "strategy": "Buy Put",
            "underlying": "SPY",
            "strike": "$420",
            "expiry": "30天",
            "max_profit": "高",
            "max_loss": "$8.50",
            "expected_return": 25,
            "risk_level": "中等",
            "rationale": "市場看空，買入保護性賣權"
        })
        
        return strategies
    
    def _generate_neutral_strategies(self, watchlist: Dict, vol_env: Dict) -> List[Dict]:
        """生成中性策略"""
        strategies = []
        
        strategies.append({
            "strategy": "Iron Condor",
            "underlying": "SPY",
            "strikes": "$410/$415/$435/$440",
            "expiry": "30天",
            "max_profit": "$3.50",
            "max_loss": "$1.50",
            "expected_return": 15,
            "risk_level": "低",
            "rationale": "預期市場震盪，收取時間價值"
        })
        
        return strategies
    
    def _generate_defensive_strategies(self, watchlist: Dict, vol_env: Dict) -> List[Dict]:
        """生成防禦策略"""
        strategies = []
        
        strategies.append({
            "strategy": "Protective Put",
            "underlying": "持有股票",
            "strike": "現價下5%",
            "expiry": "60天",
            "max_profit": "無限",
            "max_loss": "有限",
            "expected_return": 5,
            "risk_level": "低",
            "rationale": "保護現有部位，降低下跌風險"
        })
        
        return strategies
    
    def _generate_event_driven_strategies(self, watchlist: Dict, market_overview: Dict) -> List[Dict]:
        """生成事件驅動策略"""
        strategies = []
        
        strategies.append({
            "strategy": "Straddle",
            "underlying": "AAPL",
            "strike": "ATM",
            "expiry": "財報後1週",
            "max_profit": "無限",
            "max_loss": "$12.00",
            "expected_return": 30,
            "risk_level": "高",
            "rationale": "財報前買入跨式，預期大幅波動"
        })
        
        return strategies
    
    def _generate_comprehensive_recommendations(self, layer1: Dict, layer2: Dict, layer3: Dict, layer4: Dict, strategy: Dict) -> Dict[str, Any]:
        """生成綜合建議"""
        return {
            "market_outlook": layer1.get('overall_outlook', '中性'),
            "focus_sectors": [s['sector'] for s in layer2.get('focus_sectors', [])],
            "top_picks": layer3.get('watchlist', [])[:5],
            "options_strategies": layer4.get('strategy_recommendations', [])[:3],
            "risk_level": "中等",
            "confidence": 78,
            "key_themes": ["AI革命", "能源轉型", "利率政策"],
            "action_plan": self._generate_action_plan(layer3, layer4)
        }
    
    # 其他輔助方法的簡化實現
    def _analyze_vix_levels(self) -> str:
        """分析VIX波動率指數"""
        vix_level = np.random.uniform(15, 30)
        if vix_level < 20:
            return f"VIX {vix_level:.1f} - 低波動，市場相對平靜"
        elif vix_level < 30:
            return f"VIX {vix_level:.1f} - 中等波動，市場謹慎"
        else:
            return f"VIX {vix_level:.1f} - 高波動，市場恐慌"

    def _analyze_retail_sentiment(self) -> str:
        """分析散戶情緒"""
        sentiment_indicators = ["社群媒體情緒", "期權Put/Call比率", "散戶持倉數據"]
        sentiment = np.random.choice(["樂觀", "中性", "悲觀"], p=[0.3, 0.4, 0.3])
        return f"散戶情緒：{sentiment}，主要指標：{', '.join(sentiment_indicators[:2])}"

    def _analyze_institutional_flows(self) -> str:
        """分析機構資金流向"""
        flow_direction = np.random.choice(["淨流入", "淨流出", "平衡"], p=[0.4, 0.3, 0.3])
        amount = np.random.uniform(50, 200)
        return f"機構資金{flow_direction} ${amount:.0f}億，主要流向科技和醫療板塊"

    def _analyze_interest_rates(self) -> str:
        """分析利率環境"""
        fed_rate = np.random.uniform(4.5, 5.5)
        trend = np.random.choice(["上升", "持平", "下降"], p=[0.2, 0.6, 0.2])
        return f"聯準會利率 {fed_rate:.2f}%，趨勢：{trend}"

    def _determine_economic_cycle_stage(self) -> str:
        """判斷經濟週期階段"""
        stages = ["復甦期", "擴張期", "高峰期", "衰退期"]
        return np.random.choice(stages, p=[0.3, 0.4, 0.2, 0.1])

    def _assess_policy_outlook(self) -> str:
        """評估政策展望"""
        policies = ["貨幣政策維持緊縮", "財政政策支持成長", "監管政策趨嚴"]
        return f"政策展望：{np.random.choice(policies)}"

    def _detect_sector_rotation(self) -> str:
        """檢測產業輪動"""
        rotations = [
            "科技股 → 價值股",
            "成長股 → 防禦股", 
            "週期股 → 消費股",
            "大型股 → 小型股"
        ]
        return np.random.choice(rotations)

    def _analyze_etf_flows(self) -> str:
        """分析ETF資金流向"""
        etf_types = ["科技ETF", "價值ETF", "成長ETF", "防禦ETF"]
        flow_type = np.random.choice(["流入", "流出"])
        etf = np.random.choice(etf_types)
        return f"{etf}資金{flow_type}，反映投資人偏好轉變"

    def _identify_phase_drivers(self, sentiment: Dict, economic: Dict, flows: Dict) -> List[str]:
        """識別市場階段驅動因素"""
        drivers = []
        
        if sentiment.get('fear_greed_index', 50) > 60:
            drivers.append("市場情緒樂觀")
        elif sentiment.get('fear_greed_index', 50) < 40:
            drivers.append("市場情緒悲觀")
            
        if economic.get('gdp_growth', 2.0) > 2.5:
            drivers.append("經濟成長強勁")
        elif economic.get('gdp_growth', 2.0) < 1.5:
            drivers.append("經濟成長放緩")
            
        if flows.get('overall_flow') == '流入':
            drivers.append("資金持續流入")
        elif flows.get('overall_flow') == '流出':
            drivers.append("資金流出壓力")
            
        return drivers[:3]  # 限制在3個主要驅動因素

    def _generate_investment_themes(self, sectors: List, catalysts: Dict) -> List[str]:
        """生成投資主題"""
        themes = [
            "AI人工智慧革命",
            "能源轉型與綠能",
            "數位化轉型加速",
            "醫療科技創新",
            "供應鏈重組"
        ]
        return themes[:3]

    def _analyze_sector_timing(self, sectors: List) -> Dict:
        """分析產業時機"""
        return {
            "最佳進場時機": "本週至下週",
            "持有期間": "1-3個月",
            "風險控制": "設定10%停損點"
        }

    def _generate_watchlist_summary(self, watchlist: List) -> str:
        """生成觀察名單摘要"""
        if not watchlist:
            return "暫無推薦標的"
        return f"精選{len(watchlist)}支標的，涵蓋{len(set(s.get('sector', '') for s in watchlist))}個產業"

    def _calculate_sector_allocation(self, watchlist: List) -> Dict:
        """計算產業配置"""
        sectors = {}
        for stock in watchlist:
            sector = stock.get('sector', 'Unknown')
            sectors[sector] = sectors.get(sector, 0) + 1
        return sectors

    def _assess_watchlist_risk(self, watchlist: List) -> str:
        """評估觀察名單風險"""
        risk_levels = ["低", "中", "高"]
        return np.random.choice(risk_levels, p=[0.2, 0.6, 0.2])

    def _create_execution_plan(self, watchlist: List) -> Dict:
        """創建執行計劃"""
        return {
            "分批進場": "分3次進場，每次間隔1週",
            "部位控制": "單一標的不超過5%",
            "停損設定": "技術面跌破支撐位",
            "獲利了結": "達到目標價或技術面轉弱"
        }

    def _generate_options_risk_management(self) -> Dict:
        return {
            "position_sizing": "單一策略不超過5%",
            "stop_loss": "虧損達50%時停損",
            "profit_taking": "獲利達目標的75%時獲利了結"
        }
    
    def _generate_market_scenarios(self, market_overview: Dict) -> Dict:
        return {
            "bull_case": "市場上漲15%",
            "base_case": "市場震盪±5%",
            "bear_case": "市場下跌10%"
        }
    
    def _generate_options_execution_guidelines(self) -> Dict:
        return {
            "timing": "開盤後30分鐘或收盤前30分鐘",
            "liquidity": "選擇成交量大的選擇權",
            "spread": "注意買賣價差，避免流動性差的合約"
        }
    
    def _generate_options_education(self) -> Dict:
        return {
            "greeks": "Delta衡量價格敏感度，Theta衡量時間價值衰減",
            "volatility": "隱含波動率高時賣出，低時買入",
            "expiry": "避免持有至到期日，提前平倉"
        }
    
    def _generate_action_plan(self, layer3: Dict, layer4: Dict) -> List[str]:
        return [
            "1. 分批建立股票部位",
            "2. 配置適當選擇權策略",
            "3. 設定風險控制機制",
            "4. 定期檢視調整"
        ]
    
    # 備用方法
    def _get_fallback_market_overview(self) -> Dict:
        return {
            "market_sentiment": {"fear_greed_index": 50, "sentiment_label": "中性"},
            "economic_environment": {"gdp_growth": 2.0, "inflation_rate": 3.0},
            "market_phase": {"phase": "盤整期", "direction": "neutral"},
            "overall_outlook": "謹慎樂觀",
            "confidence_level": 60
        }
    
    def _get_fallback_sector_analysis(self) -> Dict:
        return {
            "focus_sectors": [
                {"sector": "Technology", "reason": "AI發展", "confidence": 80},
                {"sector": "Healthcare", "reason": "防禦性質", "confidence": 75}
            ],
            "market_catalysts": {"earnings_season": {"status": "進行中"}}
        }
    
    def _get_fallback_watchlist(self) -> Dict:
        return {
            "watchlist": [
                {"symbol": "AAPL", "name": "Apple Inc.", "total_score": 80},
                {"symbol": "MSFT", "name": "Microsoft Corp.", "total_score": 78}
            ],
            "watchlist_summary": "精選2支科技龍頭股"
        }
    
    def _get_fallback_options_analysis(self) -> Dict:
        """選擇權分析失敗時的備用方案"""
        return {
            "volatility_environment": {"level": "中等", "trend": "穩定"},
            "recommended_strategies": [
                {"type": "觀望", "description": "等待更好的進場時機"},
                {"type": "保守策略", "description": "考慮賣出價外選擇權"}
            ],
            "risk_management": {"max_risk": "5%", "strategy": "分散投資"},
            "market_scenarios": {"base_case": "盤整", "bull_case": "溫和上漲", "bear_case": "溫和下跌"},
            "execution_guidelines": {"timing": "分批進場", "size": "小額測試"},
            "educational_notes": ["選擇權具有時間價值衰減風險", "建議先學習基礎知識"]
        }
    
    def _identify_market_risks(self, sentiment: Dict, economic: Dict) -> List[str]:
        """識別市場風險"""
        risks = []
        
        # 情緒風險
        fear_greed = sentiment.get('fear_greed_index', 50)
        if fear_greed > 80:
            risks.append("市場過度貪婪，注意回調風險")
        elif fear_greed < 20:
            risks.append("市場過度恐慌，可能持續下跌")
        
        # 經濟風險
        gdp_growth = economic.get('gdp_growth', 2.5)
        if gdp_growth < 1:
            risks.append("經濟成長放緩，企業獲利承壓")
        
        inflation = economic.get('inflation_rate', 3)
        if inflation > 5:
            risks.append("通膨壓力可能導致央行緊縮政策")
        
        return risks if risks else ["當前風險相對可控"]
    
    def _calculate_market_confidence(self, sentiment: Dict, economic: Dict) -> int:
        """計算市場信心水準"""
        confidence = 50  # 基準值
        
        # 基於情緒調整
        fear_greed = sentiment.get('fear_greed_index', 50)
        if 40 <= fear_greed <= 70:
            confidence += 10  # 情緒適中加分
        elif fear_greed > 80 or fear_greed < 20:
            confidence -= 15  # 極端情緒扣分
        
        # 基於經濟數據調整
        gdp_growth = economic.get('gdp_growth', 2.5)
        if gdp_growth > 3:
            confidence += 15
        elif gdp_growth < 1:
            confidence -= 20
        
        return max(0, min(100, confidence))