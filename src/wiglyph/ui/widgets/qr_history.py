from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from PIL import Image
from PIL.ImageQt import ImageQt
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


@dataclass(slots=True)
class QRHistoryItem:
    ssid: str
    image: Image.Image
    created_at: datetime


class QRHistoryCard(QFrame):
    def __init__(
        self,
        item: QRHistoryItem,
        on_selected: Callable[[QRHistoryItem], None],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.item = item
        self._on_selected = on_selected

        self.setObjectName("historyCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 9, 12, 9)
        layout.setSpacing(12)

        preview = QLabel()
        preview.setObjectName("historyPreview")
        preview.setFixedSize(52, 52)
        preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap.fromImage(ImageQt(item.image.convert("RGBA")))
        preview.setPixmap(
            pixmap.scaled(
                44,
                44,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation,
            )
        )

        information = QVBoxLayout()
        information.setContentsMargins(0, 2, 0, 2)
        information.setSpacing(4)

        name = QLabel(item.ssid)
        name.setObjectName("historyNetworkName")
        name.setToolTip(item.ssid)

        created_at = QLabel(f"Gerado às {item.created_at:%H:%M}")
        created_at.setObjectName("historyTimestamp")

        information.addWidget(name)
        information.addWidget(created_at)

        layout.addWidget(preview)
        layout.addLayout(information, 1)

    def mousePressEvent(
        self,
        event: QMouseEvent,
    ) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._on_selected(self.item)

        super().mousePressEvent(event)


class QRHistoryWidget(QFrame):
    MAX_ITEMS = 5

    def __init__(
        self,
        on_selected: Callable[[QRHistoryItem], None],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._on_selected = on_selected
        self._items: list[QRHistoryItem] = []

        self.setObjectName("historyModule")
        self.setMinimumWidth(300)
        self.setMaximumWidth(360)
        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding,
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 22, 20, 20)
        layout.setSpacing(0)

        heading_row = QHBoxLayout()
        heading_row.setContentsMargins(0, 0, 0, 0)
        heading_row.setSpacing(12)

        heading = QLabel("HISTÓRICO DA SESSÃO")
        heading.setObjectName("sectionTitle")

        self.counter = QLabel(f"0 / {self.MAX_ITEMS}")
        self.counter.setObjectName("historyCounter")

        heading_row.addWidget(heading)
        heading_row.addStretch(1)
        heading_row.addWidget(self.counter)

        description = QLabel(
            "Reutilize os QR Codes gerados enquanto " "o WiGlyph estiver aberto."
        )
        description.setObjectName("historyDescription")
        description.setWordWrap(True)

        self.entries = QWidget()
        self.entries.setObjectName("historyEntries")

        self.entries_layout = QVBoxLayout(self.entries)
        self.entries_layout.setContentsMargins(0, 0, 0, 0)
        self.entries_layout.setSpacing(8)

        self.empty_state = QLabel(
            "Os QR Codes gerados nesta sessão " "aparecerão aqui."
        )
        self.empty_state.setObjectName("historyEmptyState")
        self.empty_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_state.setWordWrap(True)

        self.clear_button = QPushButton("Limpar histórico")
        self.clear_button.setObjectName("historyClearButton")
        self.clear_button.clicked.connect(self.clear)
        self.clear_button.hide()

        layout.addLayout(heading_row)
        layout.addSpacing(12)
        layout.addWidget(description)
        layout.addSpacing(18)
        layout.addWidget(self.empty_state)
        layout.addWidget(self.entries)
        layout.addStretch(1)
        layout.addSpacing(14)
        layout.addWidget(self.clear_button)

        self.entries.hide()

    def add_item(
        self,
        ssid: str,
        image: Image.Image,
    ) -> None:
        normalized_ssid = ssid.strip().casefold()

        self._items = [
            item
            for item in self._items
            if item.ssid.strip().casefold() != normalized_ssid
        ]

        self._items.insert(
            0,
            QRHistoryItem(
                ssid=ssid.strip(),
                image=image.copy(),
                created_at=datetime.now(),
            ),
        )

        self._items = self._items[: self.MAX_ITEMS]
        self._rebuild()

    def clear(self) -> None:
        self._items.clear()
        self._rebuild()

    def _rebuild(self) -> None:
        while self.entries_layout.count():
            layout_item = self.entries_layout.takeAt(0)
            widget = layout_item.widget()

            if widget is not None:
                widget.deleteLater()

        self.counter.setText(f"{len(self._items)} / {self.MAX_ITEMS}")

        has_items = bool(self._items)

        self.empty_state.setVisible(not has_items)
        self.entries.setVisible(has_items)
        self.clear_button.setVisible(has_items)

        for item in self._items:
            card = QRHistoryCard(
                item=item,
                on_selected=self._on_selected,
            )
            self.entries_layout.addWidget(card)
