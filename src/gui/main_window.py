"""
主視窗模組
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import sys
from typing import List

# 添加父目錄到路徑以便導入其他模組
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import WhisperTranscriber, TextConverter, SubtitleFormatter
from utils import FileUtils, ErrorHandler
from gui.components.drag_drop_frame import DragDropFrame
from gui.components.progress_frame import ProgressFrame
from gui.components.settings_frame import SettingsFrame


class WhisperGUI:
    """Whisper 字幕生成器主視窗"""
    
    def __init__(self):
        self.transcriber = None
        self.text_converter = TextConverter()
        self.is_processing = False
        self.current_files = []
        
        self.setup_window()
        self.setup_ui()
        
    def setup_window(self):
        """設置主視窗"""
        # 初始化 tkinterdnd2 (如果可用)
        try:
            import tkinterdnd2 as tkdnd
            self.root = tkdnd.Tk()
            print("✅ 使用支援拖拽的視窗")
            self.drag_drop_enabled = True
        except (ImportError, RuntimeError) as e:
            self.root = tk.Tk()
            print(f"⚠️ 拖拽功能不可用: {e}")
            print("⚠️ 使用標準視窗 (僅支援點擊選擇)")
            self.drag_drop_enabled = False
        
        self.root.title("Whisper 字幕生成器")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        # 設置圖示 (如果有的話)
        try:
            self.root.iconbitmap("assets/icon.ico")
        except:
            pass  # 圖示檔案不存在時忽略
        
        # 設置關閉事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """設置使用者介面"""
        # 創建筆記本 (標籤頁)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 主要頁面
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="檔案處理")
        
        # 設定頁面
        self.settings_page = SettingsFrame(self.notebook)
        self.notebook.add(self.settings_page, text="設定")
        
        # 設置主要頁面內容
        self.setup_main_page()
        
        # 設置自動清理回調
        self.progress_frame.set_auto_clear_callback(self.auto_clear_files)
        
        # 狀態列
        self.status_bar = tk.Label(
            self.root,
            text="準備就緒",
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_main_page(self):
        """設置主要頁面"""
        # 拖拽檔案區域
        self.drag_drop_frame = DragDropFrame(
            self.main_frame, 
            self.on_files_selected
        )
        self.drag_drop_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # 進度顯示區域
        self.progress_frame = ProgressFrame(self.main_frame)
        self.progress_frame.pack(fill="x", pady=(0, 10))
        
        # 控制按鈕
        buttons_frame = tk.Frame(self.main_frame)
        buttons_frame.pack(fill="x", pady=(0, 10))
        
        # 開始處理按鈕
        self.start_btn = ttk.Button(
            buttons_frame,
            text="開始轉錄",
            command=self.start_processing,
            style="Accent.TButton"
        )
        self.start_btn.pack(side="left", padx=(0, 10))
        
        # 停止按鈕
        self.stop_btn = ttk.Button(
            buttons_frame,
            text="停止處理",
            command=self.stop_processing,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=(0, 10))
        
        # 清除按鈕
        self.clear_btn = ttk.Button(
            buttons_frame,
            text="清除所有",
            command=self.clear_all
        )
        self.clear_btn.pack(side="left")
        
        # 說明文字
        help_text = """
使用說明：
1. 拖拽音訊檔案到上方區域，或點擊選擇檔案
2. 在「設定」標籤頁調整轉錄參數
3. 點擊「開始轉錄」進行處理
4. 等待處理完成，字幕檔案將儲存在原檔案旁邊

支援格式：MP3, WAV, M4A, FLAC, AAC, OGG, WMA
        """.strip()
        
        help_label = tk.Label(
            self.main_frame,
            text=help_text,
            font=("Arial", 9),
            fg="#666666",
            justify="left"
        )
        help_label.pack(anchor="w", pady=(10, 0))
        
        # 初始狀態
        self.update_ui_state()
    
    def on_files_selected(self, files: List[str]):
        """檔案選擇事件"""
        self.current_files = files
        self.update_ui_state()
        
        if files:
            self.status_bar.config(text=f"已選擇 {len(files)} 個檔案")
        else:
            self.status_bar.config(text="準備就緒")
    
    def update_ui_state(self):
        """更新UI狀態"""
        has_files = bool(self.current_files)
        
        # 更新按鈕狀態
        if self.is_processing:
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.clear_btn.config(state="disabled")
            self.drag_drop_frame.set_enabled(False)
        else:
            self.start_btn.config(state="normal" if has_files else "disabled")
            self.stop_btn.config(state="disabled")
            self.clear_btn.config(state="normal" if has_files else "disabled")
            self.drag_drop_frame.set_enabled(True)
    
    def start_processing(self):
        """開始處理"""
        if not self.current_files:
            messagebox.showwarning("警告", "請先選擇要處理的音訊檔案")
            return
        
        # 檢查系統需求
        requirements_ok, issues = ErrorHandler.check_system_requirements()
        if not requirements_ok:
            error_msg = "系統檢查發現問題：\\n\\n" + "\\n".join(f"• {issue}" for issue in issues)
            error_msg += "\\n\\n是否仍要繼續？"
            
            if not messagebox.askyesno("系統檢查", error_msg):
                return
        
        # 獲取設定
        settings = self.settings_page.get_settings()
        
        # 確認開始處理
        file_count = len(self.current_files)
        confirm_msg = f"準備處理 {file_count} 個檔案\\n\\n"
        confirm_msg += f"模型: {settings['model_size']}\\n"
        confirm_msg += f"語言: {settings['language']}\\n"
        confirm_msg += f"格式: {settings['output_format']}\\n\\n"
        
        # 添加預估時間提示
        if settings['model_size'] in ['large', 'large-v3-turbo']:
            confirm_msg += "⏰ 大型模型處理時間較長，請耐心等待\\n\\n"
        
        confirm_msg += "確定要開始嗎？"
        
        if not messagebox.askyesno("確認處理", confirm_msg):
            return
        
        # 設置處理狀態
        self.is_processing = True
        self.update_ui_state()
        
        # 在新執行緒中處理
        self.processing_thread = threading.Thread(
            target=self.process_files_thread,
            args=(self.current_files.copy(), settings),
            daemon=True
        )
        self.processing_thread.start()
    
    def process_files_thread(self, files: List[str], settings: dict):
        """在背景執行緒中處理檔案"""
        try:
            # 初始化進度
            self.root.after(0, lambda: self.progress_frame.start_processing(len(files)))
            self.root.after(0, lambda: self.status_bar.config(text="正在載入模型..."))
            
            # 載入轉錄器
            self.transcriber = WhisperTranscriber(
                model_size=settings["model_size"]
            )
            
            # 處理每個檔案
            for i, file_path in enumerate(files):
                if not self.is_processing:  # 檢查是否被停止
                    break
                
                filename = os.path.basename(file_path)
                
                # 更新UI
                self.root.after(0, lambda f=filename, idx=i: 
                               self.progress_frame.update_current_file(f, idx))
                self.root.after(0, lambda: 
                               self.status_bar.config(text=f"正在處理: {filename}"))
                
                try:
                    # 執行轉錄
                    self.root.after(0, lambda: 
                                   self.progress_frame.update_status("正在轉錄音訊..."))
                    
                    result = self.transcriber.transcribe(
                        file_path, 
                        language=settings["language"]
                    )
                    
                    # 生成字幕
                    self.root.after(0, lambda: 
                                   self.progress_frame.update_status("正在生成字幕..."))
                    
                    # 選擇轉換器
                    converter = self.text_converter if settings["convert_traditional"] else None
                    
                    # 生成字幕內容
                    if settings["output_format"] == "srt":
                        content = SubtitleFormatter.create_srt_content(
                            result["segments"], converter
                        )
                    elif settings["output_format"] == "vtt":
                        # 簡單的 VTT 格式實現
                        content = "WEBVTT\\n\\n" + SubtitleFormatter.create_srt_content(
                            result["segments"], converter
                        ).replace(",", ".")
                    else:  # txt
                        content = "\\n".join([
                            converter.convert_to_traditional(seg["text"]) if converter 
                            else seg["text"] 
                            for seg in result["segments"]
                        ])
                    
                    # 儲存檔案
                    output_path = FileUtils.get_output_path(
                        file_path, 
                        settings["output_format"]
                    )
                    
                    self.root.after(0, lambda: 
                                   self.progress_frame.update_status("正在儲存檔案..."))
                    
                    SubtitleFormatter.save_subtitle(content, output_path)
                    
                    # 標記成功
                    self.root.after(0, lambda path=output_path: 
                                   self.progress_frame.file_completed(True, path))
                    
                except Exception as e:
                    error_msg = ErrorHandler.format_whisper_error(e)
                    print(f"處理檔案 {filename} 時發生錯誤: {error_msg}")
                    
                    # 在 GUI 中顯示錯誤
                    self.root.after(0, lambda msg=error_msg: 
                                   messagebox.showerror(f"檔案處理失敗: {filename}", msg))
                    self.root.after(0, lambda: 
                                   self.progress_frame.file_completed(False))
            
            # 處理完成
            self.root.after(0, self.processing_completed)
            
        except Exception as e:
            error_msg = ErrorHandler.format_whisper_error(e)
            print(f"處理過程中發生嚴重錯誤: {error_msg}")
            self.root.after(0, lambda: self.progress_frame.processing_error(error_msg))
            self.root.after(0, lambda: messagebox.showerror("處理失敗", error_msg))
            self.root.after(0, self.processing_completed)
    
    def processing_completed(self):
        """處理完成"""
        self.is_processing = False
        self.update_ui_state()
        
        # 獲取自動清理設定
        settings = self.settings_page.get_settings()
        auto_clear_enabled = settings.get("auto_clear_after_completion", True)
        
        self.progress_frame.processing_complete(auto_clear_enabled)
        self.status_bar.config(text="處理完成")
    
    def auto_clear_files(self):
        """自動清理檔案（由進度框架回調）"""
        print("執行自動清理...")
        self.current_files.clear()
        self.drag_drop_frame.clear_files()
        self.progress_frame.reset()
        self.status_bar.config(text="已自動清理檔案清單")
        self.update_ui_state()
    
    def stop_processing(self):
        """停止處理"""
        if self.is_processing:
            self.is_processing = False
            self.status_bar.config(text="正在停止...")
            
            # 等待執行緒結束
            if hasattr(self, 'processing_thread') and self.processing_thread.is_alive():
                self.processing_thread.join(timeout=1.0)
            
            self.update_ui_state()
            self.status_bar.config(text="已停止處理")
    
    def clear_all(self):
        """清除所有檔案和進度"""
        if self.is_processing:
            if not messagebox.askyesno("確認", "正在處理中，確定要停止並清除嗎？"):
                return
            self.stop_processing()
        
        self.current_files.clear()
        self.drag_drop_frame.clear_files()
        self.progress_frame.reset()
        self.status_bar.config(text="準備就緒")
        self.update_ui_state()
    
    def on_closing(self):
        """視窗關閉事件"""
        if self.is_processing:
            if messagebox.askyesno("確認退出", "正在處理中，確定要退出嗎？"):
                self.stop_processing()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """執行主程式"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()


def launch_gui():
    """啟動GUI應用程式"""
    try:
        # 系統檢查
        print("🔍 檢查系統需求...")
        requirements_ok, issues = ErrorHandler.check_system_requirements()
        
        if issues:
            print("⚠️ 系統檢查發現以下問題:")
            for issue in issues:
                print(f"  • {issue}")
            
            if not requirements_ok:
                print("\\n❌ 系統需求不滿足，但應用程式仍會嘗試啟動")
                print("   某些功能可能無法正常工作")
            else:
                print("\\n✅ 系統檢查完成，可以繼續使用")
        else:
            print("✅ 系統檢查通過")
        
        # 檢查拖拽功能
        try:
            import tkinterdnd2
            print("✅ 拖拽功能可用")
        except ImportError:
            print("⚠️ tkinterdnd2 未安裝，拖拽功能將不可用")
            print("   可執行: pip install tkinterdnd2")
        
        # 啟動應用程式
        print("🚀 啟動應用程式...")
        app = WhisperGUI()
        app.run()
        
    except Exception as e:
        error_msg = f"啟動GUI失敗: {e}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        
        # 嘗試顯示錯誤對話框
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("啟動失敗", error_msg)
        except:
            pass


if __name__ == "__main__":
    launch_gui()