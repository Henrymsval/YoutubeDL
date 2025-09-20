#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试pytubefix库是否能正常工作
"""

import os
import sys
from pytubefix import YouTube
from pytubefix.cli import on_progress  # 导入进度条功能

def test_youtube_download():
    """测试YouTube视频下载功能"""
    print("测试pytubefix库是否能正常工作...")
    print(f"当前Python版本: {sys.version}")
    
    # 使用一个公开的测试视频URL
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print(f"测试URL: {test_url}")
    
    try:
        # 创建YouTube对象，添加进度回调
        yt = YouTube(test_url, on_progress_callback=on_progress)
        print(f"视频标题: {yt.title}")
        print(f"视频时长: {yt.length}秒")
        print(f"视频作者: {yt.author}")
        print(f"视频观看次数: {yt.views}")
        
        # 获取最高分辨率的视频流
        print("\n获取可用视频流...")
        stream = yt.streams.get_highest_resolution()
        print(f"选择的流: {stream}")
        
        # 创建下载目录（如果不存在）
        download_dir = "downloads"
        os.makedirs(download_dir, exist_ok=True)
        
        # 下载视频
        print(f"\n开始下载视频到 '{download_dir}' 目录...")
        stream.download(output_path=download_dir)
        print("\n✅ 视频下载成功！")
        print("🎉 pytubefix库工作正常，已成功解决HTTP 410错误问题。")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_youtube_download()