# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['src/sangonomiya.py'],
    pathex=[],
    binaries=[],
    datas=[('src/modules', 'modules'),('src/assets', 'assets'),('src/components', 'components'),('src/configs', 'configs'),('src/languages', 'languages')],
    hiddenimports=[],
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
    name='sangonomiya',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='sangonomiya',
)
app = BUNDLE(
    coll,
    name='sangonomiya.app',
    icon='src/assets/avatar.png',
    bundle_identifier=None,
)
