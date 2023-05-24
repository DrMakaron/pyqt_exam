import platform
import re
import subprocess
from collections import namedtuple

from loguru import logger
import psutil


class SystemInfo:

    def __init__(self):
        self.__info = namedtuple('System', 'platform system ram cpu')

    @staticmethod
    def _define_cpu() -> str:
        if platform.system() == "Windows":
            return platform.processor()

        elif platform.system() == "Linux":
            command = "cat /proc/cpuinfo"
            all_info = subprocess.check_output(command, shell=True).decode().strip()
            for line in all_info.split("\n"):
                if "model name" in line:
                    return re.sub(".*model name.*:", "", line, 1)

    def get_sys_info(self) -> namedtuple:
        info = self.__info(platform=platform.platform(),
                           system=platform.system(),
                           ram=round(psutil.virtual_memory().total / 1e9, 2),
                           cpu=self._define_cpu() + ' x' + str(psutil.cpu_count()))

        return info

    @staticmethod
    def _get_disk_devices():
        return [dict(name=device.device,
                     fstype=device.fstype,
                     mountpoint=device.mountpoint) for device in psutil.disk_partitions() if 'rw' in device.opts]

    @staticmethod
    def _get_disk_usage(disks):
        return [dict(total=round(psutil.disk_usage(disk['mountpoint']).total / 1e9, 2),
                     used=round(psutil.disk_usage(disk['mountpoint']).used / 1e9, 2),
                     free=round(psutil.disk_usage(disk['mountpoint']).free / 1e9, 2),
                     percent=psutil.disk_usage(disk['mountpoint']).percent) for disk in disks]

    @staticmethod
    def _build_answer(disk_info, disk_usage):
        return [info | disk for info, disk in zip(disk_info, disk_usage)]

    def get_disk_info(self):
        disks = self._get_disk_devices()
        usages = self._get_disk_usage(disks)
        answer = self._build_answer(disks, usages)
        logger.debug(answer)
        return answer


if __name__ == '__main__':
    info_instance = SystemInfo()
    info_ = info_instance.get_sys_info()
    print(info_)
    print(info_instance.get_disk_info())
