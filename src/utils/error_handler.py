"""
錯誤處理工具模組
"""
import os
import subprocess
import sys
from typing import Tuple, Optional


class ErrorHandler:
    """錯誤處理器類別"""
    
    @staticmethod
    def check_ffmpeg() -> Tuple[bool, str]:
        """
        檢查 FFmpeg 是否可用
        
        Returns:
            (是否可用, 狀態訊息)
        """
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'], 
                capture_output=True, 
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return True, "FFmpeg 已安裝"
            else:
                return False, "FFmpeg 執行失敗"
        except FileNotFoundError:
            return False, "FFmpeg 未安裝"
        except subprocess.TimeoutExpired:
            return False, "FFmpeg 回應逾時"
        except Exception as e:
            return False, f"FFmpeg 檢查失敗: {str(e)}"
    
    @staticmethod
    def get_ffmpeg_install_guide() -> str:
        """獲取 FFmpeg 安裝指南"""
        system = sys.platform.lower()
        
        if system.startswith('darwin'):  # macOS
            return """FFmpeg 未安裝，請執行以下命令安裝：

macOS:
1. 使用 Homebrew (推薦):
   brew install ffmpeg

2. 使用 MacPorts:
   sudo port install ffmpeg

3. 手動下載:
   訪問 https://ffmpeg.org/download.html"""
        
        elif system.startswith('win'):  # Windows
            return """FFmpeg 未安裝，請執行以下命令安裝：

Windows:
1. 使用 Chocolatey:
   choco install ffmpeg

2. 使用 Scoop:
   scoop install ffmpeg

3. 手動下載:
   訪問 https://ffmpeg.org/download.html
   將 ffmpeg.exe 加入系統 PATH"""
        
        else:  # Linux
            return """FFmpeg 未安裝，請執行以下命令安裝：

Linux:
1. Ubuntu/Debian:
   sudo apt update && sudo apt install ffmpeg

2. CentOS/RHEL:
   sudo yum install ffmpeg

3. Fedora:
   sudo dnf install ffmpeg"""
    
    @staticmethod
    def check_system_requirements() -> Tuple[bool, list]:
        """
        檢查系統需求
        
        Returns:
            (是否滿足需求, 問題列表)
        """
        issues = []
        
        # 檢查 Python 版本
        if sys.version_info < (3, 8):
            issues.append(f"Python 版本過舊: {sys.version}，需要 3.8+")
        
        # 檢查 FFmpeg
        ffmpeg_ok, ffmpeg_msg = ErrorHandler.check_ffmpeg()
        if not ffmpeg_ok:
            issues.append(ffmpeg_msg)
        
        # 檢查可用記憶體 (簡單估計)
        try:
            import psutil
            memory_gb = psutil.virtual_memory().total / (1024**3)
            if memory_gb < 4:
                issues.append(f"記憶體可能不足: {memory_gb:.1f}GB，建議 8GB+")
        except ImportError:
            # psutil 未安裝，跳過記憶體檢查
            pass
        
        return len(issues) == 0, issues
    
    @staticmethod
    def format_whisper_error(error: Exception) -> str:
        """
        格式化 Whisper 相關錯誤訊息
        
        Args:
            error: 異常物件
            
        Returns:
            友善的錯誤訊息
        """
        error_str = str(error).lower()
        
        if 'ffmpeg' in error_str:
            return f"""音訊處理失敗: {str(error)}

這通常是因為 FFmpeg 未正確安裝。
{ErrorHandler.get_ffmpeg_install_guide()}

安裝完成後請重新啟動應用程式。"""
        
        elif 'cuda' in error_str and 'out of memory' in error_str:
            return f"""GPU 記憶體不足: {str(error)}

建議解決方案:
1. 選擇較小的模型 (tiny, base, small)
2. 應用程式會自動切換到 CPU 模式
3. 關閉其他佔用 GPU 的程式"""
        
        elif 'model' in error_str and 'download' in error_str:
            return f"""模型下載失敗: {str(error)}

可能原因:
1. 網路連線問題
2. 磁碟空間不足
3. 防火牆阻擋

建議檢查網路連線並重試。"""
        
        elif 'permission' in error_str or 'access' in error_str:
            return f"""檔案存取失敗: {str(error)}

可能原因:
1. 檔案被其他程式使用
2. 沒有寫入權限
3. 磁碟空間不足

請檢查檔案權限和可用空間。"""
        
        else:
            return f"""處理失敗: {str(error)}

請檢查:
1. 檔案格式是否支援
2. 檔案是否損壞
3. 系統資源是否充足

如果問題持續，請嘗試使用較小的模型。"""
    
    @staticmethod
    def validate_audio_file(file_path: str) -> Tuple[bool, str]:
        """
        驗證音訊檔案
        
        Args:
            file_path: 音訊檔案路徑
            
        Returns:
            (是否有效, 錯誤訊息)
        """
        # 檢查檔案是否存在
        if not os.path.exists(file_path):
            return False, f"檔案不存在: {file_path}"
        
        # 檢查檔案大小
        try:
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return False, "檔案大小為 0"
            
            # 檢查檔案大小限制 (100MB)
            max_size = 100 * 1024 * 1024
            if file_size > max_size:
                size_mb = file_size / 1024 / 1024
                return False, f"檔案過大: {size_mb:.1f}MB (最大 100MB)"
        
        except OSError as e:
            return False, f"檔案讀取失敗: {str(e)}"
        
        # 檢查檔案格式
        from . import FileUtils
        if not FileUtils.is_audio_file(file_path):
            return False, f"不支援的檔案格式: {os.path.splitext(file_path)[1]}"
        
        return True, "檔案有效"