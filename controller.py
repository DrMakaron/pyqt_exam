from PyQt5 import QtCore

from loguru import logger

from system import SystemInfo


class Controller(QtCore.QObject):

    timer_updater = QtCore.QTimer()

    processes_signal = QtCore.pyqtSignal(list)
    fs_signal = QtCore.pyqtSignal(list)
    sys_info_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.__current_data_pack = 0

        self.sys_info = SystemInfo()

        self.init_signals()
        self.timer_updater.start(500)

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

            case 1:
                pass

            case 2:
                fs_info = self.sys_info.get_disk_info()
                self.fs_signal.emit(fs_info)

            case 3:
                system = self.sys_info.get_sys_info()

                info_string = f'Platform: {system.platform}\n' \
                              f'System: {system.system}\n' \
                              f'RAM: {system.ram} GB\n' \
                              f'CPU: {system.cpu}'

                self.sys_info_signal.emit(info_string)
