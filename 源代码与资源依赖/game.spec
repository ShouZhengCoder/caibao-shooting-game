# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['game.py'],
    pathex=[],
    binaries=[],
    datas=[('background1.jpg', '.'), ('background2.jpg', '.'), ('player_normal.jpg', '.'), ('boss.jpg', '.'), ('obstacles', 'obstacles'), ('background_music.mp3', '.'), ('intense_music.mp3', '.'), ('shoot_sound.mp3', '.'), ('hit_boss_sound.mp3', '.'), ('hit_player_sound.mp3', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
