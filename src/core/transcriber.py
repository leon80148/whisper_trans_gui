"""
Whisper 轉錄引擎模組
負責音訊檔案的轉錄功能
"""
import whisper
import warnings
import torch
from typing import Dict, Any, Optional, Callable
import os


class WhisperTranscriber:
    """Whisper 轉錄器類別"""
    
    def __init__(self, model_size: str = "large-v3-turbo", device: Optional[str] = None):
        """
        初始化轉錄器
        
        Args:
            model_size: Whisper 模型大小 (tiny, base, small, medium, large, large-v3-turbo)
            device: 指定設備 (cuda/cpu)，None 為自動偵測
        """
        # 過濾不必要的警告
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead", category=UserWarning)
        
        self.model_size = model_size
        self.device_str = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """載入 Whisper 模型"""
        print(f"Loading Whisper model ({self.model_size})...")
        
        # 顯示 PyTorch 與 CUDA 狀態
        print(f"PyTorch 版本: {torch.__version__}")
        print(f"CUDA 可用: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"可用 GPU 數量: {torch.cuda.device_count()}")
            for idx in range(torch.cuda.device_count()):
                print(f"GPU {idx}: {torch.cuda.get_device_name(idx)}")
        
        compute_type = "float16" if self.device_str == "cuda" else "float32"
        print(f"使用裝置：{self.device_str}, 計算類型：{compute_type}")
        
        self.model = whisper.load_model(self.model_size, device=self.device_str)
        print("Model loaded successfully.")
    
    def transcribe(self, 
                  audio_path: str, 
                  language: str = "zh",
                  progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        轉錄音訊檔案
        
        Args:
            audio_path: 音訊檔案路徑
            language: 語言代碼 (默認為中文 "zh")
            progress_callback: 進度回調函數
            
        Returns:
            轉錄結果字典
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音訊檔案不存在: {audio_path}")
        
        if self.model is None:
            raise RuntimeError("模型未正確載入")
        
        print(f"Transcribing audio: {audio_path}")
        print("這可能需要一些時間，請稍候...")
        
        use_fp16 = True if self.device_str == "cuda" else False
        print(f"FP16 enabled: {use_fp16}, verbose mode will show progress")
        print(f"Language specified: {language}")
        
        # 執行轉錄
        result = self.model.transcribe(
            audio_path, 
            fp16=use_fp16, 
            verbose=True, 
            language=language
        )
        
        print("Transcription completed.")
        return result
    
    def get_device_info(self) -> Dict[str, Any]:
        """獲取設備資訊"""
        return {
            "device": self.device_str,
            "cuda_available": torch.cuda.is_available(),
            "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
            "pytorch_version": torch.__version__
        }