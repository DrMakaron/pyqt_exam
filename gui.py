from time import perf_counter

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QHeaderView

from loguru import logger

from widgets import main_form, text_and_progress


class MainGui(QtWidgets.QWidget, main_form.Ui_Form):
    tab_number_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.__core_datasets = None
        self.__start_trace_time = None

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

        # self.fs_table.resizeColumnsToContents()
        self.fs_table.resizeRowsToContents()

    def show_processes_info(self, proc_info):
        logger.debug(proc_info)

        self.proc_table.setRowCount(len(proc_info))

        for i, device in enumerate(proc_info):
            for j, item in enumerate(device):
                header_item = QtWidgets.QTableWidgetItem(str(device._fields[j]))
                self.proc_table.setHorizontalHeaderItem(j, header_item)
                self.proc_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(item)))

        self.proc_table.resizeRowsToContents()

    def generate_cores_datasets(self, quantity):
        logger.debug(quantity)
        self.__core_datasets = [[]] * quantity
        logger.debug(self.__core_datasets)

    def mark_start_trace(self):
        self.__start_trace_time = perf_counter()
        logger.debug('Trace start time marked!')

    def plot_cpu_usage(self, usage_dataset):
        logger.debug(usage_dataset)
