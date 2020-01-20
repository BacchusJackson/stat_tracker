import sys, os
import yaml
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QTableWidget
from PySide2.QtWidgets import QTableWidgetItem
from PySide2.QtWidgets import QAbstractItemView
from PySide2.QtWidgets import QAction
from PySide2.QtWidgets import QMenuBar
from PySide2.QtWidgets import QFileDialog

import PySide2.QtCore as Core


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Button
        self.btn_plus = QPushButton('Add 1')
        self.btn_minus = QPushButton('Minus 1')
        self.btn_plus.clicked.connect(self.btn_plus_clicked)
        self.btn_minus.clicked.connect(self.btn_minus_clicked)
        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.btn_plus)
        self.btn_layout.addWidget(self.btn_minus)
        self.btn_container = QWidget()
        self.btn_container.setLayout(self.btn_layout)

        # Table
        self.table = QTableWidget(8, 2)
        self.table.setHorizontalHeaderLabels(['Stat', 'Points'])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.t_items = {'Warrior': (QTableWidgetItem('Warrior'), QTableWidgetItem('0')),
                        'Stealth': (QTableWidgetItem(), QTableWidgetItem()),
                        'Magic': (QTableWidgetItem(), QTableWidgetItem()),
                        'Good': (QTableWidgetItem(), QTableWidgetItem()),
                        'Neutral': (QTableWidgetItem(), QTableWidgetItem()),
                        'Evil': (QTableWidgetItem(), QTableWidgetItem()),
                        'Lawful': (QTableWidgetItem(), QTableWidgetItem()),
                        'Chaotic': (QTableWidgetItem(), QTableWidgetItem())}
        row = 0
        for item_name, item in self.t_items.items():
            item[0].setText(item_name)
            item[1].setText('0')
            item[1].setTextAlignment(Core.Qt.AlignHCenter)
            self.table.setItem(row, 0, self.t_items[item_name][0])
            self.table.setItem(row, 1, self.t_items[item_name][1])
            row += 1

        # Save / Load Buttons
        self.btn_save = QPushButton('Save')
        self.btn_load = QPushButton('Load')
        self.btn_save.clicked.connect(self.btn_save_clicked)
        self.btn_load.clicked.connect(self.btn_load_clicked)
        self.save_load_layout = QHBoxLayout()
        self.save_load_layout.addWidget(self.btn_save)
        self.save_load_layout.addWidget(self.btn_load)
        self.save_load_container = QWidget()
        self.save_load_container.setLayout(self.save_load_layout)

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.btn_container)
        self.main_layout.addWidget(self.table)
        self.main_layout.addWidget(self.save_load_container)
        self.setLayout(self.main_layout)

    @property
    def stats_dict(self) -> dict:
        return {stat: self.t_items.get(stat)[1].text() for stat in self.t_items}

    def btn_plus_clicked(self):
        for item_name, item in self.t_items.items():
            if item[0].isSelected() or item[1].isSelected():
                item[1].setText(f'{int(item[1].text()) + 1}')
            self.table.repaint()

    def btn_save_clicked(self):
        user_defined_file = QFileDialog.getSaveFileName(self, 'Save As ...')
        if not user_defined_file[0]:
            return
        file, ext = os.path.splitext(user_defined_file[0])
        file_id = file + '.yaml'

        with open(file_id, 'w') as file:
            yaml.dump(self.stats_dict, file)

    def btn_load_clicked(self):
        user_selected_file = QFileDialog.getOpenFileName(self, 'Open file...', '', '*.yaml')
        if not os.path.exists(user_selected_file[0]):
            return False
        with open(user_selected_file[0], 'r') as file:
            loaded_dict = yaml.full_load(file)
        for item_name, item in self.t_items.items():
            item[1].setText(loaded_dict.get(item_name, '0'))

    def btn_minus_clicked(self):
        for item_name, item in self.t_items.items():
            if item[0].isSelected() or item[1].isSelected():
                item[1].setText(f'{int(item[1].text()) - 1}')
            self.table.repaint()


class Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Stat Tracker')

        exit_action = QAction('&exit', self)
        exit_action.triggered.connect(self.close)

        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction('Save')
        file_menu.addAction(exit_action)

        self.widget = MainWidget()
        self.setCentralWidget(self.widget)


if __name__ == '__main__':
    app = QApplication()
    win = Window()
    win.resize(300, 400)
    win.show()
    sys.exit(app.exec_())
