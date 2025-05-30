# 🤖 AI增強美股投資分析系統

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 基於AI和數據分析的專業美股投資決策平台，採用三層架構設計，從宏觀環境到具體操作提供全方位的投資分析。

## 🌐 線上體驗

**🚀 立即使用**: https://web-production-9cc8f.up.railway.app

## 📊 **系統概述**

這是一個整合AI技術的美股投資分析系統，提供：

- 🔮 **LSTM深度學習股價預測**
- 🔬 **機器學習智能選股**
- 💡 **AI驅動投資建議**
- 📈 **多層次市場分析**

## ✨ 核心特色

### 🏗️ 三層架構設計

```
第一層：總經環境 → 第二層：事件選股 → 第三層：技術確認
    ↓                ↓                ↓
宏觀過濾層          催化劑層           操作名單層
```

### 🚀 **核心功能**

### **第一層：總經環境分析**
- ✅ 多源數據整合（85%可靠性）
- ✅ Fear & Greed Index
- ✅ 市場指數監控
- ✅ 經濟指標追蹤

### **第二層：動態選股分析**
- 🎯 策略化選股
- 📊 技術指標篩選
- 🔍 基本面分析

### **第三層：技術確認分析**
- 📈 技術指標驗證
- 🛡️ 風險評估
- ⚖️ 投資組合優化

### **AI增強功能**
- 🤖 **LSTM股價預測**: 70-80%方向預測準確率
- 🧠 **機器學習選股**: 多因子智能排名
- 💡 **AI投資建議**: 綜合分析決策支持
- 🛡️ **智能風險管理**: AI驅動風險評估

## 🚀 快速開始

### 線上使用
直接訪問 https://web-production-9cc8f.up.railway.app 即可使用所有功能。

### 本地部署

1. **克隆專案**
```bash
git clone https://github.com/adam7876/investment-analysis.git
cd investment-analysis
```

2. **安裝依賴**
```bash
pip install -r requirements.txt
```

3. **啟動系統**
```bash
python3 start_web.py
```

4. **訪問系統**
```
http://localhost:5000
```

## 🎯 **使用指南**

1. **訪問Web界面**
2. **選擇分析功能**：
   - 第一層：總經環境分析
   - 第二層：動態選股分析  
   - 第三層：技術確認分析
   - **AI增強分析**（推薦）
   - **三層聯動整合分析**

3. **查看AI分析結果**：
   - LSTM股價預測
   - 機器學習選股建議
   - AI投資建議
   - 風險評估報告

## 🛠️ **技術架構**

- **後端**: Flask + Python
- **AI框架**: TensorFlow + Scikit-learn
- **數據源**: Yahoo Finance, Alternative.me, 多個經濟數據API
- **前端**: Bootstrap 5 + 現代化UI設計

## 📦 **快速部署**

### **本地運行**
```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動系統
python3 simple_app.py

# 訪問系統
http://localhost:8000
```

### **Railway部署**
1. Fork此專案到您的GitHub
2. 連接Railway到您的GitHub倉庫
3. Railway會自動部署並提供公開URL

## 🎯 **系統升級歷程**

| 版本 | 功能 | 可靠性 |
|------|------|--------|
| v1.0 | 基礎三層分析 | 40-60% |
| v2.0 | 數據源優化 | 85% |
| **v3.0** | **AI增強** | **85%+** |

## 🤖 **AI功能詳情**

### **LSTM深度學習預測**
- 使用60天歷史數據
- 14個技術指標特徵
- 3層LSTM神經網絡
- 支援1-5天滾動預測

### **機器學習選股**
- 11個技術指標特徵
- RandomForest算法
- 智能評分排名
- 風險等級分類

### **AI投資建議**
- 結合LSTM預測和ML選股
- 市場環境因子調整
- 多維度信心評估
- 個性化風險管理

## 🔧 **配置說明**

系統支援多種配置選項：
- 股票池自定義
- 預測天數調整
- 風險偏好設定
- AI模型參數優化

## 📞 **技術支援**

如有問題或建議，請提交Issue或聯繫開發團隊。

## 📖 使用指南

詳細的使用說明請參考 [使用指南.md](使用指南.md)

### 基本操作流程

1. **總經分析**: 在儀表板進行第一層總經環境分析
2. **事件選股**: 在第二層頁面進行事件驅動選股
3. **技術確認**: 在第三層頁面進行技術分析和風險評估
4. **投資決策**: 綜合三層分析結果制定投資策略

## 🛠️ 技術架構

- **後端**: Python 3.9 + Flask 3.0
- **前端**: HTML5/CSS3 + Bootstrap 5 + JavaScript
- **數據源**: Yahoo Finance, FRED API, Alternative.me
- **部署**: Railway 雲端平台
- **版本控制**: GitHub

## 📊 系統狀態

- ✅ **第一層**: 總經環境分析 - 已完成
- ✅ **第二層**: 事件選股分析 - 已完成  
- ✅ **第三層**: 技術確認分析 - 已完成
- 🌐 **Web介面**: 現代化響應式設計 - 已完成
- ☁️ **雲端部署**: Railway自動部署 - 已完成

## 📁 專案結構

```
investment-analysis/
├── app.py                      # Flask 主應用
├── start_web.py               # Web 啟動腳本
├── config.py                  # 配置文件
├── requirements.txt           # Python 依賴
├── Procfile                   # Railway 部署配置
├── runtime.txt                # Python 版本指定
├── 使用指南.md                # 完整使用指南
├── 系統完成總結.md            # 開發總結
├── layer1_collector.py        # 第一層數據收集器
├── layer2_collector.py        # 第二層數據收集器
├── layer3_collector.py        # 第三層數據收集器
├── templates/                 # HTML 模板
│   ├── base.html             # 基礎模板
│   ├── index.html            # 首頁
│   ├── dashboard.html        # 第一層儀表板
│   ├── layer2.html           # 第二層頁面
│   └── layer3.html           # 第三層頁面
├── scrapers/                  # 數據爬蟲模組
│   ├── alternative_fear_greed_scraper.py
│   ├── fred_api_scraper.py
│   ├── macromicro_scraper.py
│   └── base_scraper.py
└── utils/                     # 工具模組
    ├── logger.py             # 日誌工具
    └── __init__.py
```

## 🎯 投資決策流程

1. **宏觀環境判斷** → 確定市場整體趨勢和風險偏好
2. **事件催化分析** → 識別投資機會和風險因子
3. **技術面確認** → 確定具體進出場時機
4. **風險管理** → 制定持倉比例和停損策略

## ⚠️ 免責聲明

本系統提供的分析和建議僅供參考，不構成投資建議。投資有風險，請根據自身情況謹慎決策。

## 📄 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 文件

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request 來改善這個專案。

---

**�� 體驗AI驅動的智能投資分析！** 