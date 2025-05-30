#!/bin/bash
# AI機器學習依賴包安裝腳本

echo "🤖 開始安裝AI機器學習依賴包..."

# 更新pip
echo "📦 更新pip..."
python3 -m pip install --upgrade pip

# 安裝核心機器學習庫
echo "🧠 安裝機器學習核心庫..."
python3 -m pip install scikit-learn==1.3.2
python3 -m pip install xgboost==2.0.3

# 安裝深度學習框架
echo "🔥 安裝TensorFlow..."
python3 -m pip install tensorflow==2.15.0

# 安裝數據處理和可視化
echo "📊 安裝數據處理庫..."
python3 -m pip install matplotlib==3.8.2
python3 -m pip install seaborn==0.13.0
python3 -m pip install plotly==5.17.0

# 安裝情緒分析增強庫
echo "😊 安裝情緒分析庫..."
python3 -m pip install textblob==0.17.1
python3 -m pip install vaderSentiment==3.3.2
python3 -m pip install transformers==4.36.2

# 安裝技術分析庫
echo "📈 安裝技術分析庫..."
python3 -m pip install ta==0.10.2
python3 -m pip install TA-Lib

# 安裝其他有用的庫
echo "🔧 安裝輔助庫..."
python3 -m pip install joblib==1.3.2
python3 -m pip install tqdm==4.66.1
python3 -m pip install python-dotenv==1.0.0

# 驗證安裝
echo "✅ 驗證安裝..."
python3 -c "
import tensorflow as tf
import sklearn
import xgboost
import textblob
print('🎉 所有AI依賴包安裝成功！')
print(f'TensorFlow版本: {tf.__version__}')
print(f'Scikit-learn版本: {sklearn.__version__}')
print(f'XGBoost版本: {xgboost.__version__}')
"

echo "🚀 AI依賴包安裝完成！" 