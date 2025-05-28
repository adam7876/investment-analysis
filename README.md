# 美股投資分析系統

一套基於AI和網頁爬蟲的美股投資分析流程，採用三層邏輯分析架構。

## 🎯 系統架構

### 三層分析邏輯
1. **第一層：總經與市場環境** (✅ 已完成)
   - 市場情緒分析 (Fear & Greed Index)
   - 聯準會經濟數據 (FRED API)
   - 宏觀經濟指標分析

2. **第二層：事件與產業選股** (🚧 開發中)
   - 財經事件日曆
   - 新聞情緒分析
   - 產業輪動分析

3. **第三層：基本面與技術確認** (⏳ 規劃中)
   - 技術分析工具
   - 基本面評估
   - 風險管理系統

## 🚀 快速開始

### 方法一：Web介面 (推薦)

1. **安裝依賴**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **啟動Web介面**
   ```bash
   python3 start_web.py
   ```

3. **打開瀏覽器**
   ```
   http://localhost:5000
   ```

4. **開始使用**
   - 點擊「前往儀表板」查看分析結果
   - 點擊「快速分析」進行即時分析
   - 使用導航欄切換不同功能

### 方法二：命令行介面

1. **第一層分析**
   ```bash
   python3 layer1_collector.py
   ```

2. **功能測試**
   ```bash
   python3 test_layer1.py
   ```

## 📊 Web介面功能

### 🏠 首頁
- 系統概覽和功能介紹
- 快速開始指南
- 系統狀態監控

### 📈 儀表板
- 實時市場情緒指數
- 經濟指標展示
- 智能分析結果
- 投資建議和風險評估
- 數據匯出功能

### 🔄 自動更新
- 點擊「重新整理」獲取最新數據
- 自動顯示數據收集進度
- 即時通知系統

## 🛠️ 技術特色

### 數據源
- **Alternative.me API**: 市場情緒指數
- **FRED API**: 聯準會官方經濟數據
- **MacroMicro**: 補充經濟數據 (可選)

### 系統特性
- ✅ 多數據源備援機制
- ✅ 優雅降級處理
- ✅ 現代化Web介面
- ✅ 響應式設計
- ✅ 實時數據更新
- ✅ 智能分析引擎

## 📋 環境配置

### 必需配置
```bash
# 複製環境變數範例
cp env_example.txt .env

# 編輯配置文件
nano .env
```

### API密鑰 (可選)
```
# FRED API (聯準會數據)
FRED_API_KEY=your_fred_api_key_here

# 其他API密鑰...
```

**注意**: 即使沒有API密鑰，系統也會使用模擬數據正常運行。

## 🎮 使用指南

### Web介面操作
1. **首次使用**: 訪問首頁了解系統功能
2. **數據分析**: 前往儀表板查看分析結果
3. **重新整理**: 點擊重新整理按鈕獲取最新數據
4. **匯出報告**: 使用匯出功能保存分析結果

### 命令行操作
```bash
# 完整分析報告
python3 layer1_collector.py

# 快速測試
python3 test_layer1.py

# 啟動Web介面
python3 start_web.py
```

## 📁 項目結構

```
select/
├── app.py                 # Flask Web應用程式
├── start_web.py          # Web介面啟動腳本
├── layer1_collector.py   # 第一層數據收集器
├── test_layer1.py        # 功能測試
├── config.py             # 系統配置
├── requirements.txt      # 依賴清單
├── templates/            # HTML模板
│   ├── base.html        # 基礎模板
│   ├── index.html       # 首頁
│   ├── dashboard.html   # 儀表板
│   ├── layer2.html      # 第二層頁面
│   └── layer3.html      # 第三層頁面
├── scrapers/            # 爬蟲模組
│   ├── alternative_fear_greed_scraper.py
│   ├── fred_api_scraper.py
│   └── macromicro_scraper.py
├── utils/               # 工具模組
└── logs/               # 日誌文件
```

## 🔧 故障排除

### 常見問題

1. **Flask未安裝**
   ```bash
   pip3 install Flask==3.0.0
   ```

2. **端口被占用**
   ```bash
   # 查找占用端口的進程
   lsof -i :5000
   # 終止進程
   kill -9 <PID>
   ```

3. **數據獲取失敗**
   - 檢查網路連接
   - 確認API密鑰設置
   - 查看logs/目錄下的日誌文件

### 日誌查看
```bash
# 查看最新日誌
tail -f logs/app_*.log
```

## 📈 系統狀態

### 第一層功能 ✅
- [x] Fear & Greed Index 收集
- [x] FRED 經濟數據收集
- [x] 市場環境分析
- [x] 投資建議生成
- [x] Web介面展示

### 第二層功能 🚧
- [ ] 財經事件日曆
- [ ] 新聞情緒分析
- [ ] 產業輪動分析
- [ ] 選股篩選器

### 第三層功能 ⏳
- [ ] 技術分析工具
- [ ] 基本面評估
- [ ] 風險管理系統
- [ ] 選擇權策略

## 🤝 貢獻指南

歡迎提交Issue和Pull Request來改進系統！

## 📄 授權

本項目採用MIT授權條款。 