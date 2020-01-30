from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton


class ControllerCreator(QDialog):
    def __init__(self, current_names: []):
        super().__init__()

        self.setModal(True)
        self.setWindowTitle('Controller Creation Wizard')
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.current_names = current_names
        self.success = False

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(QLabel('Name'))
        self.name = QLineEdit()
        self.name.textChanged.connect(self.update_selection)
        main_layout.addWidget(self.name)

        main_layout.addStretch()

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        self.ok = QPushButton('OK')
        self.ok.clicked.connect(self.dialog_done)
        self.ok.setEnabled(False)
        button_layout.addWidget(self.ok)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.cancel_dialog)
        button_layout.addWidget(cancel_button)

        self.exec_()

    def update_selection(self):
        self.name.setStyleSheet('color:#FF0000' if self.name.text() in self.current_names else 'color:#000000')
        self.ok.setEnabled(self.name.text() not in self.current_names and len(self.name.text()) > 0)

    def cancel_dialog(self):
        self.close()

    def dialog_done(self):
        self.success = True
        self.cancel_dialog()

    # Returns a tuple as a result; first item is a success bool, second is name
    def get_result(self) -> tuple:
        return self.success, self.name.text()
