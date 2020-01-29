import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QGroupBox, QVBoxLayout, QLabel, QComboBox, QPushButton, \
    QLineEdit, QSpinBox, QTableWidget, QHeaderView

from controllerCreator import ControllerCreator


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Data
        self.changes_saved = True
        self.controller_bindings = {}

        # Initialize GUI
        main_layout = QHBoxLayout()

        # Binding setup
        setup_group = QGroupBox('Binding Setup')
        setup_layout = QVBoxLayout()
        setup_group.setLayout(setup_layout)
        main_layout.addWidget(setup_group)

        option_layout = QHBoxLayout()
        setup_layout.addLayout(option_layout)

        # Controller selection
        pilot_layout = QVBoxLayout()
        option_layout.addLayout(pilot_layout)
        pilot_layout.addWidget(QLabel('Controller'))
        self.pilot_select = QComboBox()
        self.pilot_select.setEnabled(False)
        pilot_layout.addWidget(self.pilot_select)

        # Controller type selection
        controller_layout = QVBoxLayout()
        option_layout.addLayout(controller_layout)
        controller_layout.addWidget(QLabel('Controller Type'))
        self.controller_select = QComboBox()
        self.controller_select.addItems(['XBox Compatible', 'Joystick/Other'])
        controller_layout.addWidget(self.controller_select)

        # Key and port pair
        key_port_layout = QHBoxLayout()
        setup_layout.addLayout(key_port_layout)

        # Key input
        key_layout = QVBoxLayout()
        key_port_layout.addLayout(key_layout)
        key_layout.addWidget(QLabel('Key'))
        self.key = QLineEdit()
        self.key.setPlaceholderText('Input a key string')
        key_layout.addWidget(self.key)

        # Port input
        port_layout = QVBoxLayout()
        key_port_layout.addLayout(port_layout)
        port_layout.addWidget(QLabel('Port'))
        self.port = QSpinBox()
        self.port.setMinimum(0)
        port_layout.addWidget(self.port)

        # Add spacing to keep options together
        setup_layout.addStretch()

        # Binding addition and JSON importing
        self.status = QLabel('Unfilled Parameters: Controller, Key String')
        self.status.setStyleSheet('color:#FF0000')
        self.status.setAlignment(Qt.AlignCenter)
        setup_layout.addWidget(self.status)
        self.create_controller_button = QPushButton('Create Controller...')
        self.create_controller_button.clicked.connect(self.create_controller)
        setup_layout.addWidget(self.create_controller_button)
        self.add_binding = QPushButton('Add Binding')
        self.add_binding.setEnabled(False)
        setup_layout.addWidget(self.add_binding)

        self.import_json = QPushButton('Import from JSON...')
        setup_layout.addWidget(self.import_json)

        # Binding list and export controls
        list_group = QGroupBox('Binding List')
        list_layout = QVBoxLayout()
        list_group.setLayout(list_layout)
        main_layout.addWidget(list_group)

        # List filters
        filter_layout = QHBoxLayout()
        list_layout.addLayout(filter_layout)

        pilot_f_layout = QVBoxLayout()
        filter_layout.addLayout(pilot_f_layout)
        pilot_f_layout.addWidget(QLabel('Controller'))
        self.pilot_filter = QComboBox()
        self.pilot_filter.setEnabled(False)
        pilot_f_layout.addWidget(self.pilot_filter)

        controller_f_layout = QVBoxLayout()
        filter_layout.addLayout(controller_f_layout)
        controller_f_layout.addWidget(QLabel('Controller Type'))
        self.controller_filter = QComboBox()
        self.controller_filter.addItems(['XBox Compatible', 'Joystick/Other'])
        controller_f_layout.addWidget(self.controller_filter)

        # List
        self.binding_list = QTableWidget(0, 2)
        self.reset_table()
        list_layout.addWidget(self.binding_list)

        # Add spacing to keep list options together
        list_layout.addStretch()

        # Removal and JSON export controls
        self.remove_binding_button = QPushButton('Remove Binding')
        self.remove_binding_button.setEnabled(False)
        list_layout.addWidget(self.remove_binding_button)
        self.export_json_button = QPushButton('Export to JSON...')
        self.export_json_button.setEnabled(False)
        list_layout.addWidget(self.export_json_button)

        # Set layout and open window
        self.setWindowTitle('Multi-Controller JSON Profile Configuration Tool v.0.1')
        self.setLayout(main_layout)
        self.show()

    # Resets the table that holds bindings
    def reset_table(self):
        self.binding_list.setRowCount(0)
        self.binding_list.setHorizontalHeaderLabels(['Key', 'Port'])
        self.binding_list.setAutoScroll(True)
        header = self.binding_list.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    # Updates 'Add Binding' button and status label
    def update_add_button(self):
        pass

    # Creates a controller
    def create_controller(self):
        ControllerCreator()


if __name__ == '__main__':
    app = QApplication([])
    win = Window()
    sys.exit(app.exec_())
