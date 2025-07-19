"""
文字轉換模組
負責簡繁中文轉換和字幕格式化
"""
import opencc
from typing import List, Dict, Any


class TextConverter:
    """文字轉換器類別"""
    
    def __init__(self):
        """初始化轉換器"""
        # 建立簡體轉繁體轉換器
        self.converter = opencc.OpenCC('s2t')
    
    def convert_to_traditional(self, text: str) -> str:
        """
        將簡體中文轉換為繁體中文
        
        Args:
            text: 待轉換的文字
            
        Returns:
            轉換後的繁體中文
        """
        return self.converter.convert(text.strip())


class SubtitleFormatter:
    """字幕格式化器類別"""
    
    @staticmethod
    def format_time(seconds: float) -> str:
        """
        將秒數格式化為 SRT 時間格式 (HH:MM:SS,mmm)
        
        Args:
            seconds: 秒數
            
        Returns:
            格式化的時間字串
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace(".", ",")
    
    @staticmethod
    def create_srt_content(segments: List[Dict[str, Any]], 
                          text_converter: TextConverter = None) -> str:
        """
        創建 SRT 字幕內容
        
        Args:
            segments: Whisper 轉錄片段列表
            text_converter: 文字轉換器（可選）
            
        Returns:
            SRT 格式的字幕內容
        """
        srt_content = []
        
        for i, segment in enumerate(segments, start=1):
            start = SubtitleFormatter.format_time(segment["start"])
            end = SubtitleFormatter.format_time(segment["end"])
            
            # 處理文字內容
            text = segment["text"].strip()
            if text_converter:
                text = text_converter.convert_to_traditional(text)
            
            # 組合 SRT 格式
            srt_content.append(f"{i}")
            srt_content.append(f"{start} --> {end}")
            srt_content.append(text)
            srt_content.append("")  # 空行分隔
        
        return "\n".join(srt_content)
    
    @staticmethod
    def save_subtitle(content: str, output_path: str, encoding: str = "utf-8"):
        """
        儲存字幕檔案
        
        Args:
            content: 字幕內容
            output_path: 輸出檔案路徑
            encoding: 檔案編碼
        """
        with open(output_path, "w", encoding=encoding) as f:
            f.write(content)
        print(f"字幕檔案已儲存: {output_path}")