import sys

from PyQt5 import QtWidgets

from controller import Controller
from gui import MainGui


def main():
    app = QtWidgets.QApplication(sys.argv)

    # instances
    controller = Controller()
    window = MainGui()

    # connect signals
    window.tab_number_signal.connect(controller.hand_request)
    controller.sys_info_signal.connect(window.show_sys_info)
    controller.fs_signal.connect(window.show_fs_info)

    window.show()

    app.exec()


if __name__ == '__main__':
    main()
