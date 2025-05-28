import sys
import concurrent.futures
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QMessageBox, QSpacerItem, QSizePolicy, QToolBar, QFormLayout, QDialog
)
from PySide6.QtGui import QIcon, QFont, QAction
from PySide6.QtCore import Qt, QMetaObject

from src.utils import logger
import src.fiserv_and_linx.express as express
from src.fiserv_and_linx.gluo import acessar_tefway
from src.Services.service_db import DataService


class CredentialDialog(QDialog):
    def __init__(self, db_service):
        super().__init__()
        self.db_service = db_service
        self.setWindowTitle("Configurar Credenciais")
        self.setFixedSize(300, 200)

        form_layout = QFormLayout()

        self.empresa_combo = QComboBox()
        self.empresa_combo.addItems(["Elgin", "Comnect", "Tefway"])
        self.empresa_combo.currentTextChanged.connect(self.toggle_otp_field)

        self.usuario_input = QLineEdit()
        self.senha_input = QLineEdit()
        self.senha_input.setEchoMode(QLineEdit.Password)
        self.otp_input = QLineEdit()

        form_layout.addRow("Empresa:", self.empresa_combo)
        form_layout.addRow("Usuário:", self.usuario_input)
        form_layout.addRow("Senha:", self.senha_input)
        self.otp_row = form_layout.addRow("OTP:", self.otp_input)

        self.salvar_btn = QPushButton("Salvar")
        self.salvar_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        self.salvar_btn.clicked.connect(self.register_credentials)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.salvar_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

        self.load_existing_credentials(self.empresa_combo.currentText())
        self.toggle_otp_field(self.empresa_combo.currentText())

    def toggle_otp_field(self, empresa):
        if empresa in ["Elgin", "Comnect"]:
            self.otp_input.show()
        else:
            self.otp_input.hide()
            self.otp_input.clear()
        self.load_existing_credentials(empresa)

    def load_existing_credentials(self, empresa):
        try:
            entries = self.db_service.get_entry(empresa)
            if entries:
                entry = entries[0]
                self.usuario_input.setText(entry["user"])
                self.senha_input.setText(entry["password"])
                if empresa in ["Elgin", "Comnect"]:
                    self.otp_input.setText(entry["otp"])
                self.salvar_btn.setText("Atualizar")
            else:
                self.usuario_input.clear()
                self.senha_input.clear()
                self.otp_input.clear()
                self.salvar_btn.setText("Salvar")
        except Exception as e:
            logger.warning(f"Não foi possível carregar credenciais para {empresa}: {e}")
            self.usuario_input.clear()
            self.senha_input.clear()
            self.otp_input.clear()
            self.salvar_btn.setText("Salvar")

    def register_credentials(self):
        try:
            empresa = self.empresa_combo.currentText()
            usuario = self.usuario_input.text().strip()
            senha = self.senha_input.text().strip()
            otp = self.otp_input.text().strip()

            if empresa in ["Elgin", "Comnect"] and not all([usuario, senha, otp]):
                raise ValueError("Todos os campos são obrigatórios!")

            if empresa == "Tefway" and not all([usuario, senha]):
                raise ValueError("Usuário e senha são obrigatórios para Tefway!")

            existing = self.db_service.get_entry(empresa)
            if existing:
                entry_id = existing[0]["id"]
                success = self.db_service.update_entry(
                    empresa, entry_id, user=usuario, password=senha,
                    otp=otp if empresa != "Tefway" else None
                )
            else:
                success = self.db_service.create_entry(
                    empresa, usuario, senha, otp if empresa != "Tefway" else ""
                )

            if success:
                QMessageBox.information(self, "Sucesso", "Credenciais salvas com sucesso.")
            else:
                QMessageBox.warning(self, "Falha", "Não foi possível salvar as credenciais.")

            self.accept()

        except Exception as e:
            logger.error(f"Erro ao salvar credenciais: {e}")
            QMessageBox.critical(self, "Erro", str(e))


class FastWayUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FastWay - Tefway")
        self.setFixedSize(400, 300)

        self.db_service = DataService()
        self.executor = concurrent.futures.ThreadPoolExecutor()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(30, 30, 30, 30)

        self.header = QLabel("FastWay - Tefway")
        self.header.setFont(QFont("Arial", 20, QFont.Bold))
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet("color: #333;")
        self.layout.addWidget(self.header)

        self.access_btn = QPushButton("Acessar Configurador")
        self.sales_btn = QPushButton("Verificar Vendas")
        self.tefway_btn = QPushButton("Acessar Tefway")

        for btn in [self.access_btn, self.sales_btn, self.tefway_btn]:
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1976D2;
                    color: white;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
            """)
            self.layout.addWidget(btn)

        self.access_btn.clicked.connect(self.access_configurator)
        self.sales_btn.clicked.connect(self.check_sales)
        self.tefway_btn.clicked.connect(self.access_tefway)

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.central_widget.setLayout(self.layout)

        self.create_toolbar()

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        settings_action = QAction(QIcon.fromTheme("preferences-system"), "Configurar Credenciais", self)
        settings_action.triggered.connect(self.show_credential_dialog)
        toolbar.addAction(settings_action)

    def show_credential_dialog(self):
        dialog = CredentialDialog(self.db_service)
        dialog.exec()

    def access_configurator(self):
        server, ok = self.get_selection(["Elgin", "Comnect"], "Selecione o servidor para acessar:")
        if ok:
            self.executor.submit(self.run_express, server)

    def run_express(self, server):
        try:
            express.run(1 if server == "Elgin" else 2)
            logger.info(f"Acessando configurador {server}")
        except Exception as e:
            logger.error(f"Erro ao acessar configurador: {str(e)}")
            self.show_error_message(str(e))

    def access_tefway(self):
        try:
            creds = self.db_service.get_entry("Tefway")
            if not creds:
                raise ValueError("Nenhuma credencial cadastrada para Tefway.")

            user = creds[0]["user"]
            password = creds[0]["password"]

            self.executor.submit(self.run_tefway, user, password)
            logger.info("Acessando Tefway...")

        except Exception as e:
            logger.error(f"Erro ao acessar Tefway: {str(e)}")
            self.show_error_message(str(e))

    def run_tefway(self, username, password):
        try:
            acessar_tefway(username, password)
        except Exception as e:
            logger.error(f"Erro ao executar Tefway: {str(e)}")
            self.show_error_message(f"Erro ao executar Tefway: {str(e)}")

    def check_sales(self):
        QMessageBox.information(
            self,
            "Em Desenvolvimento",
            "⚠️ A função de Verificar Vendas está em desenvolvimento.\nEm breve estará disponível!"
        )

    def get_selection(self, options, prompt):
        from PySide6.QtWidgets import QInputDialog
        item, ok = QInputDialog.getItem(self, "Seleção", prompt, options, 0, False)
        return item, ok

    def show_error_message(self, msg):
        QMetaObject.invokeMethod(
            self,
            lambda: QMessageBox.critical(self, "Erro", msg),
            Qt.ConnectionType.QueuedConnection
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = FastWayUI()
    window.show()

    sys.exit(app.exec())
