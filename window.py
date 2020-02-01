import json
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QGroupBox, QVBoxLayout, QLabel, QComboBox, \
    QPushButton, QLineEdit, QSpinBox, QTableWidget, QHeaderView, QMessageBox, QTableWidgetItem, QFileDialog, QCheckBox

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
        self.pilot_select.currentIndexChanged.connect(self.update_status)
        pilot_layout.addWidget(self.pilot_select)

        # Controller type selection
        controller_layout = QVBoxLayout()
        option_layout.addLayout(controller_layout)
        controller_layout.addWidget(QLabel('Controller Type'))
        self.controller_select = QComboBox()
        self.controller_select.addItems(['XBox Compatible', 'Joystick/Other'])
        self.controller_select.currentIndexChanged.connect(self.update_status)
        controller_layout.addWidget(self.controller_select)

        # Key and port pair
        key_port_layout = QHBoxLayout()
        setup_layout.addLayout(key_port_layout)

        # Key input
        key_layout = QVBoxLayout()
        key_port_layout.addLayout(key_layout)
        key_layout.addWidget(QLabel('Key'))
        self.key = QLineEdit()
        self.key.textChanged.connect(self.update_status)
        self.key.setPlaceholderText('Input a key string')
        key_layout.addWidget(self.key)

        # Port input
        port_layout = QVBoxLayout()
        key_port_layout.addLayout(port_layout)
        port_layout.addWidget(QLabel('Port'))
        self.port = QSpinBox()
        self.port.setMinimum(0)
        self.port.setFixedWidth(100)
        port_layout.addWidget(self.port)

        # Add spacing to keep options together
        setup_layout.addStretch()

        # Binding addition and JSON importing
        self.status = QLabel('Unfilled Parameters: Controller, Key String')
        self.status.setStyleSheet('color:#FF0000')
        self.status.setAlignment(Qt.AlignCenter)
        setup_layout.addWidget(self.status)

        add_layout = QHBoxLayout()
        setup_layout.addLayout(add_layout)
        self.create_controller_button = QPushButton('Create Controller...')
        self.create_controller_button.clicked.connect(self.create_controller)
        add_layout.addWidget(self.create_controller_button)
        self.add_binding_button = QPushButton('Add Binding')
        self.add_binding_button.setEnabled(False)
        self.add_binding_button.clicked.connect(self.add_binding)
        add_layout.addWidget(self.add_binding_button)

        self.import_json_button = QPushButton('Import from JSON...')
        self.import_json_button.clicked.connect(self.import_json)
        setup_layout.addWidget(self.import_json_button)

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
        self.pilot_filter.currentIndexChanged.connect(self.update_table)
        pilot_f_layout.addWidget(self.pilot_filter)

        controller_f_layout = QVBoxLayout()
        filter_layout.addLayout(controller_f_layout)
        controller_f_layout.addWidget(QLabel('Controller Type'))
        self.controller_filter = QComboBox()
        self.controller_filter.addItems(['XBox Compatible', 'Joystick/Other'])
        self.controller_filter.currentIndexChanged.connect(self.update_table)
        controller_f_layout.addWidget(self.controller_filter)

        # List
        self.binding_list = QTableWidget(0, 2)
        self.reset_table()
        list_layout.addWidget(self.binding_list)

        # Add spacing to keep list options together
        list_layout.addStretch()

        # Removal and JSON export controls
        rm_layout = QHBoxLayout()
        list_layout.addLayout(rm_layout)

        self.remove_controller_button = QPushButton('Remove Controller')
        self.remove_controller_button.setEnabled(False)
        self.remove_controller_button.clicked.connect(self.remove_controller)
        rm_layout.addWidget(self.remove_controller_button)
        self.remove_binding_button = QPushButton('Remove Binding')
        self.remove_binding_button.setEnabled(False)
        self.remove_binding_button.clicked.connect(self.remove_binding)
        rm_layout.addWidget(self.remove_binding_button)
        self.export_json_button = QPushButton('Export to JSON...')
        self.export_json_button.setEnabled(False)
        self.export_json_button.clicked.connect(self.export_json)
        list_layout.addWidget(self.export_json_button)

        # Set layout and open window
        self.setWindowTitle('Multi-Controller JSON Profile Configuration Tool v.1.0')
        self.setLayout(main_layout)
        self.show()

    def get_current_dict(self, pilot: QComboBox, controller: QComboBox) -> dict or None:
        if len(pilot) == 0:
            return None
        dict_a = self.controller_bindings[pilot.currentText()]
        return dict_a['XBOX' if controller.currentText() == 'XBox Compatible' else 'JOY']

    # Resets the table that holds bindings
    def reset_table(self):
        self.binding_list.setRowCount(0)
        self.binding_list.setColumnCount(2)
        self.binding_list.setHorizontalHeaderLabels(['Key', 'Port'])
        self.binding_list.setAutoScroll(True)
        header = self.binding_list.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    def update_table(self):
        self.reset_table()
        if len(self.pilot_select) == 0:
            return
        selected_dict = self.get_current_dict(self.pilot_filter, self.controller_filter)
        if selected_dict is None or len(selected_dict) == 0:
            return
        self.binding_list.setRowCount(len(selected_dict))
        for index, (key, item) in enumerate(selected_dict.items()):
            self.binding_list.setItem(index, 0, QTableWidgetItem(key))
            self.binding_list.setItem(index, 1, QTableWidgetItem(str(item)))

        # Update removal buttons
        self.remove_controller_button.setEnabled(len(self.pilot_filter) > 0)
        self.remove_binding_button.setEnabled(len(selected_dict) > 0)
        self.export_json_button.setEnabled(len(selected_dict) > 0)

    # Updates controller selection combo boxes
    def update_combo_boxes(self):
        self.pilot_select.clear()
        self.pilot_select.addItems([key for key in self.controller_bindings])
        self.pilot_select.setEnabled(len(self.pilot_select) > 0)

        self.pilot_filter.clear()
        self.pilot_filter.addItems([key for key in self.controller_bindings])
        self.pilot_filter.setEnabled(len(self.pilot_select) > 0)

        self.update_status()

    # Updates 'Add Binding' button and status label
    def update_status(self):
        params = []
        if len(self.pilot_select) == 0:
            params.append('Controller')
        if len(self.key.text()) == 0:
            params.append('Key String')

        out_text = 'OK'
        self.status.setStyleSheet('color:#00AA00')
        if len(params) > 0:
            out_text = 'Unfilled Parameters: ' + ', '.join(params)
            self.status.setStyleSheet('color:#FF0000')

        if len(self.pilot_select) > 0 and self.get_current_dict(self.pilot_select, self.controller_select) is not None \
                and self.key.text() in \
                self.get_current_dict(self.pilot_select, self.controller_select):
            self.status.setStyleSheet('color:#FF0000')
            if out_text == 'OK':
                out_text = 'Key Already Used'
            else:
                out_text += '\nKey Already Used'

        self.status.setText(out_text)

        self.add_binding_button.setEnabled(out_text == 'OK')

    # Creates a controller
    def create_controller(self):
        dialog = ControllerCreator([key for key in self.controller_bindings])
        if not dialog.get_result()[0]:
            return
        self.controller_bindings[dialog.get_result()[1]] = {'XBOX': {}, 'JOY': {}}
        self.update_combo_boxes()
        self.pilot_select.setCurrentIndex(len(self.pilot_select) - 1)
        self.pilot_filter.setCurrentIndex(len(self.pilot_filter) - 1)

    def add_binding(self):
        self.controller_bindings[self.pilot_select.currentText()][
            'XBOX' if self.controller_select.currentText() == 'XBox Compatible' else 'JOY'][self.key.text()] = int(
            self.port.text())
        self.changes_saved = False
        self.port.setValue(0)
        self.key.clear()
        self.pilot_filter.setCurrentText(self.pilot_select.currentText())
        self.controller_filter.setCurrentText(self.controller_select.currentText())
        self.update_combo_boxes()
        self.update_table()

    def remove_controller(self):
        self.controller_bindings.pop(self.pilot_filter.currentText())
        self.update_combo_boxes()
        self.update_table()
        self.remove_controller_button.setEnabled(len(self.pilot_filter) > 0)
        if len(self.pilot_filter) == 0:
            self.remove_binding_button.setEnabled(False)
        else:
            self.remove_binding_button.setEnabled(len(self.get_current_dict(self.pilot_filter, self.controller_filter))
                                                  > 0)

    def remove_binding(self):
        model = self.binding_list.selectionModel()
        if len(model.selectedRows()) == 0:
            info = QMessageBox()
            info.setIcon(QMessageBox.Information)
            info.setWindowTitle('Binding Remover')
            info.setText('Please select a whole row.')
            info.exec()
            return
        sel_dict = self.get_current_dict(self.pilot_filter, self.controller_filter)
        for selection in model.selectedRows():
            sel_dict.pop(self.binding_list.item(selection.row(), 0).text())
        self.update_table()
        self.remove_binding_button.setEnabled(len(sel_dict) > 0)

    def import_json(self):
        checked = True
        if len(self.controller_bindings) > 0:
            confirmation = QMessageBox()
            confirmation.setIcon(QMessageBox.Question)
            confirmation.setWindowTitle('File Information')
            confirmation.setText('Are you sure you want to import?')
            check = QCheckBox()
            check.setText('Overwrite current entries')
            confirmation.setCheckBox(check)
            confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            confirmation.setInformativeText('Select check box to overwrite, deselect to append.')
            if confirmation.exec() == QMessageBox.No:
                return
            else:
                checked = check.isChecked()
        dialog = QFileDialog.getOpenFileName(self, 'Select JSON file...', '', '*.json')
        if not dialog or dialog[0] == '':
            return
        if checked:
            self.controller_bindings = json.load(open(dialog[0], 'r'))
        else:
            self.controller_bindings.update(json.load(open(dialog[0], 'r')))
        self.changes_saved = False
        self.update_combo_boxes()
        self.update_table()

    def export_json(self):
        dialog = QFileDialog.getSaveFileName(self, 'Select JSON file...', 'output.json', '*.json')
        if not dialog or dialog[0] == '':
            return
        json.dump(self.controller_bindings, open(dialog[0], 'w'))
        self.changes_saved = True

    # Handler to make sure all changes are saved
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.changes_saved:
            a0.accept()
        else:
            button_reply = QMessageBox.question(self, 'WARNING: Unsaved Changes', "Do you want to exit without saving?",
                                                QMessageBox.Yes | QMessageBox.No,
                                                QMessageBox.No)
            if button_reply == QMessageBox.No:
                a0.ignore()
            else:
                a0.accept()


if __name__ == '__main__':
    app = QApplication([])
    win = Window()
    sys.exit(app.exec_())
