from PyQt5 import QtWidgets, QtCore

from loguru import logger

from widgets import main_form, text_and_progress


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

    def show_fs_info(self, fs_info):
        logger.debug(fs_info)
        self.fs_table.setRowCount(len(fs_info))

        for i, device in enumerate(fs_info):
            for j, item in enumerate(device):
                if j != 5:
                    self.fs_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(item)))

                else:
                    widget_instance = text_and_progress.TextAndProgress(str(item), int(device.percent))
                    self.fs_table.setCellWidget(i, j, widget_instance.get_txt_progress_widget())

        self.fs_table.resizeColumnsToContents()
        self.fs_table.resizeRowsToContents()


