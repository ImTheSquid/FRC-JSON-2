from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel


class ControllerCreator(QDialog):
    def __init__(self):
        super().__init__()

        self.setModal(True)
        self.setWindowTitle('Controller Creation Wizard')
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(QLabel('Name'))

        self.exec_()
