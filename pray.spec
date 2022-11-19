# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['src\\pray.py'],
    pathex=[],
    binaries=[],
    datas=[('.\\src\\modules', '.\\modules'),('.\\src\\interact', '.'),('.\\src\\assets', '.\\assets'),('.\\src\\config.json', '.')],
    hiddenimports=["PySide6.QtSvg"],
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

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Genshin_Pray_Export',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon='src\\assets\\icon.ico'
)
coll = COLLECT(
    exe,
	a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Genshin_Pray_Export',
)