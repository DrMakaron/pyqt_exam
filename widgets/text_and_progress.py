from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class TextAndProgress(QtWidgets.QWidget):
    """
    Виджет, объединяющий в себе QProgreeBar и QLabel
    """
    def __init__(self, text, progress_value):
        super().__init__()

        self.__text = text
        self.__progress = progress_value

    def get_txt_progress_widget(self):
        disk_usage_progress = QtWidgets.QProgressBar()
        disk_usage_progress.setValue(self.__progress)
        disk_usage_label = QtWidgets.QLabel()
        disk_usage_label.setText(self.__text)
        disk_usage_layout = QtWidgets.QHBoxLayout()
        disk_usage_layout.addWidget(disk_usage_label)
        disk_usage_layout.addWidget(disk_usage_progress)
        disk_usage_layout.setAlignment(Qt.AlignRight)
        self.setLayout(disk_usage_layout)

        return self
