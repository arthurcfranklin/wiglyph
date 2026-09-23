import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from wiglyph.config import APP_NAME, APP_VERSION, ORGANIZATION_NAME
from wiglyph.ui.main_window import MainWindow
from wiglyph.ui.styles import load_stylesheet
from wiglyph.utils.paths import asset_path


def create_application() -> QApplication:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName(ORGANIZATION_NAME)
    app.setWindowIcon(QIcon(str(asset_path("codeico.png"))))
    app.setStyleSheet(load_stylesheet())

    return app


def main() -> int:
    app = create_application()

    window = MainWindow()
    window.show()

    return app.exec()
