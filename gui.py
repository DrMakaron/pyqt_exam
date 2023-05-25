from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

from loguru import logger

from widgets import main_form, text_and_progress
from resources import colors


class MainGui(QtWidgets.QWidget, main_form.Ui_Form):

    CHUNK_SIZE = 100
    MAX_CHUNKS = 10

    tab_number_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.__core_datasets = None
        self.__start_trace_time = None
        self.__gridLayout_plot = None
        self.__ram_usage_data = []
        self.gridLayout_plot = None
        self.gridLayout_plot_1 = None
        self.view_plot = None
        self.view_plot_1 = None
        self.plot = None
        self.plot_1 = None

        self.init_plot_widgets()
        self.init_signals()

    def init_plot_widgets(self):
        self.gridLayout_plot = QtWidgets.QGridLayout(self.plot_cpu_widget)
        self.view_plot = pg.GraphicsLayoutWidget(show=True)
        self.gridLayout_plot.addWidget(self.view_plot)
        self.plot = self.view_plot.addPlot()
        self.plot.showGrid(True, True, 1.0)
        # self.plot.setLabel('bottom', 'Counts', 'num')
        self.plot.setLabel('left', 'CPU usage', '%')

        self.gridLayout_plot_1 = QtWidgets.QGridLayout(self.plot_ram_widget)
        self.view_plot_1 = pg.GraphicsLayoutWidget(show=True)
        self.gridLayout_plot_1.addWidget(self.view_plot_1)
        self.plot_1 = self.view_plot_1.addPlot()
        self.plot_1.showGrid(True, True, 1.0)
        self.plot_1.setLabel('bottom', 'Counts', 'num')
        self.plot_1.setLabel('left', 'RAM usage', '%')

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

    def generate_datasets(self, quantity):
        logger.debug(quantity)
        self.__core_datasets = [[] for _ in range(quantity)]
        self.__ram_usage_data = []
        logger.debug(self.__core_datasets)

    @staticmethod
    def _generate_cpu_statistic_string(cpu_usage_data):
        data = [f' CPU {i + 1}: {usage} % ' for i, usage in enumerate(cpu_usage_data)]
        result = '----------------'.join(data)
        print(result)
        return result

    def plot_cpu_usage(self, usage_dataset):
        logger.debug(usage_dataset)
        self.plot.clear()

        for i, value in enumerate(usage_dataset):
            self.__core_datasets[i].append(value)

        for i, data in enumerate(self.__core_datasets):
            curve = self.plot.plot(data, pen=colors.COLORS.get(i + 1))
            curve.setData(data)

        self.plot.setLabel('bottom', self._generate_cpu_statistic_string(usage_dataset), 'num')

    def plot_ram_usage(self, usage_percent):
        logger.debug(usage_percent)
        self.plot_1.clear()
        self.__ram_usage_data.append(usage_percent)

        curve = self.plot_1.plot(self.__ram_usage_data, pen=colors.COLORS.get(1))
        curve.setData(self.__ram_usage_data)
