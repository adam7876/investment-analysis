# 🚀 Railway 部署指南

## 四層聯動美股投資分析系統

### 快速部署步驟

1. **連接GitHub到Railway**
   - 登入 [Railway](https://railway.app)
   - 點擊 "New Project"
   - 選擇 "Deploy from GitHub repo"
   - 選擇此專案倉庫

2. **自動部署**
   - Railway會自動檢測Python專案
   - 使用 `nixpacks.toml` 和 `railway.json` 配置
   - 自動安裝 `requirements.txt` 中的依賴

3. **環境變數設置（可選）**
   ```
   FLASK_ENV=production
   PORT=8080
   ```

4. **部署完成**
   - Railway會提供一個公開URL
   - 系統會自動啟動在指定端口

### 系統功能

✅ **第一層：市場總觀趨勢**
- 總經環境分析
- 市場情緒指標
- 資金流向分析

✅ **第二層：產業與催化劑**
- 熱門產業識別
- 催化劑分析
- 產業輪動趨勢

✅ **第三層：精選操作名單**
- 個股篩選與推薦
- 技術面分析
- 進場理由與風險評估

✅ **第四層：選擇權策略**
- 波動率環境評估
- 多種策略建議
- 風險管理計劃

### 訪問方式

部署完成後，訪問以下頁面：
- 主頁：`/`
- 四層分析：`/integrated`
- API端點：`/api/integrated-analysis`

### 技術特色

- 🔄 四層聯動分析
- 📊 實時數據整合
- 🎯 智能選擇權策略
- 💡 專業投資建議
- 🛡️ 完整風險管理 