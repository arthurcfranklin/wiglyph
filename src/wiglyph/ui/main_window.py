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

from wiglyph.config import APP_NAME
from wiglyph.core.qr_generator import QRGenerator
from wiglyph.core.wifi import SecurityType, WifiNetwork
from wiglyph.ui.widgets import PasswordField


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.qr_generator = QRGenerator()

        self.current_network: WifiNetwork | None = None
        self.current_image: Image.Image | None = None
        self.current_pixmap: QPixmap | None = None

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1100, 720)
        self.resize(1440, 900)

        self._build_ui()
        self._connect_signals()
        self._update_password_state()
        self._show_empty_state()

    def _build_ui(self) -> None:
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        page_layout = QVBoxLayout(central_widget)
        page_layout.setContentsMargins(56, 34, 56, 28)
        page_layout.setSpacing(0)

        page_layout.addLayout(self._create_header())
        page_layout.addSpacing(24)
        page_layout.addWidget(self._create_separator())
        page_layout.addSpacing(30)

        workspace = QWidget()
        workspace.setObjectName("workspace")
        workspace.setMaximumWidth(1400)
        workspace.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum,
        )

        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(26)

        primary_row = QHBoxLayout()
        primary_row.setContentsMargins(0, 0, 0, 0)
        primary_row.setSpacing(26)

        self.form_section = self._create_form_section()
        self.result_section = self._create_result_section()

        primary_row.addWidget(
            self.form_section,
            6,
            Qt.AlignmentFlag.AlignTop,
        )
        primary_row.addWidget(
            self.result_section,
            7,
            Qt.AlignmentFlag.AlignTop,
        )

        workspace_layout.addLayout(primary_row)

        self.access_details = self._create_access_details()
        workspace_layout.addWidget(self.access_details)

        workspace_layout.addWidget(self._create_information_module())

        centered_workspace = QHBoxLayout()
        centered_workspace.setContentsMargins(0, 0, 0, 0)
        centered_workspace.addStretch(1)
        centered_workspace.addWidget(workspace)
        centered_workspace.addStretch(1)

        page_layout.addLayout(centered_workspace)
        page_layout.addStretch(1)
        page_layout.addWidget(self._create_footer())

    def _create_header(self) -> QHBoxLayout:
        header_layout = QHBoxLayout()
        header_layout.setSpacing(24)

        identity_layout = QVBoxLayout()
        identity_layout.setSpacing(5)

        title = QLabel(APP_NAME)
        title.setObjectName("title")

        subtitle = QLabel("Compartilhe sua rede de forma simples e segura.")
        subtitle.setObjectName("subtitle")

        identity_layout.addWidget(title)
        identity_layout.addWidget(subtitle)

        privacy_badge = QLabel("Local e privado")
        privacy_badge.setObjectName("privacyBadge")
        privacy_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addLayout(identity_layout)
        header_layout.addStretch(1)
        header_layout.addWidget(
            privacy_badge,
            0,
            Qt.AlignmentFlag.AlignVCenter,
        )

        return header_layout

    def _create_form_section(self) -> QWidget:
        section = QFrame()
        section.setObjectName("formModule")
        section.setMinimumWidth(480)
        section.setMaximumWidth(620)
        section.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum,
        )

        layout = QVBoxLayout(section)
        layout.setContentsMargins(24, 22, 24, 24)
        layout.setSpacing(0)

        heading = QLabel("CONFIGURAÇÃO DA REDE")
        heading.setObjectName("sectionTitle")

        layout.addWidget(heading)
        layout.addSpacing(20)

        network_name_label = QLabel("Nome da rede")
        network_name_label.setObjectName("fieldLabel")

        self.ssid_input = QLineEdit()
        self.ssid_input.setPlaceholderText("Ex.: Minha Rede Wi-Fi")

        layout.addWidget(network_name_label)
        layout.addSpacing(7)
        layout.addWidget(self.ssid_input)
        layout.addSpacing(17)

        password_label = QLabel("Senha")
        password_label.setObjectName("fieldLabel")

        self.password_input = PasswordField()
        self.password_input.setPlaceholderText("Digite a senha da rede")

        layout.addWidget(password_label)
        layout.addSpacing(7)
        layout.addWidget(self.password_input)
        layout.addSpacing(17)

        security_label = QLabel("Segurança")
        security_label.setObjectName("fieldLabel")

        self.security_combo = QComboBox()
        self.security_combo.addItem(
            "WPA / WPA2 / WPA3",
            SecurityType.WPA.value,
        )
        self.security_combo.addItem(
            "WEP",
            SecurityType.WEP.value,
        )
        self.security_combo.addItem(
            "Rede aberta",
            SecurityType.OPEN.value,
        )

        layout.addWidget(security_label)
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
        section.setMinimumWidth(560)
        section.setMaximumWidth(720)
        section.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum,
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
        self.preview_area.setFixedHeight(350)
        self.preview_area.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        preview_layout = QVBoxLayout(self.preview_area)
        preview_layout.setContentsMargins(20, 18, 20, 18)

        self.preview_stack = QStackedWidget()
        self.preview_stack.setObjectName("previewStack")

        self.empty_state = self._create_empty_state()
        self.generated_state = self._create_generated_state()

        self.preview_stack.addWidget(self.empty_state)
        self.preview_stack.addWidget(self.generated_state)

        preview_layout.addWidget(self.preview_stack)

        layout.addWidget(self.preview_area)
        layout.addSpacing(14)

        self.actions_widget = self._create_actions()
        layout.addWidget(self.actions_widget)

        return section

    def _create_empty_state(self) -> QWidget:
        widget = QWidget()

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("▦")
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
        layout.addSpacing(3)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch(1)

        return widget

    def _create_generated_state(self) -> QWidget:
        widget = QWidget()

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.qr_label = QLabel()
        self.qr_label.setObjectName("qrPreview")
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setFixedSize(250, 250)

        self.ready_label = QLabel("Pronto para ler")
        self.ready_label.setObjectName("readyStatus")
        self.ready_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(
            self.qr_label,
            0,
            Qt.AlignmentFlag.AlignCenter,
        )
        layout.addWidget(
            self.ready_label,
            0,
            Qt.AlignmentFlag.AlignCenter,
        )

        return widget

    def _create_actions(self) -> QWidget:
        widget = QWidget()
        widget.setObjectName("actionsWidget")

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.copy_button = QPushButton("Copiar")
        self.copy_button.setObjectName("secondaryButton")

        self.save_button = QPushButton("Salvar PNG")
        self.save_button.setObjectName("secondaryButton")

        layout.addStretch(1)
        layout.addWidget(self.copy_button)
        layout.addWidget(self.save_button)

        return widget

    def _create_access_details(self) -> QWidget:
        widget = QFrame()
        widget.setObjectName("detailsModule")
        widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum,
        )

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 20, 24, 22)
        layout.setSpacing(12)

        heading = QLabel("DETALHES DO ACESSO")
        heading.setObjectName("sectionTitle")

        layout.addWidget(heading)

        details = QWidget()
        details.setObjectName("detailsContent")

        grid = QGridLayout(details)
        grid.setContentsMargins(0, 8, 0, 0)
        grid.setHorizontalSpacing(32)
        grid.setVerticalSpacing(7)

        for column in range(4):
            grid.setColumnStretch(column, 1)

        network_label = QLabel("NOME DA REDE")
        network_label.setObjectName("detailLabel")

        security_label = QLabel("SEGURANÇA")
        security_label.setObjectName("detailLabel")

        hidden_label = QLabel("REDE OCULTA")
        hidden_label.setObjectName("detailLabel")

        password_label = QLabel("SENHA")
        password_label.setObjectName("detailLabel")

        self.network_value = QLabel("—")
        self.network_value.setObjectName("detailValue")

        self.security_value = QLabel("—")
        self.security_value.setObjectName("detailValue")

        self.hidden_value = QLabel("—")
        self.hidden_value.setObjectName("detailValue")

        self.password_value = QLabel("—")
        self.password_value.setObjectName("detailValue")

        grid.addWidget(network_label, 0, 0)
        grid.addWidget(security_label, 0, 1)
        grid.addWidget(hidden_label, 0, 2)
        grid.addWidget(password_label, 0, 3)

        grid.addWidget(self.network_value, 1, 0)
        grid.addWidget(self.security_value, 1, 1)
        grid.addWidget(self.hidden_value, 1, 2)
        grid.addWidget(self.password_value, 1, 3)

        layout.addWidget(details)

        return widget

    def _create_information_module(self) -> QWidget:
        module = QFrame()
        module.setObjectName("informationModule")
        module.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum,
        )

        layout = QHBoxLayout(module)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(32)

        privacy = QWidget()

        privacy_layout = QVBoxLayout(privacy)
        privacy_layout.setContentsMargins(0, 0, 0, 0)
        privacy_layout.setSpacing(7)

        privacy_title = QLabel("PRIVACIDADE")
        privacy_title.setObjectName("infoPanelTitle")

        privacy_description = QLabel(
            "Tudo é processado neste dispositivo. "
            "Nenhuma credencial é enviada ou armazenada."
        )
        privacy_description.setObjectName("infoPanelDescription")
        privacy_description.setWordWrap(True)

        privacy_layout.addWidget(privacy_title)
        privacy_layout.addWidget(privacy_description)

        divider = QFrame()
        divider.setObjectName("informationDivider")
        divider.setFrameShape(QFrame.Shape.VLine)

        sharing = QWidget()

        sharing_layout = QVBoxLayout(sharing)
        sharing_layout.setContentsMargins(0, 0, 0, 0)
        sharing_layout.setSpacing(7)

        sharing_title = QLabel("COMPARTILHAMENTO")
        sharing_title.setObjectName("infoPanelTitle")

        sharing_description = QLabel(
            "Aponte a câmera de um dispositivo compatível para "
            "o QR Code e conecte-se sem digitar a senha."
        )
        sharing_description.setObjectName("infoPanelDescription")
        sharing_description.setWordWrap(True)

        sharing_layout.addWidget(sharing_title)
        sharing_layout.addWidget(sharing_description)

        layout.addWidget(privacy, 1)
        layout.addWidget(divider)
        layout.addWidget(sharing, 1)

        return module

    def _create_footer(self) -> QWidget:
        footer = QWidget()
        footer.setObjectName("footer")

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(0, 14, 0, 0)
        layout.setSpacing(0)

        copyright_label = QLabel("© 2026 Arthur Franklin")
        copyright_label.setObjectName("footerCopyright")

        privacy_label = QLabel("Processamento 100% local")
        privacy_label.setObjectName("footerMeta")

        layout.addWidget(copyright_label)
        layout.addStretch(1)
        layout.addWidget(privacy_label)

        return footer

    @staticmethod
    def _create_separator() -> QFrame:
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)

        return separator

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

        try:
            return SecurityType(security)
        except ValueError as error:
            raise TypeError("Invalid security type.") from error

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
            self._set_status(
                self._format_validation_error(str(error)),
                error=True,
            )
            return

        image_qt = ImageQt(image.convert("RGBA"))

        self.current_network = network
        self.current_image = image
        self.current_pixmap = QPixmap.fromImage(image_qt)

        self._update_access_details()
        self._show_generated_state()
        self._render_qr_preview()
        self._set_status("")

    def _invalidate_qr(self) -> None:
        if self.current_image is None:
            return

        self.current_network = None
        self.current_image = None
        self.current_pixmap = None

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
        self.network_value.setText("—")
        self.security_value.setText("—")
        self.hidden_value.setText("—")
        self.password_value.setText("—")

    def _update_access_details(self) -> None:
        if self.current_network is None:
            return

        self.network_value.setText(self.current_network.ssid)
        self.security_value.setText(
            self._security_display_name(self.current_network.security)
        )
        self.hidden_value.setText("Sim" if self.current_network.hidden else "Não")

        if self.current_network.security is SecurityType.OPEN:
            self.password_value.setText("Não necessária")
        else:
            self.password_value.setText("••••••••")

    @staticmethod
    def _security_display_name(
        security: SecurityType,
    ) -> str:
        if security is SecurityType.WPA:
            return "WPA / WPA2 / WPA3"

        if security is SecurityType.WEP:
            return "WEP"

        return "Rede aberta"

    def _render_qr_preview(self) -> None:
        if self.current_pixmap is None:
            return

        available_width = max(self.qr_label.width(), 1)
        available_height = max(self.qr_label.height(), 1)

        side = min(
            available_width,
            available_height,
            250,
        )

        scaled = self.current_pixmap.scaled(
            side,
            side,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation,
        )

        self.qr_label.setPixmap(scaled)

    def _copy_qr(self) -> None:
        if self.current_pixmap is None:
            return

        QGuiApplication.clipboard().setPixmap(self.current_pixmap)
        self.ready_label.setText("Copiado para a área de transferência")

    def _save_qr(self) -> None:
        if self.current_image is None:
            return

        destination, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar QR Code",
            "wiglyph.png",
            "Imagem PNG (*.png)",
        )

        if not destination:
            return

        path = Path(destination)

        if path.suffix.lower() != ".png":
            path = path.with_suffix(".png")

        try:
            self.current_image.save(
                path,
                format="PNG",
            )
        except OSError as error:
            QMessageBox.critical(
                self,
                "Não foi possível salvar o QR Code",
                str(error),
            )
            return

        self.ready_label.setText("QR Code salvo com sucesso")

    def _update_password_state(self) -> None:
        is_open = self._selected_security() is SecurityType.OPEN

        self.password_input.setEnabled(not is_open)

        if is_open:
            self.password_input.clear()
            self.password_input.set_password_visible(False)

    def _set_status(
        self,
        message: str,
        *,
        error: bool = False,
    ) -> None:
        self.status_label.setText(message)
        self.status_label.setProperty("error", error)

        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

    @staticmethod
    def _format_validation_error(
        message: str,
    ) -> str:
        translations = {
            "SSID cannot be empty.": ("Informe o nome da rede."),
            "Password is required for secured networks.": ("Informe a senha da rede."),
        }

        return translations.get(message, message)

    def resizeEvent(
        self,
        event: QResizeEvent,
    ) -> None:
        super().resizeEvent(event)
        self._render_qr_preview()
