#!/usr/bin/env python3
"""
Whisper 字幕生成器 - 主程式
支援命令行和圖形介面模式
"""
import sys
import argparse
from pathlib import Path

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core import WhisperTranscriber, TextConverter, SubtitleFormatter
from utils import FileUtils


def transcribe_audio(input_path: str, 
                    output_path: str = None, 
                    model_size: str = "large-v3-turbo",
                    language: str = "zh") -> bool:
    """
    轉錄單個音訊檔案
    
    Args:
        input_path: 輸入音訊檔案路徑
        output_path: 輸出字幕檔案路徑（可選）
        model_size: Whisper 模型大小
        language: 語言代碼
        
    Returns:
        是否成功
    """
    try:
        # 驗證輸入檔案
        is_valid, error_msg = FileUtils.validate_input_file(input_path)
        if not is_valid:
            print(f"錯誤: {error_msg}")
            return False
        
        # 生成輸出路徑
        if output_path is None:
            output_path = FileUtils.get_output_path(input_path)
        
        # 確保輸出目錄存在
        FileUtils.ensure_directory_exists(output_path)
        
        # 初始化轉錄器和轉換器
        transcriber = WhisperTranscriber(model_size=model_size)
        text_converter = TextConverter()
        
        # 執行轉錄
        print(f"\n開始處理: {input_path}")
        result = transcriber.transcribe(input_path, language=language)
        
        # 生成字幕內容
        print("生成字幕檔案...")
        srt_content = SubtitleFormatter.create_srt_content(
            result["segments"], 
            text_converter
        )
        
        # 儲存字幕檔案
        SubtitleFormatter.save_subtitle(srt_content, output_path)
        
        print(f"✅ 完成！字幕檔案: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        return False


def main():
    """主函數"""
    parser = argparse.ArgumentParser(
        description="Whisper 字幕生成器 - 將音訊檔案轉換為繁體中文字幕"
    )
    
    parser.add_argument(
        "input",
        nargs="?",
        help="輸入音訊檔案路徑"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="輸出字幕檔案路徑"
    )
    
    parser.add_argument(
        "-m", "--model",
        choices=["tiny", "base", "small", "medium", "large", "large-v3-turbo"],
        default="large-v3-turbo",
        help="Whisper 模型大小 (預設: large-v3-turbo)"
    )
    
    parser.add_argument(
        "-l", "--language",
        default="zh",
        help="語言代碼 (預設: zh)"
    )
    
    parser.add_argument(
        "--gui",
        action="store_true",
        help="啟動圖形介面模式"
    )
    
    args = parser.parse_args()
    
    # 如果指定 GUI 模式或沒有提供輸入檔案，啟動圖形介面
    if args.gui or not args.input:
        try:
            from src.gui.main_window import launch_gui
            print("啟動圖形介面...")
            launch_gui()
        except ImportError as e:
            print(f"圖形介面載入失敗: {e}")
            print("請使用命令行模式")
            print("使用方式: python main.py <音訊檔案路徑>")
            return
    else:
        # 命令行模式
        success = transcribe_audio(
            input_path=args.input,
            output_path=args.output,
            model_size=args.model,
            language=args.language
        )
        
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()