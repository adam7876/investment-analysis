# 美股投資分析系統

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 基於AI和數據分析的專業美股投資決策平台，採用三層架構設計，從宏觀環境到具體操作提供全方位的投資分析。

## 🌐 線上體驗

**🚀 立即使用**: https://web-production-9cc8f.up.railway.app

## ✨ 核心特色

### 🏗️ 三層架構設計

```
第一層：總經環境 → 第二層：事件選股 → 第三層：技術確認
    ↓                ↓                ↓
宏觀過濾層          催化劑層           操作名單層
```

### 📊 主要功能

- **🌍 第一層：總經環境**
  - Fear & Greed Index 市場情緒分析
  - 聯準會經濟數據 (GDP、失業率、通膨率)
  - 經濟階段智能識別
  - 投資策略建議

- **📰 第二層：事件選股**
  - 財經事件日曆追蹤
  - 新聞情緒分析
  - 產業輪動分析
  - 智能選股篩選

- **📈 第三層：技術確認**
  - 深度技術指標分析 (RSI、MACD、布林帶)
  - 支撐阻力位識別
  - 交易信號生成
  - 風險管理與投資組合建議

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

**🎉 立即體驗**: https://web-production-9cc8f.up.railway.app 