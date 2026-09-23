from pathlib import Path

from wiglyph.utils.paths import asset_path

_THEME_PATH = Path(__file__).with_name("theme.qss")

_ASSET_TOKENS = {
    "{{CHECK_ICON}}": asset_path("icons", "check.svg").as_posix(),
    "{{CHEVRON_ICON}}": asset_path("icons", "chevron-down.svg").as_posix(),
}


def load_stylesheet() -> str:
    stylesheet = _THEME_PATH.read_text(encoding="utf-8")

    for token, path in _ASSET_TOKENS.items():
        stylesheet = stylesheet.replace(token, path)

    return stylesheet
