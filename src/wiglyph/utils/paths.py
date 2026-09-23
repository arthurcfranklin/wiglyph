import sys
from pathlib import Path


def project_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parents[3]


def asset_path(*parts: str) -> Path:
    return project_root().joinpath("assets", *parts)
