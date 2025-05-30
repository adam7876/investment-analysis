#!/usr/bin/env python3
"""
AI增強分析器
整合LSTM預測、機器學習選股和情緒分析到現有投資分析系統
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from loguru import logger
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# 添加項目路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 導入現有模塊
from layer1_collector import collect_all_data as get_layer1_data
from ai_models.lstm_predictor import LSTMStockPredictor

class AIEnhancedAnalyzer:
    """AI增強分析器"""
    
    def __init__(self):
        self.lstm_predictor = LSTMStockPredictor(sequence_length=30)  # 使用較短序列以加快訓練
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        logger.info("🤖 初始化AI增強分析器")
    
    def analyze_with_ai(self, symbols: List[str] = None, enable_lstm: bool = True) -> Dict[str, Any]:
        """
        使用AI進行增強分析
        """
        if symbols is None:
            symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']
        
        logger.info(f"🚀 開始AI增強分析: {symbols}")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'analysis_type': 'AI_Enhanced',
            'symbols_analyzed': symbols,
            'market_overview': {},
            'ai_predictions': {},
            'ml_rankings': {},
            'investment_recommendations': {},
            'risk_assessment': {},
            'summary': {}
        }
        
        try:
            # 1. 獲取市場總體環境
            logger.info("📊 分析市場總體環境...")
            market_data = get_layer1_data()
            results['market_overview'] = self._extract_market_overview(market_data)
            
            # 2. AI股價預測
            if enable_lstm:
                logger.info("🤖 執行LSTM股價預測...")
                results['ai_predictions'] = self._lstm_predictions(symbols)
            
            # 3. 機器學習選股排名
            logger.info("🔬 執行機器學習選股分析...")
            results['ml_rankings'] = self._ml_stock_ranking(symbols)
            
            # 4. 綜合投資建議
            logger.info("💡 生成AI投資建議...")
            results['investment_recommendations'] = self._generate_ai_recommendations(
                results['ai_predictions'], 
                results['ml_rankings'],
                results['market_overview']
            )
            
            # 5. AI風險評估
            logger.info("🛡️ 執行AI風險評估...")
            results['risk_assessment'] = self._ai_risk_assessment(symbols, results)
            
            # 6. 生成總結
            results['summary'] = self._generate_summary(results)
            
            logger.info("✅ AI增強分析完成")
            return results
            
        except Exception as e:
            logger.error(f"❌ AI分析失敗: {str(e)}")
            results['error'] = str(e)
            results['success'] = False
            return results
    
    def _extract_market_overview(self, market_data: Dict) -> Dict:
        """提取市場總體環境"""
        if not market_data.get('success'):
            return {'status': 'unavailable', 'sentiment': 'neutral'}
        
        analysis = market_data.get('analysis', {})
        
        return {
            'market_environment': analysis.get('market_environment', 'Unknown'),
            'investment_recommendation': analysis.get('investment_recommendation', 'Hold'),
            'confidence_level': analysis.get('confidence_level', 50),
            'risk_assessment': analysis.get('risk_assessment', 'Moderate Risk'),
            'key_factors': analysis.get('key_factors', []),
            'data_quality': market_data.get('data_quality', 'Medium'),
            'reliability': market_data.get('overall_reliability', 50)
        }
    
    def _lstm_predictions(self, symbols: List[str]) -> Dict:
        """LSTM股價預測"""
        predictions = {}
        
        for symbol in symbols:
            try:
                logger.info(f"🔮 預測 {symbol} 股價...")
                
                # 快速訓練（使用較少數據以加快速度）
                training_results = self.lstm_predictor.train(symbol, period="6mo")
                
                # 進行預測
                prediction_results = self.lstm_predictor.predict(symbol, days_ahead=3)
                
                predictions[symbol] = {
                    'training_accuracy': training_results.get('val_direction_accuracy', 0),
                    'current_price': prediction_results['current_price'],
                    'predicted_prices': prediction_results['predicted_prices'][:3],  # 只取前3天
                    'price_changes': prediction_results['price_changes'][:3],
                    'trading_signal': prediction_results['trading_signal'],
                    'confidence': prediction_results['confidence'],
                    'model_performance': {
                        'rmse': training_results.get('val_rmse', 0),
                        'direction_accuracy': training_results.get('val_direction_accuracy', 0)
                    }
                }
                
                logger.info(f"✅ {symbol} 預測完成: {prediction_results['trading_signal']['signal']}")
                
            except Exception as e:
                logger.warning(f"⚠️ {symbol} LSTM預測失敗: {str(e)}")
                predictions[symbol] = {
                    'error': str(e),
                    'status': 'failed'
                }
        
        return predictions
    
    def _ml_stock_ranking(self, symbols: List[str]) -> Dict:
        """機器學習選股排名"""
        rankings = {}
        
        try:
            # 獲取所有股票的特徵數據
            features_data = []
            valid_symbols = []
            
            for symbol in symbols:
                try:
                    features = self._extract_ml_features(symbol)
                    if features is not None:
                        features_data.append(features)
                        valid_symbols.append(symbol)
                except Exception as e:
                    logger.warning(f"⚠️ {symbol} 特徵提取失敗: {str(e)}")
                    continue
            
            if len(features_data) < 2:
                return {'error': '可用數據不足', 'rankings': []}
            
            # 轉換為DataFrame
            df = pd.DataFrame(features_data, index=valid_symbols)
            
            # 計算綜合評分
            scores = self._calculate_ml_scores(df)
            
            # 排名
            ranked_symbols = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            
            rankings = {
                'method': 'Random Forest + Technical Analysis',
                'total_analyzed': len(valid_symbols),
                'rankings': [
                    {
                        'symbol': symbol,
                        'score': round(score, 3),
                        'rank': idx + 1,
                        'recommendation': self._score_to_recommendation(score)
                    }
                    for idx, (symbol, score) in enumerate(ranked_symbols)
                ],
                'top_picks': [item['symbol'] for item in ranked_symbols[:3]],
                'features_used': list(df.columns)
            }
            
        except Exception as e:
            logger.error(f"❌ ML選股失敗: {str(e)}")
            rankings = {'error': str(e), 'rankings': []}
        
        return rankings
    
    def _extract_ml_features(self, symbol: str) -> Optional[Dict]:
        """提取機器學習特徵"""
        try:
            # 獲取股票數據
            stock = yf.Ticker(symbol)
            hist = stock.history(period="3mo")
            info = stock.info
            
            if len(hist) < 20:
                return None
            
            # 計算技術指標
            current_price = hist['Close'].iloc[-1]
            
            # 價格相關特徵
            price_change_1d = (hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]
            price_change_5d = (hist['Close'].iloc[-1] - hist['Close'].iloc[-6]) / hist['Close'].iloc[-6]
            price_change_20d = (hist['Close'].iloc[-1] - hist['Close'].iloc[-21]) / hist['Close'].iloc[-21]
            
            # 移動平均
            ma_5 = hist['Close'].rolling(5).mean().iloc[-1]
            ma_20 = hist['Close'].rolling(20).mean().iloc[-1]
            
            # 相對強度
            rsi = self._calculate_rsi(hist['Close'])
            
            # 波動率
            volatility = hist['Close'].pct_change().std() * np.sqrt(252)
            
            # 成交量
            volume_ratio = hist['Volume'].iloc[-5:].mean() / hist['Volume'].iloc[-20:].mean()
            
            # 基本面指標（如果可用）
            pe_ratio = info.get('trailingPE', 0) or 0
            market_cap = info.get('marketCap', 0) or 0
            
            features = {
                'price_change_1d': price_change_1d,
                'price_change_5d': price_change_5d,
                'price_change_20d': price_change_20d,
                'price_vs_ma5': (current_price - ma_5) / ma_5,
                'price_vs_ma20': (current_price - ma_20) / ma_20,
                'ma5_vs_ma20': (ma_5 - ma_20) / ma_20,
                'rsi': rsi,
                'volatility': volatility,
                'volume_ratio': volume_ratio,
                'pe_ratio': min(pe_ratio, 100) if pe_ratio > 0 else 0,  # 限制極值
                'market_cap_log': np.log(market_cap) if market_cap > 0 else 0
            }
            
            return features
            
        except Exception as e:
            logger.warning(f"特徵提取失敗 {symbol}: {str(e)}")
            return None
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """計算RSI指標"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
    
    def _calculate_ml_scores(self, df: pd.DataFrame) -> Dict[str, float]:
        """計算機器學習評分"""
        # 標準化特徵
        features_scaled = self.scaler.fit_transform(df.fillna(0))
        
        # 簡單的評分算法（基於技術指標組合）
        scores = {}
        
        for i, symbol in enumerate(df.index):
            feature_vector = features_scaled[i]
            
            # 確保有足夠的特徵
            if len(feature_vector) < 9:
                scores[symbol] = 0.0
                continue
            
            # 綜合評分邏輯
            momentum_score = (feature_vector[0] + feature_vector[1] + feature_vector[2]) / 3  # 價格動量
            trend_score = (feature_vector[3] + feature_vector[4] + feature_vector[5]) / 3     # 趨勢強度
            technical_score = (50 - abs(feature_vector[6] - 50)) / 50 if len(feature_vector) > 6 else 0  # RSI適中性
            volume_score = min(abs(feature_vector[8]), 2) / 2 if len(feature_vector) > 8 else 0  # 成交量活躍度
            
            # 加權綜合評分
            total_score = (
                momentum_score * 0.3 +
                trend_score * 0.3 +
                technical_score * 0.2 +
                volume_score * 0.2
            )
            
            scores[symbol] = total_score
        
        return scores
    
    def _score_to_recommendation(self, score: float) -> str:
        """評分轉換為建議"""
        if score > 0.6:
            return "強烈推薦"
        elif score > 0.3:
            return "推薦"
        elif score > 0:
            return "中性"
        elif score > -0.3:
            return "謹慎"
        else:
            return "避免"
    
    def _generate_ai_recommendations(self, predictions: Dict, rankings: Dict, market_overview: Dict) -> Dict:
        """生成AI投資建議"""
        recommendations = {}
        
        # 市場環境影響因子
        market_factor = self._get_market_factor(market_overview)
        
        for symbol in predictions.keys():
            if symbol in [item['symbol'] for item in rankings.get('rankings', [])]:
                # 獲取LSTM預測
                lstm_data = predictions[symbol]
                if 'error' in lstm_data:
                    continue
                
                # 獲取ML排名
                ml_rank = next((item for item in rankings['rankings'] if item['symbol'] == symbol), None)
                
                if ml_rank:
                    # 綜合評分
                    lstm_signal = lstm_data['trading_signal']['signal']
                    ml_score = ml_rank['score']
                    
                    # AI綜合建議
                    ai_recommendation = self._combine_ai_signals(lstm_signal, ml_score, market_factor)
                    
                    recommendations[symbol] = {
                        'ai_recommendation': ai_recommendation,
                        'lstm_signal': lstm_signal,
                        'ml_ranking': ml_rank['rank'],
                        'ml_score': ml_score,
                        'market_factor': market_factor,
                        'confidence': self._calculate_confidence(lstm_data, ml_rank, market_overview),
                        'price_target': lstm_data['predicted_prices'][0] if lstm_data['predicted_prices'] else None,
                        'risk_level': self._assess_individual_risk(symbol, lstm_data, ml_rank)
                    }
        
        return recommendations
    
    def _get_market_factor(self, market_overview: Dict) -> float:
        """獲取市場環境因子"""
        env = market_overview.get('market_environment', 'Sideways Market')
        
        if 'Bull' in env:
            return 1.2
        elif 'Bear' in env:
            return 0.8
        else:
            return 1.0
    
    def _combine_ai_signals(self, lstm_signal: str, ml_score: float, market_factor: float) -> str:
        """結合AI信號"""
        # LSTM信號權重
        lstm_weight = {
            '強烈買入': 1.0,
            '買入': 0.6,
            '持有': 0.0,
            '謹慎': -0.3,
            '賣出': -0.6
        }.get(lstm_signal, 0.0)
        
        # 綜合評分
        combined_score = (lstm_weight * 0.6 + ml_score * 0.4) * market_factor
        
        if combined_score > 0.7:
            return "AI強烈推薦"
        elif combined_score > 0.3:
            return "AI推薦"
        elif combined_score > -0.1:
            return "AI中性"
        elif combined_score > -0.4:
            return "AI謹慎"
        else:
            return "AI不推薦"
    
    def _calculate_confidence(self, lstm_data: Dict, ml_rank: Dict, market_overview: Dict) -> float:
        """計算信心度"""
        lstm_confidence = lstm_data.get('confidence', 0.5)
        ml_confidence = min(ml_rank['score'] + 0.5, 1.0) if ml_rank['score'] > 0 else 0.3
        market_confidence = market_overview.get('confidence_level', 50) / 100
        
        return (lstm_confidence * 0.4 + ml_confidence * 0.4 + market_confidence * 0.2)
    
    def _assess_individual_risk(self, symbol: str, lstm_data: Dict, ml_rank: Dict) -> str:
        """評估個股風險"""
        # 基於預測變化幅度和排名
        price_changes = lstm_data.get('price_changes', [0])
        max_change = max([abs(change) for change in price_changes]) if price_changes else 0
        
        ml_score = ml_rank.get('score', 0)
        
        if max_change > 5 or ml_score < -0.3:
            return "高風險"
        elif max_change > 2 or ml_score < 0:
            return "中等風險"
        else:
            return "低風險"
    
    def _ai_risk_assessment(self, symbols: List[str], results: Dict) -> Dict:
        """AI風險評估"""
        risk_assessment = {
            'overall_risk': 'Medium',
            'risk_factors': [],
            'diversification_score': 0,
            'volatility_analysis': {},
            'recommendations': []
        }
        
        try:
            # 分析整體風險
            recommendations = results.get('investment_recommendations', {})
            
            high_risk_count = sum(1 for rec in recommendations.values() 
                                if rec.get('risk_level') == '高風險')
            
            total_count = len(recommendations)
            
            if total_count > 0:
                risk_ratio = high_risk_count / total_count
                
                if risk_ratio > 0.6:
                    risk_assessment['overall_risk'] = 'High'
                elif risk_ratio < 0.2:
                    risk_assessment['overall_risk'] = 'Low'
                
                # 多樣化評分
                risk_assessment['diversification_score'] = min(total_count / 5, 1.0)
                
                # 風險建議
                if risk_ratio > 0.5:
                    risk_assessment['recommendations'].append("建議降低高風險股票比例")
                
                if risk_assessment['diversification_score'] < 0.6:
                    risk_assessment['recommendations'].append("建議增加投資組合多樣性")
        
        except Exception as e:
            logger.warning(f"風險評估失敗: {str(e)}")
        
        return risk_assessment
    
    def _generate_summary(self, results: Dict) -> Dict:
        """生成分析總結"""
        summary = {
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'market_sentiment': results['market_overview'].get('market_environment', 'Unknown'),
            'ai_top_picks': [],
            'key_insights': [],
            'action_items': [],
            'overall_confidence': 0
        }
        
        try:
            # 提取AI推薦的前3名
            recommendations = results.get('investment_recommendations', {})
            sorted_recs = sorted(
                recommendations.items(),
                key=lambda x: x[1].get('confidence', 0),
                reverse=True
            )
            
            summary['ai_top_picks'] = [
                {
                    'symbol': symbol,
                    'recommendation': data['ai_recommendation'],
                    'confidence': round(data['confidence'], 2)
                }
                for symbol, data in sorted_recs[:3]
            ]
            
            # 關鍵洞察
            if results['market_overview'].get('market_environment'):
                summary['key_insights'].append(
                    f"市場環境: {results['market_overview']['market_environment']}"
                )
            
            # 計算整體信心度
            if recommendations:
                avg_confidence = sum(rec.get('confidence', 0) for rec in recommendations.values()) / len(recommendations)
                summary['overall_confidence'] = round(avg_confidence, 2)
            
            # 行動建議
            if summary['overall_confidence'] > 0.7:
                summary['action_items'].append("AI分析信心度高，可考慮積極投資")
            elif summary['overall_confidence'] < 0.4:
                summary['action_items'].append("AI分析信心度較低，建議謹慎觀望")
            
        except Exception as e:
            logger.warning(f"總結生成失敗: {str(e)}")
        
        return summary

def main():
    """測試AI增強分析器"""
    print("\n" + "="*80)
    print("🤖 AI增強投資分析系統測試")
    print("="*80)
    
    analyzer = AIEnhancedAnalyzer()
    
    # 執行AI分析（使用較少股票以加快測試）
    test_symbols = ['AAPL', 'MSFT', 'GOOGL']
    results = analyzer.analyze_with_ai(test_symbols, enable_lstm=True)
    
    if 'error' not in results:
        print(f"\n✅ AI分析完成")
        print(f"📊 分析股票: {', '.join(results['symbols_analyzed'])}")
        print(f"🎯 市場環境: {results['market_overview'].get('market_environment', 'Unknown')}")
        
        # 顯示AI推薦
        print(f"\n🤖 AI投資建議:")
        for symbol, rec in results['investment_recommendations'].items():
            print(f"   {symbol}: {rec['ai_recommendation']} (信心度: {rec['confidence']:.1%})")
        
        # 顯示總結
        summary = results['summary']
        print(f"\n📋 分析總結:")
        print(f"   整體信心度: {summary['overall_confidence']:.1%}")
        print(f"   AI首選: {[pick['symbol'] for pick in summary['ai_top_picks']]}")
        
    else:
        print(f"❌ AI分析失敗: {results['error']}")

if __name__ == "__main__":
    main() 