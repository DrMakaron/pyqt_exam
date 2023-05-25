from PyQt5 import QtCore

from loguru import logger

from system import SystemInfo


class Controller(QtCore.QObject):
    """
    Класс запрашивает данные о системе и отправляет их на отображение
    """

    timer_updater = QtCore.QTimer()

    processes_signal = QtCore.pyqtSignal(list)
    cpu_cores_signal = QtCore.pyqtSignal(int)
    start_trace_signal = QtCore.pyqtSignal()
    cpu_usage_signal = QtCore.pyqtSignal(list)
    ram_usage_signal = QtCore.pyqtSignal(float)
    fs_signal = QtCore.pyqtSignal(list)
    sys_info_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        """
        Конструктор класса
        """
        super().__init__()

        self.__current_data_pack = 0
        self.__cpu_core_send_flag = False

        self.sys_info = SystemInfo()

        self.init_signals()
        self.timer_updater.start(500)

    def init_signals(self) -> None:
        """
        Инициализация сигналов
        :return:
        """
        self.timer_updater.timeout.connect(self.send_data)

    def hand_request(self, num: int) -> None:
        """
        Метод обрабатывает запрос на обновление конкретного типа системной информации
        :param num: номер выбранного виджета: 0, 1, 2 или 3
        :return:
        """
        self.__current_data_pack = num
        logger.debug(f'Data pack updated to: {num} {self.__current_data_pack=}')

    def send_data(self) -> None:
        """
        Метод в зависимости от выбранного виджета отправляет на отображение выбранный тип информации
        0 - информация о процеммах
        1 - информация о загрузке ЦП и ОЗУ
        2 - информация о файловой системе
        3 - общая информация о системе
        :return:
        """
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
