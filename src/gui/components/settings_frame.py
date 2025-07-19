"""
設定面板組件
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any


class SettingsFrame(tk.Frame):
    """設定面板"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        self.load_default_settings()
    
    def setup_ui(self):
        """設置UI"""
        # 標題
        title_label = tk.Label(
            self,
            text="轉錄設定",
            font=("Arial", 12, "bold"),
            fg="#333333"
        )
        title_label.pack(pady=(10, 15))
        
        # 設定項目框架
        settings_frame = tk.Frame(self)
        settings_frame.pack(fill="both", expand=True, padx=20)
        
        # 模型選擇
        model_frame = tk.Frame(settings_frame)
        model_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            model_frame,
            text="Whisper 模型:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")
        
        tk.Label(
            model_frame,
            text="較大的模型準確度更高，但速度較慢",
            font=("Arial", 8),
            fg="#666666"
        ).pack(anchor="w", pady=(0, 5))
        
        self.model_var = tk.StringVar(value="large-v3-turbo")
        model_options = [
            ("tiny", "Tiny - 最快速，準確度較低"),
            ("base", "Base - 快速，準確度一般"),
            ("small", "Small - 平衡速度與準確度"),
            ("medium", "Medium - 準確度高，速度較慢"),
            ("large", "Large - 準確度很高，速度慢"),
            ("large-v3-turbo", "Large-v3-Turbo - 最佳平衡 (推薦)")
        ]
        
        for value, text in model_options:
            rb = tk.Radiobutton(
                model_frame,
                text=text,
                variable=self.model_var,
                value=value,
                font=("Arial", 9)
            )
            rb.pack(anchor="w", padx=20)
        
        # 語言設定
        language_frame = tk.Frame(settings_frame)
        language_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            language_frame,
            text="語言設定:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")
        
        lang_select_frame = tk.Frame(language_frame)
        lang_select_frame.pack(fill="x", pady=(5, 0))
        
        tk.Label(
            lang_select_frame,
            text="語言:"
        ).pack(side="left")
        
        self.language_var = tk.StringVar(value="zh")
        language_combo = ttk.Combobox(
            lang_select_frame,
            textvariable=self.language_var,
            values=["zh", "en", "ja", "ko", "auto"],
            state="readonly",
            width=10
        )
        language_combo.pack(side="left", padx=(5, 0))
        
        # 語言說明
        lang_desc = {
            "zh": "中文",
            "en": "英文", 
            "ja": "日文",
            "ko": "韓文",
            "auto": "自動偵測"
        }
        
        self.language_desc_label = tk.Label(
            lang_select_frame,
            text=f"({lang_desc[self.language_var.get()]})",
            font=("Arial", 8),
            fg="#666666"
        )
        self.language_desc_label.pack(side="left", padx=(5, 0))
        
        # 綁定語言變更事件
        language_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # 輸出格式
        output_frame = tk.Frame(settings_frame)
        output_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            output_frame,
            text="輸出格式:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")
        
        format_select_frame = tk.Frame(output_frame)
        format_select_frame.pack(fill="x", pady=(5, 0))
        
        tk.Label(
            format_select_frame,
            text="格式:"
        ).pack(side="left")
        
        self.format_var = tk.StringVar(value="srt")
        format_combo = ttk.Combobox(
            format_select_frame,
            textvariable=self.format_var,
            values=["srt", "vtt", "txt"],
            state="readonly",
            width=10
        )
        format_combo.pack(side="left", padx=(5, 0))
        
        # 格式說明
        format_desc = {
            "srt": "SRT字幕檔 (最常用)",
            "vtt": "WebVTT字幕檔",
            "txt": "純文字檔"
        }
        
        self.format_desc_label = tk.Label(
            format_select_frame,
            text=f"({format_desc[self.format_var.get()]})",
            font=("Arial", 8),
            fg="#666666"
        )
        self.format_desc_label.pack(side="left", padx=(5, 0))
        
        # 綁定格式變更事件
        format_combo.bind('<<ComboboxSelected>>', self.on_format_change)
        
        # 進階選項
        advanced_frame = tk.LabelFrame(
            settings_frame,
            text="進階選項",
            font=("Arial", 9, "bold"),
            fg="#333333"
        )
        advanced_frame.pack(fill="x", pady=(10, 0))
        
        # 簡繁轉換
        self.convert_traditional_var = tk.BooleanVar(value=True)
        convert_cb = tk.Checkbutton(
            advanced_frame,
            text="自動轉換為繁體中文",
            variable=self.convert_traditional_var,
            font=("Arial", 9)
        )
        convert_cb.pack(anchor="w", padx=10, pady=5)
        
        # 詳細輸出
        self.verbose_var = tk.BooleanVar(value=True)
        verbose_cb = tk.Checkbutton(
            advanced_frame,
            text="顯示詳細處理過程",
            variable=self.verbose_var,
            font=("Arial", 9)
        )
        verbose_cb.pack(anchor="w", padx=10, pady=5)
        
        # 自動清理
        self.auto_clear_var = tk.BooleanVar(value=True)
        auto_clear_cb = tk.Checkbutton(
            advanced_frame,
            text="處理完成後自動清理檔案清單 (5秒倒數)",
            variable=self.auto_clear_var,
            font=("Arial", 9)
        )
        auto_clear_cb.pack(anchor="w", padx=10, pady=5)
        
        # 設定按鈕
        buttons_frame = tk.Frame(settings_frame)
        buttons_frame.pack(fill="x", pady=(20, 10))
        
        # 重置按鈕
        reset_btn = ttk.Button(
            buttons_frame,
            text="重置為預設",
            command=self.reset_to_defaults
        )
        reset_btn.pack(side="right", padx=(5, 0))
        
        # 儲存按鈕
        save_btn = ttk.Button(
            buttons_frame,
            text="儲存設定",
            command=self.save_settings
        )
        save_btn.pack(side="right")
    
    def on_language_change(self, event):
        """語言變更事件"""
        lang_desc = {
            "zh": "中文",
            "en": "英文", 
            "ja": "日文",
            "ko": "韓文",
            "auto": "自動偵測"
        }
        selected = self.language_var.get()
        self.language_desc_label.config(text=f"({lang_desc.get(selected, '')})")
    
    def on_format_change(self, event):
        """格式變更事件"""
        format_desc = {
            "srt": "SRT字幕檔 (最常用)",
            "vtt": "WebVTT字幕檔",
            "txt": "純文字檔"
        }
        selected = self.format_var.get()
        self.format_desc_label.config(text=f"({format_desc.get(selected, '')})")
    
    def get_settings(self) -> Dict[str, Any]:
        """獲取當前設定"""
        return {
            "model_size": self.model_var.get(),
            "language": self.language_var.get(),
            "output_format": self.format_var.get(),
            "convert_traditional": self.convert_traditional_var.get(),
            "verbose": self.verbose_var.get(),
            "auto_clear_after_completion": self.auto_clear_var.get()
        }
    
    def set_settings(self, settings: Dict[str, Any]):
        """設置設定值"""
        if "model_size" in settings:
            self.model_var.set(settings["model_size"])
        if "language" in settings:
            self.language_var.set(settings["language"])
            self.on_language_change(None)
        if "output_format" in settings:
            self.format_var.set(settings["output_format"])
            self.on_format_change(None)
        if "convert_traditional" in settings:
            self.convert_traditional_var.set(settings["convert_traditional"])
        if "verbose" in settings:
            self.verbose_var.set(settings["verbose"])
        if "auto_clear_after_completion" in settings:
            self.auto_clear_var.set(settings["auto_clear_after_completion"])
    
    def load_default_settings(self):
        """載入預設設定"""
        defaults = {
            "model_size": "large-v3-turbo",
            "language": "zh",
            "output_format": "srt",
            "convert_traditional": True,
            "verbose": True,
            "auto_clear_after_completion": True
        }
        self.set_settings(defaults)
    
    def reset_to_defaults(self):
        """重置為預設設定"""
        self.load_default_settings()
    
    def save_settings(self):
        """儲存設定 (可擴展為儲存到檔案)"""
        # 這裡可以添加儲存設定到檔案的邏輯
        settings = self.get_settings()
        print("設定已儲存:", settings)  # 暫時用 print，之後可改為檔案儲存