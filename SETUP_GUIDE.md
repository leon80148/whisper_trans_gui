# 🚀 Whisper 字幕生成器 - 完整安裝指南

## 📋 系統需求

- **Python**: 3.8+ (建議 3.10+)
- **作業系統**: Windows, macOS, Linux
- **記憶體**: 建議 8GB+ (模型載入需要)
- **硬碟空間**: 5GB+ (模型檔案約 3GB)

## 🛠️ 快速安裝

### 1. 安裝 Python 依賴
```bash
# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows

# 安裝依賴套件
pip install -r requirements.txt
```

### 2. 安裝 FFmpeg (必要)

FFmpeg 是音訊處理的核心依賴，Whisper 需要它來處理各種音訊格式。

#### macOS
```bash
# 使用 Homebrew
brew install ffmpeg

# 或使用 MacPorts
sudo port install ffmpeg
```

#### Windows
```bash
# 使用 Chocolatey
choco install ffmpeg

# 或使用 Scoop
scoop install ffmpeg

# 或手動下載：https://ffmpeg.org/download.html
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg

# CentOS/RHEL/Fedora
sudo yum install ffmpeg
# 或
sudo dnf install ffmpeg
```

### 3. 驗證安裝
```bash
# 檢查 FFmpeg
ffmpeg -version

# 檢查 Python 模組
python -c "import whisper; print('Whisper 安裝成功')"
```

## 🎯 使用方式

### GUI 模式 (推薦)
```bash
python main.py --gui
```

### 命令行模式
```bash
# 基本使用
python main.py audio.wav

# 指定輸出檔案
python main.py audio.mp3 -o subtitle.srt

# 選擇模型大小
python main.py audio.wav -m medium

# 指定語言
python main.py audio.wav -l en
```

## 🔧 常見問題解決

### ❌ 錯誤：No such file or directory: 'ffmpeg'

**原因**: FFmpeg 未安裝或未加入 PATH
**解決方案**:
1. 安裝 FFmpeg (見上方安裝指南)
2. 確認 FFmpeg 在 PATH 中：`ffmpeg -version`
3. 重新啟動終端機

### ❌ 錯誤：Unable to load tkdnd library

**原因**: 拖拽功能在某些系統上不支援
**解決方案**: 
- 應用程式會自動降級為點擊選擇模式
- 功能完全不受影響，只是操作方式不同

### ❌ 錯誤：CUDA out of memory

**原因**: GPU 記憶體不足
**解決方案**:
1. 選擇較小的模型 (tiny, base, small)
2. 應用程式會自動使用 CPU 模式

### ❌ 模型下載緩慢

**原因**: 網路連線問題
**解決方案**:
1. 首次使用會下載約 3GB 模型檔案
2. 耐心等待，模型會快取到本地
3. 後續使用不需重新下載

## 📚 模型說明

| 模型大小 | 檔案大小 | 記憶體需求 | 準確度 | 速度 |
|---------|----------|-----------|--------|------|
| tiny    | 39 MB    | ~1 GB     | 較低   | 最快 |
| base    | 74 MB    | ~1 GB     | 一般   | 快   |
| small   | 244 MB   | ~2 GB     | 好     | 中等 |
| medium  | 769 MB   | ~5 GB     | 很好   | 較慢 |
| large   | 1550 MB  | ~10 GB    | 最好   | 慢   |
| large-v3-turbo | 1550 MB | ~10 GB | 最好 | 平衡 |

## 🎵 支援的音訊格式

- **MP3** - 最常見格式
- **WAV** - 無壓縮格式，品質最好
- **M4A** - Apple 格式
- **FLAC** - 無損壓縮，高品質
- **AAC** - 高效編碼
- **OGG** - 開源格式
- **WMA** - Windows Media 格式

## 💡 效能最佳化建議

### 音訊品質
- 使用高品質音訊檔案 (44.1kHz, 16-bit 以上)
- 減少背景噪音
- 確保語音清晰

### 硬體配置
- **GPU**: 支援 CUDA 的 NVIDIA 顯卡可大幅提升速度
- **CPU**: 多核心處理器有助於 CPU 模式
- **記憶體**: 充足的 RAM 可載入更大的模型

### 設定調整
- **短檔案**: 使用 large-v3-turbo 或 medium
- **長檔案**: 使用 small 或 base 節省時間
- **高準確度需求**: 使用 large 模型
- **快速處理**: 使用 tiny 或 base 模型

## 🔄 更新指南

```bash
# 更新 Python 套件
pip install --upgrade -r requirements.txt

# 更新 FFmpeg
brew upgrade ffmpeg  # macOS
choco upgrade ffmpeg # Windows
```

## 📞 支援

如果遇到問題：
1. 檢查上述常見問題
2. 確認所有依賴都正確安裝
3. 查看終端機錯誤訊息
4. 嘗試重新啟動應用程式

祝您使用愉快！ 🎉