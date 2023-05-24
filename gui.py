from PyQt5 import QtWidgets, QtCore

from loguru import logger

from widgets import main_form


class MainGui(QtWidgets.QWidget, main_form.Ui_Form):
    tab_number_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.init_signals()

    def init_signals(self):
        self.tabWidget.currentChanged.connect(self.send_tab_number)

    def send_tab_number(self):
        sender = self.sender()
        tab_number = sender.currentIndex()
        self.tab_number_signal.emit(tab_number)
        logger.debug(f'Tab {tab_number} selected.')

    def show_sys_info(self, info_string: str) -> None:
        logger.debug(f'Sys info received: {info_string}')
        self.info.setPlainText(info_string)

    def show_fs_info(self, info):
        logger.debug(info)
