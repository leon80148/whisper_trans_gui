"""
拖拽檔案區域組件
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable, List
import os
from utils import FileUtils

def check_dnd_available():
    """檢查拖拽功能是否可用"""
    try:
        import tkinterdnd2 as tkdnd
        # 嘗試檢查是否能正常載入
        return True
    except (ImportError, RuntimeError):
        return False

DND_AVAILABLE = check_dnd_available()


class DragDropFrame(tk.Frame):
    """拖拽檔案區域"""
    
    def __init__(self, parent, on_files_dropped: Callable[[List[str]], None]):
        super().__init__(parent)
        self.on_files_dropped = on_files_dropped
        self.setup_ui()
        self.setup_drag_drop()
    
    def setup_ui(self):
        """設置UI"""
        # 主框架設置
        self.configure(relief="sunken", borderwidth=2, bg="#f0f0f0")
        
        # 拖拽區域
        self.drop_area = tk.Label(
            self,
            text="拖拽音訊檔案到這裡\n或點擊選擇檔案\n\n支援格式: MP3, WAV, M4A, FLAC",
            font=("Arial", 14),
            bg="#f8f8f8",
            fg="#666666",
            relief="ridge",
            borderwidth=2,
            cursor="hand2"
        )
        self.drop_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 綁定點擊事件
        self.drop_area.bind("<Button-1>", self.select_files)
        
        # 檔案列表框架
        self.files_frame = tk.Frame(self)
        self.files_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # 檔案列表
        self.files_listbox = tk.Listbox(
            self.files_frame,
            height=4,
            selectmode=tk.MULTIPLE
        )
        
        # 滾動條
        scrollbar = ttk.Scrollbar(self.files_frame, orient="vertical")
        scrollbar.config(command=self.files_listbox.yview)
        self.files_listbox.config(yscrollcommand=scrollbar.set)
        
        # 打包列表和滾動條
        self.files_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 按鈕框架
        buttons_frame = tk.Frame(self.files_frame)
        buttons_frame.pack(fill="x", pady=(5, 0))
        
        # 清除按鈕
        clear_btn = ttk.Button(
            buttons_frame,
            text="清除列表",
            command=self.clear_files
        )
        clear_btn.pack(side="right", padx=(5, 0))
        
        # 移除選中按鈕
        remove_btn = ttk.Button(
            buttons_frame,
            text="移除選中",
            command=self.remove_selected
        )
        remove_btn.pack(side="right")
        
        # 初始時隱藏檔案列表
        self.files_frame.pack_forget()
        
        # 儲存檔案列表
        self.file_paths = []
    
    def setup_drag_drop(self):
        """設置拖拽功能"""
        if DND_AVAILABLE:
            try:
                import tkinterdnd2 as tkdnd
                
                # 設置拖拽功能
                self.drop_area.drop_target_register(tkdnd.DND_FILES)
                self.drop_area.dnd_bind('<<Drop>>', self.on_drop)
                self.drop_area.dnd_bind('<<DragEnter>>', self.on_drag_enter)
                self.drop_area.dnd_bind('<<DragLeave>>', self.on_drag_leave)
                
                # 更新文字提示
                self.drop_area.config(
                    text="拖拽音訊檔案到這裡\n或點擊選擇檔案\n\n支援格式: MP3, WAV, M4A, FLAC"
                )
                print("✅ 拖拽功能已啟用")
                return
                
            except Exception as e:
                print(f"⚠️ 拖拽功能設置失敗: {e}")
        
        # 降級到點擊選擇模式
        print("⚠️ 降級到點擊選擇模式")
        self.setup_click_only()
    
    def setup_click_only(self):
        """設置僅點擊選擇模式"""
        self.drop_area.config(
            text="點擊選擇音訊檔案\n\n支援格式: MP3, WAV, M4A, FLAC"
        )
    
    def on_drag_enter(self, event):
        """拖拽進入事件"""
        self.drop_area.config(
            bg="#e8f4fd",
            relief="solid",
            borderwidth=3
        )
        # 更新文字提示
        if not self.file_paths:
            self.drop_area.config(
                text="放開滑鼠以添加檔案\n\n支援格式: MP3, WAV, M4A, FLAC",
                fg="#0066cc"
            )
        else:
            self.drop_area.config(
                text=f"放開滑鼠以添加更多檔案\n目前已有 {len(self.file_paths)} 個檔案",
                fg="#0066cc"
            )
    
    def on_drag_leave(self, event):
        """拖拽離開事件"""
        self.restore_normal_appearance()
    
    def on_drop(self, event):
        """檔案拖拽放下事件"""
        self.restore_normal_appearance()
        
        # 顯示處理中狀態
        self.drop_area.config(
            text="正在處理檔案...",
            fg="#666666"
        )
        self.update_idletasks()
        
        # 解析拖拽的檔案
        files = self.parse_drop_files(event.data)
        self.add_files(files)
    
    def restore_normal_appearance(self):
        """恢復正常外觀"""
        self.drop_area.config(
            bg="#f8f8f8",
            relief="ridge",
            borderwidth=2,
            fg="#666666"
        )
        
        # 恢復正常文字
        if not self.file_paths:
            self.drop_area.config(
                text="拖拽音訊檔案到這裡\n或點擊選擇檔案\n\n支援格式: MP3, WAV, M4A, FLAC"
            )
        else:
            file_count = len(self.file_paths)
            self.drop_area.config(
                text=f"已選擇 {file_count} 個檔案\n點擊或拖拽添加更多檔案"
            )
    
    def parse_drop_files(self, data: str) -> List[str]:
        """解析拖拽的檔案路徑"""
        files = []
        
        try:
            # 處理不同格式的拖拽數據
            print(f"解析拖拽數據: {repr(data)}")  # 除錯用
            
            # 方法1: 處理 tkinterdnd2 的標準格式
            if data.startswith('{') and data.endswith('}'):
                # 移除外層大括號
                data = data[1:-1]
                
                # 處理多個檔案的情況: {file1} {file2}
                import re
                file_matches = re.findall(r'\{([^}]+)\}|([^{}\s]+)', data)
                for match in file_matches:
                    file_path = match[0] or match[1]
                    if file_path and os.path.exists(file_path):
                        files.append(file_path)
            else:
                # 方法2: 簡單分割處理
                potential_files = data.split()
                for file_path in potential_files:
                    # 清理路徑
                    file_path = file_path.strip('{}"\' ')
                    if file_path and os.path.exists(file_path):
                        files.append(file_path)
            
            # 方法3: 如果上面都沒找到，嘗試直接使用原始數據
            if not files and os.path.exists(data.strip()):
                files.append(data.strip())
            
            print(f"解析結果: {files}")  # 除錯用
            
        except Exception as e:
            print(f"解析拖拽檔案時發生錯誤: {e}")
        
        return files
    
    def select_files(self, event=None):
        """點擊選擇檔案"""
        file_types = [
            ("音訊檔案", "*.mp3 *.wav *.m4a *.flac *.aac *.ogg *.wma"),
            ("所有檔案", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="選擇音訊檔案",
            filetypes=file_types
        )
        
        if files:
            self.add_files(list(files))
    
    def add_files(self, files: List[str]):
        """添加檔案到列表"""
        valid_files = []
        invalid_files = []
        
        for file_path in files:
            # 驗證檔案
            is_valid, error_msg = FileUtils.validate_input_file(file_path)
            
            if is_valid and file_path not in self.file_paths:
                valid_files.append(file_path)
                self.file_paths.append(file_path)
                
                # 添加到列表框
                filename = os.path.basename(file_path)
                self.files_listbox.insert(tk.END, filename)
            elif not is_valid:
                invalid_files.append(f"{os.path.basename(file_path)}: {error_msg}")
        
        # 顯示檔案列表
        if self.file_paths:
            self.files_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            # 更新拖拽區域文字
            file_count = len(self.file_paths)
            self.drop_area.config(
                text=f"已選擇 {file_count} 個檔案\n點擊或拖拽添加更多檔案"
            )
        
        # 顯示無效檔案警告
        if invalid_files:
            error_msg = "以下檔案無效:\n\n" + "\n".join(invalid_files[:5])
            if len(invalid_files) > 5:
                error_msg += f"\n... 還有 {len(invalid_files) - 5} 個檔案"
            messagebox.showwarning("檔案驗證", error_msg)
        
        # 通知父組件
        if valid_files:
            self.on_files_dropped(self.file_paths)
    
    def remove_selected(self):
        """移除選中的檔案"""
        selected_indices = self.files_listbox.curselection()
        
        if not selected_indices:
            messagebox.showinfo("提示", "請先選擇要移除的檔案")
            return
        
        # 從後往前刪除，避免索引變化
        for index in reversed(selected_indices):
            self.files_listbox.delete(index)
            del self.file_paths[index]
        
        # 更新UI
        self.update_ui_after_file_change()
        
        # 通知父組件
        self.on_files_dropped(self.file_paths)
    
    def clear_files(self):
        """清除所有檔案"""
        self.file_paths.clear()
        self.files_listbox.delete(0, tk.END)
        self.update_ui_after_file_change()
        
        # 通知父組件
        self.on_files_dropped(self.file_paths)
    
    def update_ui_after_file_change(self):
        """檔案變更後更新UI"""
        if not self.file_paths:
            # 隱藏檔案列表
            self.files_frame.pack_forget()
            
            # 恢復原始拖拽區域文字
            self.drop_area.config(
                text="拖拽音訊檔案到這裡\n或點擊選擇檔案\n\n支援格式: MP3, WAV, M4A, FLAC"
            )
        else:
            # 更新檔案計數
            file_count = len(self.file_paths)
            self.drop_area.config(
                text=f"已選擇 {file_count} 個檔案\n點擊或拖拽添加更多檔案"
            )
    
    def get_files(self) -> List[str]:
        """獲取當前檔案列表"""
        return self.file_paths.copy()
    
    def set_enabled(self, enabled: bool):
        """設置組件啟用狀態"""
        state = "normal" if enabled else "disabled"
        self.drop_area.config(state=state)
        self.files_listbox.config(state=state)