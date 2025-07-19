# Whisper 語音轉字幕桌面應用程式

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenAI Whisper](https://img.shields.io/badge/OpenAI-Whisper-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

一個基於 OpenAI Whisper 的桌面應用程式，支援拖拽檔案、批量處理、即時進度顯示，並自動轉換為繁體中文字幕。

[功能特色](#功能特色) •
[安裝說明](#安裝說明) •
[使用方法](#使用方法) •
[系統需求](#系統需求) •
[故障排除](#故障排除)

</div>

## 🎯 功能特色

### 核心功能
- **🎛️ 圖形化介面**: 直觀易用的桌面應用程式
- **📂 拖拽支援**: 直接拖拽音檔到視窗即可處理
- **📊 批量處理**: 同時處理多個音訊檔案
- **📈 即時進度**: 顯示處理進度與詳細狀態
- **🔄 自動清理**: 處理完成後可自動清理檔案清單

### 轉錄功能
- **🤖 多模型選擇**: tiny, base, small, medium, large, large-v3-turbo
- **🌐 語言支援**: 中文、英文、日文、韓文及自動偵測
- **📝 多格式輸出**: SRT、VTT、TXT 格式
- **🔤 簡繁轉換**: 自動轉換為繁體中文
- **⚡ 智慧預設**: 推薦最佳平衡的 large-v3-turbo 模型

### 技術特色
- **💾 完全離線**: 無需網路連線，保護隱私
- **🧩 模組化設計**: 清晰的程式碼架構
- **🔧 錯誤處理**: 友善的錯誤訊息與系統檢查
- **🔒 執行緒安全**: GUI 與轉錄邏輯分離
- **📱 跨平台**: Windows、macOS、Linux 支援

## 📥 安裝說明

### 系統需求
- Python 3.8+ (建議 3.10+)
- FFmpeg (音訊處理)
- 足夠的磁碟空間存放 Whisper 模型

### 快速安裝

1. **下載專案**
   ```bash
   git clone https://github.com/leon80148/whisper_trans_gui.git
   cd whisper_trans_gui
   ```

2. **建立虛擬環境**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

4. **安裝 FFmpeg**
   
   **macOS (使用 Homebrew):**
   ```bash
   brew install ffmpeg
   ```
   
   **Windows:**
   - 下載 [FFmpeg](https://ffmpeg.org/download.html)
   - 解壓縮並將 `bin` 目錄加入 PATH
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

5. **安裝拖拽功能 (可選)**
   ```bash
   pip install tkinterdnd2
   ```

## 🚀 使用方法

### GUI 模式 (推薦)
```bash
python main.py --gui
```

### 命令列模式
```bash
# 處理單個檔案
python main.py audio.wav

# 指定輸出格式
python main.py audio.wav --format srt

# 指定模型
python main.py audio.wav --model large-v3-turbo
```

### 使用步驟

1. **啟動應用程式**
   ```bash
   python main.py --gui
   ```

2. **選擇檔案**
   - 方法一: 直接拖拽音檔到視窗
   - 方法二: 點擊選擇檔案按鈕

3. **調整設定** (可選)
   - 點擊「設定」標籤頁
   - 選擇 Whisper 模型大小
   - 設定語言和輸出格式
   - 配置簡繁轉換選項

4. **開始轉錄**
   - 點擊「開始轉錄」按鈕
   - 觀察進度條和狀態訊息
   - 等待處理完成

5. **檢視結果**
   - 字幕檔案會儲存在原音檔旁邊
   - 點擊「開啟輸出資料夾」查看結果

## 📁 支援格式

### 輸入格式
- **音訊**: MP3, WAV, M4A, FLAC, AAC, OGG, WMA
- **批量**: 支援同時處理多個檔案

### 輸出格式
- **SRT**: 最常用的字幕格式
- **VTT**: WebVTT 網頁字幕格式
- **TXT**: 純文字檔案

## ⚙️ 設定選項

### Whisper 模型
| 模型 | 大小 | 速度 | 準確度 | 建議用途 |
|------|------|------|--------|----------|
| tiny | ~39 MB | 最快 | 較低 | 快速預覽 |
| base | ~74 MB | 快 | 一般 | 日常使用 |
| small | ~244 MB | 中等 | 良好 | 平衡選擇 |
| medium | ~769 MB | 慢 | 很好 | 高品質需求 |
| large | ~1550 MB | 最慢 | 最高 | 專業用途 |
| large-v3-turbo | ~1550 MB | 較快 | 最高 | **推薦選擇** |

### 進階選項
- **自動轉換繁體中文**: 將簡體中文轉換為繁體
- **顯示詳細過程**: 在終端顯示詳細處理資訊
- **自動清理檔案清單**: 處理完成後自動清理 (5秒倒數)

## 🛠️ 故障排除

### 常見問題

**Q: 出現 "No such file or directory: 'ffmpeg'" 錯誤**
A: 需要安裝 FFmpeg，請參考[安裝說明](#安裝說明)中的 FFmpeg 安裝步驟。

**Q: 拖拽功能無法使用**
A: 請安裝 tkinterdnd2：`pip install tkinterdnd2`。如果仍無法使用，應用程式會自動降級到點擊選擇模式。

**Q: 模型下載很慢或失敗**
A: 首次使用時 Whisper 會下載模型檔案，請確保網路連線穩定。模型會快取在本地，後續使用無需重新下載。

**Q: 處理大檔案時記憶體不足**
A: 建議使用較小的模型（如 base 或 small），或確保系統有足夠的可用記憶體。

**Q: 進度條不更新**
A: 這是已知問題並已修復，請確保使用最新版本。

### 系統檢查
應用程式啟動時會自動檢查：
- Python 環境
- FFmpeg 安裝狀況
- Whisper 模組可用性
- 拖拽功能支援

### 除錯模式
如需更詳細的錯誤資訊，請在終端執行並查看輸出：
```bash
python main.py --gui --verbose
```

## 🏗️ 專案結構

```
whisper-trans-gui/
├── src/                      # 主要程式碼
│   ├── core/                 # 核心轉錄邏輯
│   ├── gui/                  # 圖形介面
│   └── utils/                # 工具函數
├── main.py                   # 應用程式入口
├── requirements.txt          # 依賴清單
├── CLAUDE.md                 # 開發指導
└── README.md                 # 專案說明
```

## 🧪 測試

```bash
# 運行元件測試
python test_progress_only.py

# 運行完整測試 (需要 whisper 模組)
python test_progress_fixes.py
```

## 📄 授權條款

本專案使用 MIT 授權條款。詳見 [LICENSE](LICENSE) 檔案。

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

### 開發環境設置
1. Fork 本專案
2. 創建功能分支: `git checkout -b feature/your-feature`
3. 提交變更: `git commit -am 'Add some feature'`
4. 推送分支: `git push origin feature/your-feature`
5. 提交 Pull Request

## 📞 支援

如果您遇到問題或有建議，請：
1. 查看[故障排除](#故障排除)章節
2. 搜尋現有的 [Issues](https://github.com/leon80148/whisper_trans_gui/issues)
3. 建立新的 Issue 並詳細描述問題

## 🎉 致謝

- [OpenAI Whisper](https://github.com/openai/whisper) - 強大的語音轉錄模型
- [OpenCC](https://github.com/BYVoid/OpenCC) - 開源中文轉換工具
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) - Tkinter 拖拽功能支援

---

<div align="center">

**享受高品質的語音轉字幕體驗！** 🎵➡️📝

Made with ❤️ by leon80148

</div>