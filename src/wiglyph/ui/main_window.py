from pathlib import Path

from PIL import Image
from PIL.ImageQt import ImageQt
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication, QPixmap, QResizeEvent
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from wiglyph.config import APP_NAME, APP_VERSION
from wiglyph.core.qr_generator import QRGenerator
from wiglyph.core.wifi import SecurityType, WifiNetwork
from wiglyph.ui.widgets import PasswordField, QRHistoryItem, QRHistoryWidget
from wiglyph.utils.paths import asset_path


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.qr_generator = QRGenerator()
        self.current_network: WifiNetwork | None = None
        self.current_image: Image.Image | None = None
        self.current_pixmap: QPixmap | None = None
        self.current_ssid: str | None = None
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1180, 760)
        self.resize(1500, 920)
        self._build_ui()
        self._connect_signals()
        self._update_password_state()
        self._show_empty_state()

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)
        page = QVBoxLayout(central)
        page.setContentsMargins(48, 28, 48, 24)
        page.setSpacing(0)
        page.addWidget(self._create_header())
        page.addSpacing(24)

        container = QWidget()
        container.setObjectName("contentContainer")
        container.setMaximumWidth(1500)
        container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(18)

        workspace = QWidget()
        workspace.setObjectName("workspace")
        workspace_layout = QHBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(20)

        main = QWidget()
        main.setObjectName("mainContent")
        main.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        main_layout = QVBoxLayout(main)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(18)

        primary = QHBoxLayout()
        primary.setContentsMargins(0, 0, 0, 0)
        primary.setSpacing(20)
        self.form_section = self._create_form_section()
        self.result_section = self._create_result_section()
        primary.addWidget(self.form_section, 5)
        primary.addWidget(self.result_section, 6)
        main_layout.addLayout(primary, 1)

        self.access_details = self._create_access_details()
        main_layout.addWidget(self.access_details)

        self.information_module = self._create_information_module()
        main_layout.addWidget(self.information_module)

        self.history_section = QRHistoryWidget(self._restore_history_item)
        workspace_layout.addWidget(main, 1)
        workspace_layout.addWidget(self.history_section)
        container_layout.addWidget(workspace, 1)

        centered = QHBoxLayout()
        centered.setContentsMargins(0, 0, 0, 0)
        centered.addStretch(1)
        centered.addWidget(container, 1)
        centered.addStretch(1)

        page.addLayout(centered, 1)
        page.addSpacing(18)
        page.addWidget(self._create_footer())

    def _create_header(self) -> QWidget:
        header = QFrame()
        header.setObjectName("appHeader")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 22)
        layout.setSpacing(14)

        icon = QLabel()
        icon.setObjectName("appIcon")
        icon.setFixedSize(50, 50)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(str(asset_path("icon.png")))
        if not pixmap.isNull():
            icon.setPixmap(
                pixmap.scaled(
                    44,
                    44,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        identity = QVBoxLayout()
        identity.setSpacing(3)
        title = QLabel(APP_NAME)
        title.setObjectName("title")
        subtitle = QLabel("Compartilhe sua rede com simplicidade e privacidade.")
        subtitle.setObjectName("subtitle")
        identity.addWidget(title)
        identity.addWidget(subtitle)

        status = QVBoxLayout()
        status.setSpacing(5)
        badge = QLabel("Local e privado")
        badge.setObjectName("privacyBadge")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version = QLabel(f"v{APP_VERSION}")
        version.setObjectName("headerVersion")
        version.setAlignment(Qt.AlignmentFlag.AlignRight)
        status.addWidget(badge, 0, Qt.AlignmentFlag.AlignRight)
        status.addWidget(version)

        layout.addWidget(icon)
        layout.addLayout(identity)
        layout.addStretch(1)
        layout.addLayout(status)
        return header

    def _create_form_section(self) -> QWidget:
        section = QFrame()
        section.setObjectName("formModule")
        section.setMinimumWidth(400)
        section.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        layout = QVBoxLayout(section)
        layout.setContentsMargins(24, 22, 24, 24)
        layout.setSpacing(0)

        heading = QLabel("CONFIGURAÇÃO DA REDE")
        heading.setObjectName("sectionTitle")
        layout.addWidget(heading)
        layout.addSpacing(20)

        label = QLabel("Nome da rede")
        label.setObjectName("fieldLabel")
        self.ssid_input = QLineEdit()
        self.ssid_input.setPlaceholderText("Ex.: Minha Rede Wi-Fi")
        layout.addWidget(label)
        layout.addSpacing(7)
        layout.addWidget(self.ssid_input)
        layout.addSpacing(17)

        label = QLabel("Senha")
        label.setObjectName("fieldLabel")
        self.password_input = PasswordField()
        self.password_input.setPlaceholderText("Digite a senha da rede")
        layout.addWidget(label)
        layout.addSpacing(7)
        layout.addWidget(self.password_input)
        layout.addSpacing(17)

        label = QLabel("Segurança")
        label.setObjectName("fieldLabel")
        self.security_combo = QComboBox()
        self.security_combo.addItem("WPA / WPA2 / WPA3", SecurityType.WPA.value)
        self.security_combo.addItem("WEP", SecurityType.WEP.value)
        self.security_combo.addItem("Rede aberta", SecurityType.OPEN.value)
        layout.addWidget(label)
        layout.addSpacing(7)
        layout.addWidget(self.security_combo)
        layout.addSpacing(17)

        self.hidden_checkbox = QCheckBox("Rede oculta")
        layout.addWidget(self.hidden_checkbox)
        layout.addSpacing(22)

        self.generate_button = QPushButton("Gerar QR Code")
        self.generate_button.setObjectName("primaryButton")
        self.generate_button.setDefault(True)
        layout.addWidget(self.generate_button)
        layout.addSpacing(10)

        self.status_label = QLabel("")
        self.status_label.setObjectName("status")
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumHeight(18)
        layout.addWidget(self.status_label)
        return section

    def _create_result_section(self) -> QWidget:
        section = QFrame()
        section.setObjectName("resultModule")
        section.setMinimumWidth(450)
        section.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        layout = QVBoxLayout(section)
        layout.setContentsMargins(24, 22, 24, 24)
        layout.setSpacing(0)
        heading = QLabel("SEU QR CODE")
        heading.setObjectName("sectionTitle")
        layout.addWidget(heading)
        layout.addSpacing(18)

        self.preview_area = QFrame()
        self.preview_area.setObjectName("previewArea")
        self.preview_area.setMinimumHeight(350)
        self.preview_area.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        preview_layout = QVBoxLayout(self.preview_area)
        preview_layout.setContentsMargins(20, 14, 20, 14)
        self.preview_stack = QStackedWidget()
        self.empty_state = self._create_empty_state()
        self.generated_state = self._create_generated_state()
        self.preview_stack.addWidget(self.empty_state)
        self.preview_stack.addWidget(self.generated_state)
        preview_layout.addWidget(self.preview_stack)
        layout.addWidget(self.preview_area, 1)
        return section

    def _create_empty_state(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)
        icon = QLabel("◇")
        icon.setObjectName("emptyStateIcon")
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title = QLabel("Seu QR Code aparecerá aqui")
        title.setObjectName("emptyStateTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description = QLabel(
            "Preencha os dados da rede para gerar um código de acesso."
        )
        description.setObjectName("emptyStateDescription")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setMaximumWidth(300)
        layout.addStretch(1)
        layout.addWidget(icon)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch(1)
        return widget

    def _create_generated_state(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 10, 8, 10)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label = QLabel()
        self.qr_label.setObjectName("qrPreview")
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setFixedSize(220, 220)
        self.ready_label = QLabel("Pronto para ler")
        self.ready_label.setObjectName("readyStatus")
        self.ready_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.actions_widget = self._create_actions()
        layout.addWidget(self.qr_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.ready_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.actions_widget, 0, Qt.AlignmentFlag.AlignCenter)
        return widget

    def _create_actions(self) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        self.copy_button = QPushButton("Copiar")
        self.copy_button.setObjectName("secondaryButton")
        self.save_button = QPushButton("Salvar PNG")
        self.save_button.setObjectName("secondaryButton")
        layout.addWidget(self.copy_button)
        layout.addWidget(self.save_button)
        return widget

    def _create_access_details(self) -> QWidget:
        widget = QFrame()
        widget.setObjectName("detailsModule")
        widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 18, 24, 20)
        layout.setSpacing(10)
        heading = QLabel("DETALHES DO ACESSO")
        heading.setObjectName("sectionTitle")
        layout.addWidget(heading)

        grid = QGridLayout()
        grid.setHorizontalSpacing(28)
        for column in range(4):
            grid.setColumnStretch(column, 1)

        labels = ("NOME DA REDE", "SEGURANÇA", "REDE OCULTA", "SENHA")
        for column, text in enumerate(labels):
            label = QLabel(text)
            label.setObjectName("detailLabel")
            grid.addWidget(label, 0, column)

        self.network_value = QLabel("—")
        self.security_value = QLabel("—")
        self.hidden_value = QLabel("—")
        self.password_value = QLabel("—")
        for column, value in enumerate(
            (
                self.network_value,
                self.security_value,
                self.hidden_value,
                self.password_value,
            )
        ):
            value.setObjectName("detailValue")
            grid.addWidget(value, 1, column)

        layout.addLayout(grid)
        return widget

    def _create_information_module(self) -> QWidget:
        module = QFrame()
        module.setObjectName("informationModule")
        module.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        layout = QHBoxLayout(module)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(28)

        def info(title: str, description: str) -> QWidget:
            widget = QWidget()
            box = QVBoxLayout(widget)
            box.setContentsMargins(0, 0, 0, 0)
            box.setSpacing(6)
            heading = QLabel(title)
            heading.setObjectName("infoPanelTitle")
            text = QLabel(description)
            text.setObjectName("infoPanelDescription")
            text.setWordWrap(True)
            box.addWidget(heading)
            box.addWidget(text)
            return widget

        privacy = info(
            "PRIVACIDADE",
            "O processamento é local. O histórico permanece somente durante esta sessão.",
        )
        sharing = info(
            "COMPARTILHAMENTO",
            "Aponte a câmera de um dispositivo compatível para o QR Code e conecte-se sem digitar a senha.",
        )
        divider = QFrame()
        divider.setObjectName("informationDivider")
        divider.setFrameShape(QFrame.Shape.VLine)
        layout.addWidget(privacy, 1)
        layout.addWidget(divider)
        layout.addWidget(sharing, 1)
        return module

    def _create_footer(self) -> QWidget:
        footer = QFrame()
        footer.setObjectName("footer")
        footer.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(0, 14, 0, 0)
        layout.setSpacing(16)

        copyright_label = QLabel("© 2026 WiGlyph")
        copyright_label.setObjectName("footerCopyright")

        privacy_label = QLabel("Processamento local · Sem persistência")
        privacy_label.setObjectName("footerMeta")
        privacy_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(copyright_label)
        layout.addStretch(1)
        layout.addWidget(privacy_label)

        return footer

    def _connect_signals(self) -> None:
        self.generate_button.clicked.connect(self._generate_qr)
        self.copy_button.clicked.connect(self._copy_qr)
        self.save_button.clicked.connect(self._save_qr)
        self.security_combo.currentIndexChanged.connect(self._update_password_state)
        self.ssid_input.returnPressed.connect(self._generate_qr)
        self.password_input.returnPressed.connect(self._generate_qr)
        self.ssid_input.textChanged.connect(self._invalidate_qr)
        self.password_input.textChanged.connect(self._invalidate_qr)
        self.security_combo.currentIndexChanged.connect(self._invalidate_qr)
        self.hidden_checkbox.toggled.connect(self._invalidate_qr)

    def _selected_security(self) -> SecurityType:
        security = self.security_combo.currentData()
        if not isinstance(security, str):
            raise TypeError("Invalid security type.")
        return SecurityType(security)

    def _build_network(self) -> WifiNetwork:
        return WifiNetwork(
            ssid=self.ssid_input.text(),
            security=self._selected_security(),
            password=self.password_input.text(),
            hidden=self.hidden_checkbox.isChecked(),
        )

    def _generate_qr(self) -> None:
        try:
            network = self._build_network()
            image = self.qr_generator.generate(network)
        except ValueError as error:
            self._set_status(self._format_validation_error(str(error)), error=True)
            return

        self.current_network = network
        self.current_image = image
        self.current_pixmap = QPixmap.fromImage(ImageQt(image.convert("RGBA")))
        self.current_ssid = network.ssid
        self.history_section.add_item(network.ssid, image)
        self._update_access_details()
        self._show_generated_state()
        self._render_qr_preview()
        self._set_status("")

    def _restore_history_item(self, item: QRHistoryItem) -> None:
        self.current_network = None
        self.current_image = item.image.copy()
        self.current_pixmap = QPixmap.fromImage(
            ImageQt(self.current_image.convert("RGBA"))
        )
        self.current_ssid = item.ssid
        self.preview_stack.setCurrentWidget(self.generated_state)
        self.actions_widget.show()
        self.ready_label.setText(f"QR Code de {item.ssid}")
        self.network_value.setText(item.ssid)
        self.security_value.setText("—")
        self.hidden_value.setText("—")
        self.password_value.setText("—")
        self._render_qr_preview()
        self._set_status("")

    def _invalidate_qr(self) -> None:
        if self.current_image is None:
            return
        self.current_network = None
        self.current_image = None
        self.current_pixmap = None
        self.current_ssid = None
        self._show_empty_state()
        self._set_status("")

    def _show_empty_state(self) -> None:
        self.preview_stack.setCurrentWidget(self.empty_state)
        self.actions_widget.hide()
        self._clear_access_details()

    def _show_generated_state(self) -> None:
        self.preview_stack.setCurrentWidget(self.generated_state)
        self.actions_widget.show()
        self.ready_label.setText("Pronto para ler")

    def _clear_access_details(self) -> None:
        for label in (
            self.network_value,
            self.security_value,
            self.hidden_value,
            self.password_value,
        ):
            label.setText("—")

    def _update_access_details(self) -> None:
        if self.current_network is None:
            return
        self.network_value.setText(self.current_network.ssid)
        self.security_value.setText(
            self._security_display_name(self.current_network.security)
        )
        self.hidden_value.setText("Sim" if self.current_network.hidden else "Não")
        self.password_value.setText(
            "Não necessária"
            if self.current_network.security is SecurityType.OPEN
            else "••••••••"
        )

    @staticmethod
    def _security_display_name(security: SecurityType) -> str:
        if security is SecurityType.WPA:
            return "WPA / WPA2 / WPA3"
        if security is SecurityType.WEP:
            return "WEP"
        return "Rede aberta"

    def _render_qr_preview(self) -> None:
        if self.current_pixmap is None:
            return
        side = min(max(self.qr_label.width(), 1), max(self.qr_label.height(), 1), 220)
        self.qr_label.setPixmap(
            self.current_pixmap.scaled(
                side,
                side,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.FastTransformation,
            )
        )

    def _copy_qr(self) -> None:
        if self.current_pixmap is None:
            return
        QGuiApplication.clipboard().setPixmap(self.current_pixmap)
        self.ready_label.setText("Copiado para a área de transferência")

    def _save_qr(self) -> None:
        if self.current_image is None:
            return
        name = (
            self._safe_filename(self.current_ssid) if self.current_ssid else "wiglyph"
        )
        destination, _ = QFileDialog.getSaveFileName(
            self, "Salvar QR Code", f"{name}.png", "Imagem PNG (*.png)"
        )
        if not destination:
            return
        path = Path(destination)
        if path.suffix.lower() != ".png":
            path = path.with_suffix(".png")
        try:
            self.current_image.save(path, format="PNG")
        except OSError as error:
            QMessageBox.critical(self, "Não foi possível salvar o QR Code", str(error))
            return
        self.ready_label.setText("QR Code salvo com sucesso")

    @staticmethod
    def _safe_filename(value: str) -> str:
        invalid = '<>:"/\\|?*'
        safe = "".join("_" if char in invalid else char for char in value.strip())
        return safe or "wiglyph"

    def _update_password_state(self) -> None:
        is_open = self._selected_security() is SecurityType.OPEN
        self.password_input.setEnabled(not is_open)
        if is_open:
            self.password_input.clear()
            self.password_input.set_password_visible(False)

    def _set_status(self, message: str, *, error: bool = False) -> None:
        self.status_label.setText(message)
        self.status_label.setProperty("error", error)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

    @staticmethod
    def _format_validation_error(message: str) -> str:
        return {
            "SSID cannot be empty.": "Informe o nome da rede.",
            "Password is required for secured networks.": "Informe a senha da rede.",
        }.get(message, message)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._render_qr_preview()
