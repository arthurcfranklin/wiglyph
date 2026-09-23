from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QLineEdit

from wiglyph.utils.paths import asset_path


class PasswordField(QLineEdit):
    def __init__(self) -> None:
        super().__init__()

        self._password_visible = False

        self._eye_icon = QIcon(str(asset_path("icons", "eye.svg")))
        self._eye_off_icon = QIcon(str(asset_path("icons", "eye-off.svg")))

        self.setPlaceholderText("Enter Wi-Fi password")
        self.setEchoMode(QLineEdit.EchoMode.Password)

        self._visibility_action = QAction(
            self._eye_icon,
            "Show password",
            self,
        )

        self._visibility_action.triggered.connect(self._toggle_password_visibility)

        self.addAction(
            self._visibility_action,
            QLineEdit.ActionPosition.TrailingPosition,
        )

        self.setStyleSheet(
            """
            QLineEdit {
                padding-right: 36px;
            }
            """
        )

    def set_password_visible(
        self,
        visible: bool,
    ) -> None:
        self._password_visible = visible

        self.setEchoMode(
            QLineEdit.EchoMode.Normal if visible else QLineEdit.EchoMode.Password
        )

        self._visibility_action.setIcon(
            self._eye_off_icon if visible else self._eye_icon
        )

        self._visibility_action.setText("Hide password" if visible else "Show password")

    def _toggle_password_visibility(
        self,
    ) -> None:
        self.set_password_visible(not self._password_visible)
