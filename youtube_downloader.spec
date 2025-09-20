# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 确保中文正常显示
import sys
import os

# 添加pytubefix库的hook
from PyInstaller.utils.hooks import collect_submodules

# 定义数据文件
# 如果有自定义图标，可以添加在这里
# icon_file = 'icon.ico'

a = Analysis(
    ['youtube_downloader.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=collect_submodules('pytubefix') + ['requests'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 定义exe配置
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTube视频下载器',  # 应用程序名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon=icon_file,  # 取消注释并设置图标路径
)

# 生成单个文件夹的输出
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='YouTube视频下载器',
)