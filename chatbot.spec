# -*- mode: python ; coding: utf-8 -*-
import sys
sys.path.append('/usr/lib/python3.8/site-packages')  # Ajusta según tu sistema

block_cipher = None

a = Analysis(
    ['app/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('modelo/intents_combinate.json', 'modelo'),
        ('modelo/chatbot_model.h5', 'modelo'),
        ('modelo/classes.pkl',modelo),
        ('modelo/words.pkl',modelo)
    ],
    hiddenimports=['tensorflow'],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Chatbot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)