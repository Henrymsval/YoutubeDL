#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
YouTube视频下载器
"""
import os
import re
import sys
import time
import json
import requests
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import pytubefix
from pytubefix import YouTube
from pytubefix.cli import on_progress

# 打印使用的pytubefix版本
print(f"使用的pytubefix版本: {pytubefix.__version__}")

class YoutubeDownloaderApp:
    """YouTube视频下载器GUI应用"""
    def __init__(self, root):
        """初始化应用"""
        self.root = root
        self.root.title("YouTube视频下载器")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 设置中文字体
        self.style = ttk.Style()
        self.style.configure("TLabel", font=(
            "SimHei", 10))
        self.style.configure("TButton", font=(
            "SimHei", 10))
        self.style.configure("TEntry", font=(
            "SimHei", 10))
        self.style.configure("TRadiobutton", font=(
            "SimHei", 10))
        
        # 视频信息
        self.yt = None
        self.download_path = os.getcwd()
        self.is_downloading = False
        
        # 创建UI
        self._create_widgets()
        
        # 检查更新
        self._check_for_updates()
    
    def _create_widgets(self):
        """创建UI组件"""
        # URL输入区域
        url_frame = ttk.Frame(self.root, padding="10")
        url_frame.pack(fill=tk.X)
        
        ttk.Label(url_frame, text="YouTube视频URL:").pack(anchor=tk.W)
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(fill=tk.X, pady=5)
        self.url_entry.bind("<Return>", lambda event: self._get_video_info())
        
        # 按钮区域
        button_frame = ttk.Frame(self.root, padding="0 0 10 10")
        button_frame.pack(fill=tk.X, anchor=tk.E)
        
        self.get_info_btn = ttk.Button(
            button_frame, text="获取视频信息", command=self._get_video_info)
        self.get_info_btn.pack(side=tk.RIGHT, padx=5)
        
        # 视频信息区域
        info_frame = ttk.LabelFrame(self.root, text="视频信息", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 视频标题
        title_frame = ttk.Frame(info_frame)
        title_frame.pack(fill=tk.X, pady=2)
        ttk.Label(title_frame, text="标题:", width=8).pack(side=tk.LEFT)
        self.title_var = tk.StringVar()
        ttk.Label(title_frame, textvariable=self.title_var, wraplength=500).pack(
            side=tk.LEFT, fill=tk.X, expand=True)
        
        # 视频时长
        length_frame = ttk.Frame(info_frame)
        length_frame.pack(fill=tk.X, pady=2)
        ttk.Label(length_frame, text="时长:", width=8).pack(side=tk.LEFT)
        self.length_var = tk.StringVar()
        ttk.Label(length_frame, textvariable=self.length_var).pack(side=tk.LEFT)
        
        # 视频作者
        author_frame = ttk.Frame(info_frame)
        author_frame.pack(fill=tk.X, pady=2)
        ttk.Label(author_frame, text="作者:", width=8).pack(side=tk.LEFT)
        self.author_var = tk.StringVar()
        ttk.Label(author_frame, textvariable=self.author_var).pack(side=tk.LEFT)
        
        # 视频观看次数
        views_frame = ttk.Frame(info_frame)
        views_frame.pack(fill=tk.X, pady=2)
        ttk.Label(views_frame, text="观看次数:", width=8).pack(side=tk.LEFT)
        self.views_var = tk.StringVar()
        ttk.Label(views_frame, textvariable=self.views_var).pack(side=tk.LEFT)
        
        # 下载选项区域
        options_frame = ttk.LabelFrame(self.root, text="下载选项", padding="10")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 下载路径
        path_frame = ttk.Frame(options_frame)
        path_frame.pack(fill=tk.X, pady=5)
        ttk.Label(path_frame, text="保存路径:", width=8).pack(side=tk.LEFT)
        self.path_var = tk.StringVar(value=self.download_path)
        ttk.Entry(path_frame, textvariable=self.path_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(path_frame, text="浏览...", command=self._browse_path).pack(
            side=tk.RIGHT)
        
        # 下载质量
        quality_frame = ttk.Frame(options_frame)
        quality_frame.pack(fill=tk.X, pady=5)
        ttk.Label(quality_frame, text="下载质量:", width=8).pack(side=tk.LEFT)
        self.quality_var = tk.StringVar(value="highest")
        ttk.Radiobutton(quality_frame, text="最高质量", 
                       variable=self.quality_var, value="highest").pack(side=tk.LEFT)
        ttk.Radiobutton(quality_frame, text="仅音频", 
                       variable=self.quality_var, value="audio").pack(side=tk.LEFT)
        ttk.Radiobutton(quality_frame, text="最低质量", 
                       variable=self.quality_var, value="lowest").pack(side=tk.LEFT)
        
        # 进度条区域
        progress_frame = ttk.Frame(self.root, padding="10")
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="准备就绪")
        self.progress_label.pack(anchor=tk.CENTER)
        
        # 下载按钮
        self.download_btn = ttk.Button(
            self.root, text="开始下载", command=self._start_download, state=tk.DISABLED)
        self.download_btn.pack(pady=10)
    
    def _browse_path(self):
        """浏览下载路径"""
        path = filedialog.askdirectory()
        if path:
            self.download_path = path
            self.path_var.set(path)
    
    def _get_video_info(self):
        """获取视频信息"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("错误", "请输入YouTube视频URL")
            return
        
        # 禁用按钮
        self.get_info_btn.config(state=tk.DISABLED)
        self.download_btn.config(state=tk.DISABLED)
        self.progress_label.config(text="正在获取视频信息...")
        
        # 在新线程中获取视频信息
        threading.Thread(target=self._fetch_video_info, args=(url,)).start()
    
    def _fetch_video_info(self, url):
        """在后台线程中获取视频信息"""
        try:
            # 验证URL格式
            if not self._is_valid_youtube_url(url):
                self.root.after(0, lambda: messagebox.showerror(
                    "错误", "无效的YouTube URL"))
                self.root.after(0, lambda: self._reset_ui_state())
                return
            
            # 验证URL是否可访问
            print(f"验证URL有效性...")
            response = requests.head(url, allow_redirects=True, timeout=10)
            if response.status_code != 200:
                self.root.after(0, lambda: messagebox.showerror(
                    "错误", f"无法访问URL，状态码: {response.status_code}"))
                self.root.after(0, lambda: self._reset_ui_state())
                return
            print(f"URL验证成功，状态码: {response.status_code}")
            
            # 尝试创建YouTube对象
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    print(f"尝试 {attempt+1}/{max_retries}: 创建YouTube对象")
                    self.yt = YouTube(url, on_progress_callback=lambda stream, chunk, bytes_remaining: 
                                     self._update_progress(stream, chunk, bytes_remaining))
                    print(f"尝试 {attempt+1} 成功: YouTube对象创建成功")
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"尝试 {attempt+1} 失败: {str(e)}")
                    time.sleep(1)  # 等待1秒后重试
            
            # 获取视频信息
            print("开始获取可用的视频流...")
            title = self.yt.title
            length = self._format_time(self.yt.length)
            author = self.yt.author
            views = f"{self.yt.views:,}"
            
            # 更新UI
            self.root.after(0, lambda: self.title_var.set(title))
            self.root.after(0, lambda: self.length_var.set(length))
            self.root.after(0, lambda: self.author_var.set(author))
            self.root.after(0, lambda: self.views_var.set(views))
            self.root.after(0, lambda: self.progress_label.config(text="视频信息获取成功"))
            self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL))
            print("视频信息获取成功")
        except Exception as e:
            error_msg = str(e)
            print(f"获取视频信息失败: {error_msg}")
            
            # 特殊处理HTTP 410错误
            if "HTTP Error 410" in error_msg:
                self.root.after(0, lambda: messagebox.showerror(
                    "错误", "YouTube API已变更，导致HTTP 410错误。\n请确保您使用的是最新版本的pytubefix库。\n可以通过命令：python -m pip install --upgrade pytubefix 来更新。"))
            else:
                self.root.after(0, lambda: messagebox.showerror(
                    "错误", f"获取视频信息失败: {error_msg}"))
            
            self.root.after(0, lambda: self._reset_ui_state())
        finally:
            self.root.after(0, lambda: self.get_info_btn.config(state=tk.NORMAL))
    
    def _start_download(self):
        """开始下载视频"""
        if not self.yt or self.is_downloading:
            return
        
        # 禁用按钮
        self.get_info_btn.config(state=tk.DISABLED)
        self.download_btn.config(state=tk.DISABLED)
        self.is_downloading = True
        self.progress_var.set(0)
        
        # 在新线程中下载
        threading.Thread(target=self._download_video).start()
    
    def _download_video(self):
        """在后台线程中下载视频"""
        try:
            # 选择下载质量
            quality = self.quality_var.get()
            if quality == "highest":
                stream = self.yt.streams.get_highest_resolution()
            elif quality == "audio":
                stream = self.yt.streams.get_audio_only()
            else:  # lowest
                stream = self.yt.streams.get_lowest_resolution()
            
            # 确保下载目录存在
            os.makedirs(self.download_path, exist_ok=True)
            
            # 开始下载
            self.root.after(0, lambda: self.progress_label.config(
                text=f"正在下载: {self.yt.title}"))
            
            stream.download(output_path=self.download_path)
            
            # 下载完成
            self.root.after(0, lambda: self.progress_label.config(
                text=f"下载完成: {self.yt.title}"))
            self.root.after(0, lambda: messagebox.showinfo(
                "成功", f"视频下载成功！\n保存至: {self.download_path}"))
        except Exception as e:
            error_msg = str(e)
            print(f"下载失败: {error_msg}")
            self.root.after(0, lambda: messagebox.showerror(
                "错误", f"下载失败: {error_msg}"))
        finally:
            self.is_downloading = False
            self.root.after(0, lambda: self.get_info_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL))
    
    def _update_progress(self, stream, chunk, bytes_remaining):
        """更新下载进度"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.root.after(0, lambda: self.progress_var.set(percentage))
        
        # 更新进度标签
        downloaded_mb = bytes_downloaded / (1024 * 1024)
        total_mb = total_size / (1024 * 1024)
        self.root.after(0, lambda: self.progress_label.config(
            text=f"下载中: {downloaded_mb:.2f} MB / {total_mb:.2f} MB ({percentage:.1f}%)"))
    
    def _is_valid_youtube_url(self, url):
        """验证是否为有效的YouTube URL"""
        youtube_patterns = [
            r'^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+',
            r'^(https?://)?(www\.)?youtube\.com/embed/[\w-]+',
            r'^(https?://)?(www\.)?youtube\.com/v/[\w-]+',
            r'^(https?://)?youtu\.be/[\w-]+'
        ]
        
        for pattern in youtube_patterns:
            if re.match(pattern, url):
                return True
        return False
    
    def _format_time(self, seconds):
        """将秒数格式化为时:分:秒"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours}小时{minutes}分{seconds}秒"
        elif minutes > 0:
            return f"{minutes}分{seconds}秒"
        else:
            return f"{seconds}秒"
    
    def _reset_ui_state(self):
        """重置UI状态"""
        self.progress_label.config(text="准备就绪")
        self.get_info_btn.config(state=tk.NORMAL)
    
    def _check_for_updates(self):
        """检查是否有更新"""
        # 这里可以添加检查更新的逻辑
        pass

# 主函数
if __name__ == "__main__":
    # 确保中文显示正常
    root = tk.Tk()
    app = YoutubeDownloaderApp(root)
    root.mainloop()