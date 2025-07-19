"""
檔案處理工具模組
"""
import os
from typing import List, Tuple
from pathlib import Path


class FileUtils:
    """檔案處理工具類別"""
    
    # 支援的音訊檔案格式
    SUPPORTED_AUDIO_FORMATS = {'.wav', '.mp3', '.m4a', '.flac', '.aac', '.ogg', '.wma'}
    
    @staticmethod
    def is_audio_file(file_path: str) -> bool:
        """
        檢查檔案是否為支援的音訊格式
        
        Args:
            file_path: 檔案路徑
            
        Returns:
            是否為支援的音訊檔案
        """
        return Path(file_path).suffix.lower() in FileUtils.SUPPORTED_AUDIO_FORMATS
    
    @staticmethod
    def get_output_path(input_path: str, output_format: str = "srt") -> str:
        """
        根據輸入檔案路徑生成輸出檔案路徑
        
        Args:
            input_path: 輸入檔案路徑
            output_format: 輸出格式 (srt, vtt, txt)
            
        Returns:
            輸出檔案路徑
        """
        base_path = os.path.splitext(input_path)[0]
        return f"{base_path}.{output_format}"
    
    @staticmethod
    def validate_input_file(file_path: str) -> Tuple[bool, str]:
        """
        驗證輸入檔案
        
        Args:
            file_path: 檔案路徑
            
        Returns:
            (是否有效, 錯誤訊息)
        """
        if not os.path.exists(file_path):
            return False, f"檔案不存在: {file_path}"
        
        if not FileUtils.is_audio_file(file_path):
            return False, f"不支援的檔案格式: {Path(file_path).suffix}"
        
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return False, "檔案大小為 0"
        
        # 檢查檔案大小限制 (100MB)
        max_size = 100 * 1024 * 1024  # 100MB
        if file_size > max_size:
            return False, f"檔案過大: {file_size / 1024 / 1024:.1f}MB (最大 100MB)"
        
        return True, ""
    
    @staticmethod
    def get_audio_files_from_directory(directory: str) -> List[str]:
        """
        從目錄中獲取所有音訊檔案
        
        Args:
            directory: 目錄路徑
            
        Returns:
            音訊檔案路徑列表
        """
        audio_files = []
        
        if not os.path.isdir(directory):
            return audio_files
        
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path) and FileUtils.is_audio_file(file_path):
                audio_files.append(file_path)
        
        return sorted(audio_files)
    
    @staticmethod
    def ensure_directory_exists(file_path: str):
        """
        確保檔案所在目錄存在
        
        Args:
            file_path: 檔案路徑
        """
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)