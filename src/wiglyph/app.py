import ctypes
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from wiglyph.config import APP_NAME, APP_VERSION, ORGANIZATION_NAME
from wiglyph.ui.main_window import MainWindow
from wiglyph.ui.styles import load_stylesheet
from wiglyph.utils.paths import asset_path


def _set_windows_app_user_model_id() -> None:
    if sys.platform != "win32":
        return

    app_id = "ArthurFranklin.WiGlyph"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)


def create_application() -> QApplication:
    _set_windows_app_user_model_id()

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(ORGANIZATION_NAME)

    icon_file = "icon.ico" if sys.platform == "win32" else "icon.png"
    app.setWindowIcon(QIcon(str(asset_path(icon_file))))

    app.setStyleSheet(load_stylesheet())

    return app


def main() -> int:
    app = create_application()

    window = MainWindow()
    window.show()

    return app.exec()
