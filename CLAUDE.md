# CLAUDE.md

此文件為 Claude Code (claude.ai/code) 在此儲存庫中工作時提供指導。

## 專案概述
Whisper 個人字幕生成器 - 一個桌面應用程式，使用 OpenAI Whisper 模型將音檔轉換為繁體中文字幕。支援拖拽檔案、批量處理、即時進度顯示、自動清理等功能。

## 環境設置
- **虛擬環境**: 使用 `.venv/` (注意是點開頭的隱藏資料夾)
- **啟動命令**: 
  - Linux/macOS: `source .venv/bin/activate`
  - Windows: `.venv\Scripts\activate`
- **Python版本**: 3.8+ (建議 3.10+)

## 技術棧
### 核心依賴
- **Python**: 主要開發語言
- **OpenAI Whisper**: 語音轉錄模型
- **OpenCC**: 簡繁中文轉換
- **Tkinter**: 內建GUI框架
- **tkinterdnd2**: 拖拽功能支援
- **FFmpeg**: 音訊處理依賴

### 開發工具
- **pytest**: 單元測試框架
- **PyInstaller**: 打包成獨立執行檔

## 專案架構
```
whisper-trans-gui/
├── .venv/                           # Python虛擬環境
├── src/                             # 主要程式碼
│   ├── core/                        # 核心轉錄邏輯
│   │   ├── __init__.py
│   │   ├── transcriber.py           # Whisper轉錄引擎
│   │   └── converter.py             # 簡繁轉換與字幕格式化
│   ├── gui/                         # 圖形介面
│   │   ├── __init__.py
│   │   ├── main_window.py           # 主視窗
│   │   └── components/              # UI元件
│   │       ├── __init__.py
│   │       ├── drag_drop_frame.py   # 拖拽檔案區域
│   │       ├── progress_frame.py    # 進度顯示組件
│   │       └── settings_frame.py    # 設定面板
│   └── utils/                       # 工具函數
│       ├── __init__.py
│       ├── file_utils.py            # 檔案驗證與管理
│       └── error_handler.py         # 錯誤處理與系統檢查
├── tests/                           # 測試檔案
├── requirements.txt                 # Python依賴
├── main.py                         # 應用程式入口點
├── voice_tran.py                   # 原始CLI版本
├── test_progress_fixes.py          # 進度條修復測試
├── test_progress_only.py           # 獨立進度組件測試
├── .gitignore                      # Git忽略規則
├── CLAUDE.md                       # Claude開發指導 (本文件)
└── README.md                       # 專案說明文件
```

## 常用命令
### 開發環境
```bash
# 安裝依賴
pip install -r requirements.txt

# 安裝FFmpeg (macOS)
brew install ffmpeg

# 安裝拖拽功能 (可選)
pip install tkinterdnd2

# 執行GUI應用程式
python main.py --gui

# 執行CLI版本
python main.py audio.wav
```

### 測試
```bash
# 運行進度條修復測試
python test_progress_only.py

# 運行完整測試套件 (需要whisper模組)
python test_progress_fixes.py
```

## 核心功能
### 已實現功能
1. **拖拽介面**: 支援拖拽音檔到視窗 (有fallback機制)
2. **批量處理**: 同時處理多個檔案
3. **即時進度**: 顯示處理進度與狀態
4. **模型選擇**: tiny/base/small/medium/large/large-v3-turbo
5. **輸出格式**: SRT/VTT/TXT 格式選擇
6. **簡繁轉換**: 自動轉換為繁體中文
7. **錯誤處理**: 友善的錯誤訊息與系統檢查
8. **自動清理**: 處理完成後可自動清理檔案清單

### 技術特色
1. **模組化架構**: 清晰的程式碼組織
2. **執行緒安全**: GUI與轉錄邏輯分離
3. **記憶體優化**: 避免重複載入模型
4. **錯誤恢復**: 單檔失敗不影響批次處理
5. **跨平台**: Windows/macOS/Linux 支援

## 系統需求檢查
應用程式會自動檢查：
- Python環境是否正確
- FFmpeg是否已安裝
- Whisper模組是否可用
- tkinterdnd2拖拽功能是否可用

## 最近修復
### 進度條問題修復 (2024)
**問題**: 
1. 進度條無法正常作業
2. 任務完成後清單還會留在list上面

**解決方案**:
1. **進度條邏輯修復**: 改為基於已完成檔案數量更新，而非當前處理檔案索引
2. **自動清理功能**: 新增5秒倒數自動清理機制，可在設定中開關
3. **用戶控制**: 提供"取消自動清理"按鈕給用戶選擇

## 開發指導
### 程式碼風格
- 使用中文註解和文件字串
- 函數命名使用英文，但要清晰易懂
- UI文字全部使用繁體中文
- 錯誤訊息要友善且具體

### 測試策略
- 核心邏輯需要單元測試
- GUI組件需要獨立測試
- 整合測試確保所有功能正常

### Git 工作流程
- 每個新功能創建feature branch
- 修復bug創建fix branch
- 重要變更需要測試驗證
- commit訊息使用中英文混合

## 部署注意事項
### 依賴管理
- 確保所有依賴都在requirements.txt中
- FFmpeg需要額外安裝說明
- tkinterdnd2為可選依賴

### 打包分發
```bash
# 使用PyInstaller打包
pyinstaller --onefile --windowed main.py

# macOS特殊處理
pyinstaller --onefile --windowed --add-data "src:src" main.py
```

## 效能考量
### 記憶體優化
- Whisper模型只載入一次
- 大音檔分段處理避免記憶體不足
- 及時清理暫存檔案

### 用戶體驗
- 長時間處理顯示預估時間
- 支援停止/取消操作
- 自動開啟輸出資料夾

## 故障排除
### 常見問題
1. **FFmpeg錯誤**: 確認已正確安裝FFmpeg
2. **拖拽不可用**: 檢查tkinterdnd2安裝
3. **模型載入失敗**: 檢查網路連線與磁碟空間
4. **權限錯誤**: 確認輸出目錄寫入權限

### 除錯技巧
- 查看終端輸出的詳細錯誤訊息
- 使用verbose模式獲得更多資訊
- 檢查系統需求是否滿足

## 未來擴展
1. **批次處理增強**: 支援資料夾拖拽
2. **字幕編輯**: 內建簡單編輯功能
3. **多語言**: 擴展支援更多語言
4. **佈景主題**: 支援深色/淺色模式
5. **雲端同步**: 可選的設定雲端備份

## 個人使用優勢
- **完全離線**: 無需網路連線
- **無使用限制**: 處理檔案數量不限
- **隱私安全**: 檔案不上傳任何伺服器
- **資源專用**: GPU/CPU資源完全屬於用戶
- **一次安裝**: 無訂閱費用或使用限制