from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class InfoPanel(QWidget):
    def __init__(
        self,
        title: str,
        description: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("infoPanel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("infoPanelTitle")

        description_label = QLabel(description)
        description_label.setObjectName("infoPanelDescription")
        description_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(description_label)
