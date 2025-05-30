#!/usr/bin/env python3
"""
LSTM股價預測模型
使用深度學習進行時間序列預測，提升系統AI能力
"""

import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from loguru import logger
from typing import Dict, List, Tuple, Optional
import joblib
import os

class LSTMStockPredictor:
    """LSTM股價預測器"""
    
    def __init__(self, sequence_length: int = 60, prediction_days: int = 1):
        self.sequence_length = sequence_length  # 使用過去60天數據
        self.prediction_days = prediction_days  # 預測未來1天
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.feature_columns = [
            'Close', 'Volume', 'High', 'Low', 'Open',
            'MA_5', 'MA_10', 'MA_20', 'MA_50',
            'RSI', 'MACD', 'BB_upper', 'BB_lower', 'Volatility'
        ]
        
    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """準備特徵數據"""
        df = data.copy()
        
        # 移動平均線
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_10'] = df['Close'].rolling(window=10).mean()
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        df['MA_50'] = df['Close'].rolling(window=50).mean()
        
        # RSI指標
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD指標
        exp1 = df['Close'].ewm(span=12).mean()
        exp2 = df['Close'].ewm(span=26).mean()
        df['MACD'] = exp1 - exp2
        
        # 布林通道
        bb_period = 20
        bb_std = df['Close'].rolling(window=bb_period).std()
        bb_ma = df['Close'].rolling(window=bb_period).mean()
        df['BB_upper'] = bb_ma + (bb_std * 2)
        df['BB_lower'] = bb_ma - (bb_std * 2)
        
        # 波動率
        df['Volatility'] = df['Close'].pct_change().rolling(window=20).std()
        
        # 填充缺失值
        df = df.fillna(method='bfill').fillna(method='ffill')
        
        return df
    
    def create_sequences(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """創建LSTM訓練序列"""
        X, y = [], []
        
        for i in range(self.sequence_length, len(data) - self.prediction_days + 1):
            # 輸入序列（過去60天的多個特徵）
            X.append(data[i - self.sequence_length:i])
            # 目標值（未來1天的收盤價）
            y.append(data[i + self.prediction_days - 1, 0])  # 收盤價在第0列
        
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape: Tuple[int, int]) -> Sequential:
        """構建LSTM模型"""
        model = Sequential([
            # 第一層LSTM
            LSTM(units=100, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            BatchNormalization(),
            
            # 第二層LSTM
            LSTM(units=100, return_sequences=True),
            Dropout(0.2),
            BatchNormalization(),
            
            # 第三層LSTM
            LSTM(units=50, return_sequences=False),
            Dropout(0.2),
            BatchNormalization(),
            
            # 全連接層
            Dense(units=25, activation='relu'),
            Dropout(0.1),
            
            # 輸出層
            Dense(units=1)
        ])
        
        # 編譯模型
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def train(self, symbol: str, period: str = "2y", validation_split: float = 0.2) -> Dict:
        """訓練模型"""
        logger.info(f"🤖 開始訓練LSTM模型：{symbol}")
        
        try:
            # 獲取數據
            stock_data = yf.download(symbol, period=period)
            if len(stock_data) < self.sequence_length + 50:
                raise ValueError(f"數據量不足，需要至少{self.sequence_length + 50}天數據")
            
            # 準備特徵
            df = self.prepare_features(stock_data)
            
            # 選擇特徵列
            feature_data = df[self.feature_columns].values
            
            # 數據標準化
            scaled_data = self.scaler.fit_transform(feature_data)
            
            # 創建序列
            X, y = self.create_sequences(scaled_data)
            
            # 分割訓練和驗證集
            split_idx = int(len(X) * (1 - validation_split))
            X_train, X_val = X[:split_idx], X[split_idx:]
            y_train, y_val = y[:split_idx], y[split_idx:]
            
            logger.info(f"訓練集大小: {X_train.shape}, 驗證集大小: {X_val.shape}")
            
            # 構建模型
            self.model = self.build_model((X_train.shape[1], X_train.shape[2]))
            
            # 設置回調函數
            callbacks = [
                EarlyStopping(patience=10, restore_best_weights=True),
                ReduceLROnPlateau(factor=0.5, patience=5, min_lr=0.0001)
            ]
            
            # 訓練模型
            history = self.model.fit(
                X_train, y_train,
                epochs=100,
                batch_size=32,
                validation_data=(X_val, y_val),
                callbacks=callbacks,
                verbose=1
            )
            
            # 評估模型
            train_pred = self.model.predict(X_train)
            val_pred = self.model.predict(X_val)
            
            # 反標準化預測結果
            train_pred_rescaled = self.inverse_transform_predictions(train_pred)
            val_pred_rescaled = self.inverse_transform_predictions(val_pred)
            y_train_rescaled = self.inverse_transform_predictions(y_train.reshape(-1, 1))
            y_val_rescaled = self.inverse_transform_predictions(y_val.reshape(-1, 1))
            
            # 計算評估指標
            train_rmse = np.sqrt(mean_squared_error(y_train_rescaled, train_pred_rescaled))
            val_rmse = np.sqrt(mean_squared_error(y_val_rescaled, val_pred_rescaled))
            train_mae = mean_absolute_error(y_train_rescaled, train_pred_rescaled)
            val_mae = mean_absolute_error(y_val_rescaled, val_pred_rescaled)
            
            # 計算準確率（方向預測準確率）
            train_direction_accuracy = self.calculate_direction_accuracy(
                y_train_rescaled, train_pred_rescaled
            )
            val_direction_accuracy = self.calculate_direction_accuracy(
                y_val_rescaled, val_pred_rescaled
            )
            
            results = {
                'symbol': symbol,
                'training_samples': len(X_train),
                'validation_samples': len(X_val),
                'train_rmse': float(train_rmse),
                'val_rmse': float(val_rmse),
                'train_mae': float(train_mae),
                'val_mae': float(val_mae),
                'train_direction_accuracy': float(train_direction_accuracy),
                'val_direction_accuracy': float(val_direction_accuracy),
                'epochs_trained': len(history.history['loss']),
                'final_loss': float(history.history['val_loss'][-1])
            }
            
            logger.info(f"✅ 模型訓練完成")
            logger.info(f"📊 驗證集RMSE: {val_rmse:.2f}")
            logger.info(f"📈 方向預測準確率: {val_direction_accuracy:.1%}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ 模型訓練失敗: {str(e)}")
            raise
    
    def predict(self, symbol: str, days_ahead: int = 1) -> Dict:
        """預測股價"""
        if self.model is None:
            raise ValueError("模型尚未訓練，請先調用train()方法")
        
        try:
            # 獲取最新數據
            stock_data = yf.download(symbol, period="3mo")  # 獲取3個月數據
            df = self.prepare_features(stock_data)
            
            # 準備最新的序列數據
            feature_data = df[self.feature_columns].values
            scaled_data = self.scaler.transform(feature_data)
            
            # 取最後sequence_length天的數據
            last_sequence = scaled_data[-self.sequence_length:].reshape(1, self.sequence_length, -1)
            
            # 預測
            predictions = []
            current_sequence = last_sequence.copy()
            
            for _ in range(days_ahead):
                pred = self.model.predict(current_sequence, verbose=0)
                predictions.append(pred[0, 0])
                
                # 更新序列（滾動預測）
                if days_ahead > 1:
                    # 創建新的特徵向量（簡化版本，實際應用中需要更複雜的邏輯）
                    new_features = current_sequence[0, -1, :].copy()
                    new_features[0] = pred[0, 0]  # 更新收盤價
                    
                    # 滾動更新序列
                    current_sequence = np.roll(current_sequence, -1, axis=1)
                    current_sequence[0, -1, :] = new_features
            
            # 反標準化預測結果
            predictions_rescaled = self.inverse_transform_predictions(
                np.array(predictions).reshape(-1, 1)
            )
            
            # 獲取當前價格
            current_price = float(stock_data['Close'].iloc[-1])
            
            # 計算預測變化
            predicted_prices = predictions_rescaled.flatten()
            price_changes = [(price - current_price) / current_price * 100 
                           for price in predicted_prices]
            
            # 生成預測信號
            signal = self.generate_trading_signal(current_price, predicted_prices[0])
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'predicted_prices': predicted_prices.tolist(),
                'price_changes': price_changes,
                'prediction_dates': self.get_prediction_dates(days_ahead),
                'trading_signal': signal,
                'confidence': self.calculate_prediction_confidence(predictions),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ 預測失敗: {str(e)}")
            raise
    
    def inverse_transform_predictions(self, predictions: np.ndarray) -> np.ndarray:
        """反標準化預測結果"""
        # 創建與原始特徵相同形狀的數組
        dummy_features = np.zeros((predictions.shape[0], len(self.feature_columns)))
        dummy_features[:, 0] = predictions.flatten()  # 收盤價在第0列
        
        # 反標準化
        rescaled = self.scaler.inverse_transform(dummy_features)
        return rescaled[:, 0].reshape(-1, 1)
    
    def calculate_direction_accuracy(self, actual: np.ndarray, predicted: np.ndarray) -> float:
        """計算方向預測準確率"""
        if len(actual) <= 1:
            return 0.0
        
        actual_direction = np.diff(actual.flatten()) > 0
        predicted_direction = np.diff(predicted.flatten()) > 0
        
        return np.mean(actual_direction == predicted_direction)
    
    def generate_trading_signal(self, current_price: float, predicted_price: float) -> Dict:
        """生成交易信號"""
        change_percent = (predicted_price - current_price) / current_price * 100
        
        if change_percent > 2:
            signal = "強烈買入"
            confidence = "高"
        elif change_percent > 0.5:
            signal = "買入"
            confidence = "中"
        elif change_percent < -2:
            signal = "賣出"
            confidence = "高"
        elif change_percent < -0.5:
            signal = "謹慎"
            confidence = "中"
        else:
            signal = "持有"
            confidence = "低"
        
        return {
            'signal': signal,
            'confidence': confidence,
            'expected_change': round(change_percent, 2)
        }
    
    def calculate_prediction_confidence(self, predictions: List[float]) -> float:
        """計算預測信心度"""
        # 基於預測的一致性和模型性能計算信心度
        if len(predictions) == 1:
            return 0.75  # 單點預測的基礎信心度
        
        # 計算預測的變異性
        pred_std = np.std(predictions)
        pred_mean = np.mean(predictions)
        
        # 變異係數越小，信心度越高
        cv = pred_std / pred_mean if pred_mean != 0 else 1
        confidence = max(0.5, 1 - cv)
        
        return min(0.95, confidence)
    
    def get_prediction_dates(self, days_ahead: int) -> List[str]:
        """獲取預測日期"""
        dates = []
        current_date = datetime.now()
        
        for i in range(1, days_ahead + 1):
            # 跳過週末
            pred_date = current_date + timedelta(days=i)
            while pred_date.weekday() >= 5:  # 週六=5, 週日=6
                pred_date += timedelta(days=1)
            dates.append(pred_date.strftime('%Y-%m-%d'))
        
        return dates
    
    def save_model(self, filepath: str):
        """保存模型"""
        if self.model is None:
            raise ValueError("沒有訓練好的模型可以保存")
        
        # 創建目錄
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # 保存Keras模型
        self.model.save(f"{filepath}_model.h5")
        
        # 保存標準化器
        joblib.dump(self.scaler, f"{filepath}_scaler.pkl")
        
        logger.info(f"✅ 模型已保存到: {filepath}")
    
    def load_model(self, filepath: str):
        """載入模型"""
        try:
            # 載入Keras模型
            self.model = tf.keras.models.load_model(f"{filepath}_model.h5")
            
            # 載入標準化器
            self.scaler = joblib.load(f"{filepath}_scaler.pkl")
            
            logger.info(f"✅ 模型已載入: {filepath}")
            
        except Exception as e:
            logger.error(f"❌ 模型載入失敗: {str(e)}")
            raise

def main():
    """示例用法"""
    # 創建預測器
    predictor = LSTMStockPredictor(sequence_length=60)
    
    # 訓練模型
    symbol = "AAPL"
    training_results = predictor.train(symbol, period="2y")
    
    print("\n" + "="*50)
    print("🤖 LSTM股價預測模型訓練結果")
    print("="*50)
    print(f"股票代號: {training_results['symbol']}")
    print(f"驗證集RMSE: {training_results['val_rmse']:.2f}")
    print(f"方向預測準確率: {training_results['val_direction_accuracy']:.1%}")
    
    # 進行預測
    prediction_results = predictor.predict(symbol, days_ahead=5)
    
    print(f"\n📈 未來5天預測結果:")
    print(f"當前價格: ${prediction_results['current_price']:.2f}")
    
    for i, (date, price, change) in enumerate(zip(
        prediction_results['prediction_dates'],
        prediction_results['predicted_prices'],
        prediction_results['price_changes']
    )):
        print(f"第{i+1}天 ({date}): ${price:.2f} ({change:+.1f}%)")
    
    print(f"\n🎯 交易建議: {prediction_results['trading_signal']['signal']}")
    print(f"信心度: {prediction_results['confidence']:.1%}")

if __name__ == "__main__":
    main() 