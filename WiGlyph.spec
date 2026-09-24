# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

project_root = Path(SPEC).resolve().parent

datas = [
    (
        str(project_root / "assets"),
        "assets",
    ),
    (
        str(project_root / "src" / "wiglyph" / "ui" / "styles" / "theme.qss"),
        "wiglyph/ui/styles",
    ),
]

a = Analysis(
    [str(project_root / "packaging" / "launcher.py")],
    pathex=[str(project_root / "src")],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="WiGlyph",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=str(project_root / "assets" / "icon.ico"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="WiGlyph",
)
