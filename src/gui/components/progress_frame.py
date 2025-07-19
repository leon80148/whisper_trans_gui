"""
進度顯示組件
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional


class ProgressFrame(tk.Frame):
    """進度顯示區域"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """設置UI"""
        # 主標題
        self.title_label = tk.Label(
            self,
            text="準備就緒",
            font=("Arial", 12, "bold"),
            fg="#333333"
        )
        self.title_label.pack(pady=(10, 5))
        
        # 當前處理檔案
        self.current_file_label = tk.Label(
            self,
            text="",
            font=("Arial", 10),
            fg="#666666"
        )
        self.current_file_label.pack(pady=(0, 5))
        
        # 進度條
        self.progress_bar = ttk.Progressbar(
            self,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(pady=5, padx=20, fill="x")
        
        # 進度百分比
        self.progress_label = tk.Label(
            self,
            text="0%",
            font=("Arial", 10),
            fg="#666666"
        )
        self.progress_label.pack(pady=(0, 5))
        
        # 狀態訊息
        self.status_label = tk.Label(
            self,
            text="",
            font=("Arial", 9),
            fg="#888888",
            wraplength=400
        )
        self.status_label.pack(pady=(0, 10))
        
        # 結果區域
        self.result_frame = tk.Frame(self)
        
        # 成功/失敗統計
        self.stats_label = tk.Label(
            self.result_frame,
            text="",
            font=("Arial", 10),
            fg="#333333"
        )
        self.stats_label.pack(pady=5)
        
        # 輸出資料夾按鈕
        self.open_folder_btn = ttk.Button(
            self.result_frame,
            text="開啟輸出資料夾",
            command=self.open_output_folder
        )
        
        self.output_folder = None
        
    def start_processing(self, total_files: int):
        """開始處理"""
        self.total_files = total_files
        self.current_file_index = 0
        self.success_count = 0
        self.failure_count = 0
        
        self.title_label.config(text="正在處理中...")
        self.progress_bar.config(maximum=total_files)
        self.progress_bar.config(value=0)
        self.progress_label.config(text="0%")
        self.status_label.config(text="正在初始化...")
        
        # 隱藏結果區域
        self.result_frame.pack_forget()
    
    def update_current_file(self, filename: str, file_index: int):
        """更新當前處理的檔案"""
        self.current_file_index = file_index
        self.current_file_label.config(
            text=f"正在處理: {filename} ({file_index + 1}/{self.total_files})"
        )
        
        # 注意：這裡不更新進度條，進度條應該基於已完成的檔案數量
        # 進度條將在 file_completed() 中更新
    
    def update_status(self, message: str):
        """更新狀態訊息"""
        self.status_label.config(text=message)
        self.update_idletasks()  # 強制更新UI
    
    def file_completed(self, success: bool, output_path: Optional[str] = None):
        """檔案處理完成"""
        if success:
            self.success_count += 1
            if output_path and self.output_folder is None:
                import os
                self.output_folder = os.path.dirname(output_path)
        else:
            self.failure_count += 1
        
        # 更新進度條 - 基於已完成的檔案數量
        completed = self.success_count + self.failure_count
        progress = (completed / self.total_files) * 100
        self.progress_bar.config(value=completed)
        self.progress_label.config(text=f"{progress:.0f}%")
        
        # 更新當前檔案顯示
        if completed < self.total_files:
            # 還有檔案要處理
            remaining = self.total_files - completed
            self.current_file_label.config(
                text=f"已完成 {completed}/{self.total_files} 個檔案，剩餘 {remaining} 個"
            )
        else:
            # 所有檔案處理完成
            self.current_file_label.config(text="所有檔案處理完成")
        
        # 強制更新UI
        self.update_idletasks()
    
    def processing_complete(self, auto_clear_enabled: bool = True):
        """所有處理完成"""
        self.title_label.config(text="處理完成")
        self.current_file_label.config(text="所有檔案處理完成")
        
        # 顯示統計結果
        total = self.success_count + self.failure_count
        stats_text = f"共處理 {total} 個檔案："
        
        if self.success_count > 0:
            stats_text += f" ✅ 成功 {self.success_count} 個"
        
        if self.failure_count > 0:
            stats_text += f" ❌ 失敗 {self.failure_count} 個"
        
        self.stats_label.config(text=stats_text)
        
        # 顯示結果區域
        if self.success_count > 0:
            self.result_frame.pack(fill="x", pady=10)
            if self.output_folder:
                self.open_folder_btn.pack()
        
        self.status_label.config(text="所有檔案處理完成！")
        
        # 如果啟用自動清理，設置倒數計時（不管是否有成功檔案）
        if auto_clear_enabled:
            # 如果結果區域還沒顯示，先顯示它以便放置取消按鈕
            if total > 0:  # 只要有處理過檔案就顯示
                self.result_frame.pack(fill="x", pady=10)
            self.start_auto_clear_countdown()
    
    def start_auto_clear_countdown(self):
        """開始自動清理倒數計時"""
        self.auto_clear_countdown = 5
        self.auto_clear_cancelled = False
        
        # 添加取消按鈕到結果區域
        self.cancel_auto_clear_btn = ttk.Button(
            self.result_frame,
            text="取消自動清理",
            command=self.cancel_auto_clear
        )
        self.cancel_auto_clear_btn.pack(side="left", padx=(10, 0))
        
        # 開始倒數
        self.update_countdown()
    
    def update_countdown(self):
        """更新倒數計時"""
        if self.auto_clear_cancelled:
            return
        
        if self.auto_clear_countdown > 0:
            self.status_label.config(
                text=f"所有檔案處理完成！將在 {self.auto_clear_countdown} 秒後自動清理檔案清單..."
            )
            self.auto_clear_countdown -= 1
            # 1秒後再次更新
            self.after(1000, self.update_countdown)
        else:
            # 倒數結束，執行自動清理
            if hasattr(self, 'auto_clear_callback') and self.auto_clear_callback:
                self.auto_clear_callback()
    
    def cancel_auto_clear(self):
        """取消自動清理"""
        self.auto_clear_cancelled = True
        self.status_label.config(text="所有檔案處理完成！")
        
        # 移除取消按鈕
        if hasattr(self, 'cancel_auto_clear_btn'):
            self.cancel_auto_clear_btn.destroy()
    
    def set_auto_clear_callback(self, callback):
        """設置自動清理回調函數"""
        self.auto_clear_callback = callback
    
    def processing_error(self, error_message: str):
        """處理過程中發生錯誤"""
        self.title_label.config(text="處理失敗")
        self.status_label.config(text=f"錯誤: {error_message}", fg="red")
        self.current_file_label.config(text="")
    
    def open_output_folder(self):
        """開啟輸出資料夾"""
        if self.output_folder:
            import os
            import subprocess
            import platform
            
            try:
                if platform.system() == "Windows":
                    os.startfile(self.output_folder)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", self.output_folder])
                else:  # Linux
                    subprocess.run(["xdg-open", self.output_folder])
            except Exception as e:
                print(f"無法開啟資料夾: {e}")
    
    def reset(self):
        """重置進度顯示"""
        # 取消自動清理倒數
        if hasattr(self, 'auto_clear_cancelled'):
            self.auto_clear_cancelled = True
        
        self.title_label.config(text="準備就緒")
        self.current_file_label.config(text="")
        self.progress_bar.config(value=0)
        self.progress_label.config(text="0%")
        self.status_label.config(text="", fg="#888888")
        self.result_frame.pack_forget()
        self.output_folder = None
        
        # 清理自動清理相關屬性
        if hasattr(self, 'cancel_auto_clear_btn'):
            self.cancel_auto_clear_btn.destroy()
            delattr(self, 'cancel_auto_clear_btn')