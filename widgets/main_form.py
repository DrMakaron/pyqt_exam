# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(933, 672)
        Form.setStyleSheet("background-color: #30393d;")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tabWidget.setFont(font)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setStyleSheet("QTabWidget::pane\n"
"{\n"
"    top: -8px;\n"
"    background-color: white;\n"
"    border: None;\n"
"}\n"
"\n"
"\n"
"QTabWidget::tab-bar\n"
"{\n"
"    alignment: center;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"     \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.83, x2:0, y2:0.915, stop:0 rgba(48, 57, 61, 255), stop:1 rgba(2, 163, 250, 255));\n"
"    color: white;\n"
"}\n"
" \n"
"\n"
"QTabBar::tab:!selected {\n"
"    background:#30393d;\n"
"    color: white;\n"
"    margin-bottom: 0px;\n"
"    margin-left: 13px;\n"
"    margin-right: 13px;\n"
"}\n"
"")
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.fs_table = QtWidgets.QTableWidget(self.tab_3)
        self.fs_table.setObjectName("fs_table")
        self.fs_table.setColumnCount(6)
        self.fs_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.fs_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.fs_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.fs_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.fs_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.fs_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.fs_table.setHorizontalHeaderItem(5, item)
        self.horizontalLayout_3.addWidget(self.fs_table)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.info = QtWidgets.QPlainTextEdit(self.tab_4)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.info.setFont(font)
        self.info.setStyleSheet("color: white;\n"
"border: none;")
        self.info.setReadOnly(True)
        self.info.setObjectName("info")
        self.horizontalLayout_2.addWidget(self.info)
        self.tabWidget.addTab(self.tab_4, "")
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Processes"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Resources"))
        item = self.fs_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Device"))
        item = self.fs_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Directory"))
        item = self.fs_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Type"))
        item = self.fs_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Total"))
        item = self.fs_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Free"))
        item = self.fs_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Used"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "File system"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Form", "System info"))
