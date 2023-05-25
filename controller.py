from PyQt5 import QtCore

from loguru import logger

from system import SystemInfo


class Controller(QtCore.QObject):

    timer_updater = QtCore.QTimer()

    processes_signal = QtCore.pyqtSignal(list)
    cpu_cores_signal = QtCore.pyqtSignal(int)
    start_trace_signal = QtCore.pyqtSignal()
    cpu_usage_signal = QtCore.pyqtSignal(list)
    ram_usage_signal = QtCore.pyqtSignal(float)
    fs_signal = QtCore.pyqtSignal(list)
    sys_info_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.__current_data_pack = 0
        self.__cpu_core_send_flag = False

        self.sys_info = SystemInfo()

        self.init_signals()
        self.timer_updater.start(100)

    def init_signals(self) -> None:
        self.timer_updater.timeout.connect(self.send_data)

    def hand_request(self, num: int) -> None:
        self.__current_data_pack = num
        logger.debug(f'Data pack updated to: {num} {self.__current_data_pack=}')

    def send_data(self) -> None:
        match self.__current_data_pack:

            case 0:
                proc_info = self.sys_info.get_processes_info()
                self.processes_signal.emit(proc_info)
                self.__cpu_core_send_flag = False

            case 1:
                if not self.__cpu_core_send_flag:
                    cores = self.sys_info.get_cpu_quantity()
                    self.cpu_cores_signal.emit(cores)
                    self.start_trace_signal.emit()
                    self.__cpu_core_send_flag = True
                else:
                    cpu_usage = self.sys_info.get_cpu_usage()
                    ram_usage = self.sys_info.get_ram_usage()
                    self.cpu_usage_signal.emit(cpu_usage)
                    self.ram_usage_signal.emit(ram_usage)

            case 2:
                fs_info = self.sys_info.get_disk_info()
                self.fs_signal.emit(fs_info)
                self.__cpu_core_send_flag = False

            case 3:
                system = self.sys_info.get_sys_info()

                info_string = f'Platform: {system.platform}\n' \
                              f'System: {system.system}\n' \
                              f'RAM: {system.ram} GB\n' \
                              f'CPU: {system.cpu}'

                self.sys_info_signal.emit(info_string)
                self.__cpu_core_send_flag = False
