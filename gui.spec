# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gui.py'],
    pathex=['.'],  # Ensure the current directory is in the path
    binaries=[],
    datas=[('venv/Scripts/chromedriver.exe', 'venv/Scripts')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,  # Exclude binaries from EXE, add them in COLLECT
    name='gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=False,  # Change to True if you want a console window
)

coll = COLLECT(
    exe,
    a.binaries,  # Ensure binaries are included in the COLLECT step
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='gui',
)
