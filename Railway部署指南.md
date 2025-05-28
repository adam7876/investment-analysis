# 🚂 Railway部署指南

## 📋 問題描述

Railway有時候可能不會自動觸發部署，即使代碼已經推送到GitHub。這是一個已知的問題，可能由以下原因造成：

1. **GitHub Webhook失敗**：GitHub向Railway發送的webhook請求可能失敗
2. **Railway服務暫時性問題**：Railway的自動部署服務可能暫時不可用
3. **配置問題**：部署分支或觸發條件可能需要調整

## 🔧 解決方案

### 方案1：手動觸發部署（立即解決）

1. 打開 [Railway控制台](https://railway.app)
2. 進入您的專案
3. 選擇對應的服務
4. 使用快捷鍵：`Cmd + K`（Mac）或 `Ctrl + K`（Windows/Linux）
5. 輸入 "Deploy latest commit" 並按Enter
6. 等待部署完成

### 方案2：GitHub Action自動部署（長期解決）

我們已經創建了 `.github/workflows/railway-deploy.yml` 檔案，它會：

- ✅ 每次推送到 `main` 分支時自動部署
- ✅ 支援手動觸發部署
- ✅ 提供部署狀態通知
- ✅ 使用最新的Railway CLI

#### 設置步驟：

1. **確保RAILWAY_TOKEN已設置**：
   - 在GitHub repository中，進入 Settings → Secrets and variables → Actions
   - 確認 `RAILWAY_TOKEN` 已經添加

2. **手動觸發部署**：
   - 進入GitHub repository的 Actions 頁面
   - 選擇 "🚀 Railway Auto Deploy" workflow
   - 點擊 "Run workflow" 按鈕

### 方案3：檢查Railway設置

1. **確認部署分支**：
   - 在Railway控制台中，檢查服務設置
   - 確認 "Source" 設置為正確的GitHub repository和分支

2. **檢查webhook**：
   - 在GitHub repository設置中，查看 Webhooks 頁面
   - 確認Railway的webhook存在且狀態正常

## 📊 部署狀態檢查

### 當前部署資訊：
- **網站地址**：https://web-production-9cc8f.up.railway.app
- **GitHub Repository**：https://github.com/adam7876/investment-analysis
- **部署分支**：main

### 檢查部署是否成功：

```bash
# 檢查網站是否可訪問
curl -I https://web-production-9cc8f.up.railway.app

# 檢查特定功能是否已部署
curl -s "https://web-production-9cc8f.up.railway.app/layer2" | grep "調試資訊"
```

## 🚨 故障排除

### 如果GitHub Action失敗：

1. **檢查RAILWAY_TOKEN**：
   - 確認token有效且權限正確
   - 在Railway控制台重新生成token

2. **檢查workflow日誌**：
   - 在GitHub Actions頁面查看詳細錯誤信息
   - 根據錯誤信息調整配置

3. **手動重試**：
   - 在Actions頁面點擊 "Re-run jobs"

### 如果Railway控制台無法訪問：

1. **使用Railway CLI**：
   ```bash
   # 安裝Railway CLI
   curl -fsSL https://railway.app/install.sh | sh
   
   # 登入並部署
   railway login
   railway up
   ```

## 📈 最佳實踐

1. **定期檢查部署狀態**：每次重要更新後確認部署成功
2. **使用多種部署方法**：結合自動部署和手動觸發
3. **監控部署日誌**：及時發現和解決問題
4. **備份重要配置**：確保可以快速恢復服務

## 🎯 總結

通過以上解決方案，您可以：
- ✅ 立即解決當前的部署問題
- ✅ 建立可靠的自動部署流程
- ✅ 預防未來的部署問題
- ✅ 快速診斷和解決故障

如果問題持續存在，建議聯繫Railway支援團隊或在Railway Discord社群尋求幫助。 