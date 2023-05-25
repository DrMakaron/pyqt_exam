import platform
import re
import subprocess
from collections import namedtuple

from loguru import logger
import psutil


class SystemInfo:
    """
    Класс для получения информации о системе
    """
    def __init__(self):
        self.__info = namedtuple('System', 'platform system ram cpu')

    @staticmethod
    def _define_cpu() -> str:
        """
        Метод для получения модели процессора
        :return:
        """
        if platform.system() == "Windows":
            return platform.processor()

        elif platform.system() == "Linux":
            command = "cat /proc/cpuinfo"
            all_info = subprocess.check_output(command, shell=True).decode().strip()
            for line in all_info.split("\n"):
                if "model name" in line:
                    return re.sub(".*model name.*:", "", line, 1)

    def get_sys_info(self) -> namedtuple:
        """
        Метод для получения информации о системе
        :return:
        """
        info = self.__info(platform=platform.platform(),
                           system=platform.system(),
                           ram=round(psutil.virtual_memory().total / 1e9, 2),
                           cpu=self._define_cpu() + ' x' + str(psutil.cpu_count()))

        return info

    @staticmethod
    def _get_disk_devices():
        """
        Метод для получения информации о дисках
        :return:
        """
        return [dict(name=device.device,
                     fstype=device.fstype,
                     mountpoint=device.mountpoint) for device in psutil.disk_partitions() if 'rw' in device.opts]

    @staticmethod
    def _get_disk_usage(disks):
        """
        Метод для получения информации о степени использования дисков
        :param disks:
        :return:
        """
        return [dict(total=round(psutil.disk_usage(disk['mountpoint']).total / 1e9, 2),
                     used=round(psutil.disk_usage(disk['mountpoint']).used / 1e9, 2),
                     free=round(psutil.disk_usage(disk['mountpoint']).free / 1e9, 2),
                     percent=psutil.disk_usage(disk['mountpoint']).percent) for disk in disks]

    @staticmethod
    def _build_answer(disk_info, disk_usage):
        """
        Метод для формирования ответа на запрос о состоянии файловой системы
        :param disk_info:
        :param disk_usage:
        :return:
        """
        return [namedtuple('fs', info | disk)(**info | disk) for info, disk in zip(disk_info, disk_usage)]

    def get_disk_info(self):
        """
        Метод для предоставления информации о файловой системе
        :return:
        """
        disks = self._get_disk_devices()
        usages = self._get_disk_usage(disks)
        answer = self._build_answer(disks, usages)
        logger.debug(answer)
        return answer

    @staticmethod
    def get_processes_info():
        """
        Метод для предоставления информации о процессах, запущенных в системе
        :return:
        """
        lst = []

        for proc in psutil.process_iter():
            try:
                p_info = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'status'])
                p_info['memory'] = round(proc.memory_info().rss / 1e9, 2)
                lst.append(p_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return [namedtuple('proc', proc)(**proc) for proc in lst]

    @staticmethod
    def get_cpu_quantity():
        """
        Метод для предоставления данных о количетве ядер ЦП
        :return:
        """
        return psutil.cpu_count()

    @staticmethod
    def get_cpu_usage():
        """
        Метод для предоствления данных о загрузке ЦП
        :return:
        """
        return psutil.cpu_percent(percpu=True)

    @staticmethod
    def get_ram_usage():
        """
        Метод для предоставления данных о загрузке ОЗУ
        :return:
        """
        return psutil.virtual_memory().percent


if __name__ == '__main__':
    info_instance = SystemInfo()
    # info_ = info_instance.get_sys_info()
    # print(info_)
    # print(info_instance.get_disk_info())
    print(info_instance.get_ram_usage())
