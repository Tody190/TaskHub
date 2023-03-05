# -*- coding: utf-8 -*-
__author__ = "yangtao"

import sys

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

from . import task_ui, language
from . import publisher_ui
from . import task_info_ui
from . import version_ui


class Main_Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Main_Widget, self).__init__(parent)
        self.main_widget_settings = QtCore.QSettings("pipeline_tools", "task_hub")

        # 界面语言
        self.lan = language.lan()
        self.current_lan = self.lan.get_language()

        self.__setup_ui()
        self.__setup_connect()

    def __setup_ui(self):
        self.setMinimumSize(900, 600)
        # filter
        # project
        project_label = QtWidgets.QLabel(self.current_lan.project)
        self.project_combobox = QtWidgets.QComboBox()
        # self.project_combobox.setEditable(True)
        self.project_combobox.setMinimumWidth(80)
        # limit
        self.limit_label = QtWidgets.QLabel()
        self.limit_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        # status
        task_status_label = QtWidgets.QLabel(self.current_lan.status)
        self.task_status_combobox = QtWidgets.QComboBox()
        self.task_status_combobox.setMinimumWidth(120)
        # load button
        self.load_button = QtWidgets.QPushButton(self.current_lan.load)
        # filter layout
        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(project_label)
        filter_layout.addWidget(self.project_combobox)
        filter_layout.addWidget(task_status_label)
        filter_layout.addWidget(self.task_status_combobox)
        filter_layout.addWidget(self.limit_label)
        filter_layout.addWidget(self.limit_slider)
        filter_layout.addStretch(9)
        filter_layout.addWidget(self.load_button)

        # 任务列表
        self.task_listWidget = task_ui.Task_List_Widget()

        # 提交
        self.publisher_widget = publisher_ui.PublisherWidget()

        self.tools_tab_widget = QtWidgets.QTabWidget()
        self.task_info_widget = task_info_ui.Task_Info_Widget()
        self.tools_tab_widget.addTab(self.task_info_widget, self.current_lan.details)
        self.task_versions_widget = version_ui.Versions_Widget()
        self.tools_tab_widget.addTab(self.task_versions_widget, self.current_lan.versions)
        self.tools_tab_widget.addTab(self.publisher_widget, self.current_lan.submit)
        self.tools_tab_widget.setCurrentIndex(self.main_widget_settings.value("tools_current_tab_index", 0))

        # 内容布局
        self.info_splitter = QtWidgets.QSplitter()
        self.info_splitter.addWidget(self.task_listWidget)
        self.info_splitter.addWidget(self.tools_tab_widget)
        self.info_splitter.setStretchFactor(0, 4)
        self.info_splitter.setStretchFactor(1, 7)

        # 运行状态栏
        # 登录信息
        self.login_info_button = QtWidgets.QPushButton("xxxx | xxx")
        self.status_info_label = QtWidgets.QLabel("xxxx")
        self.status_info_label.setAlignment(QtCore.Qt.AlignCenter)
        status_bar_layout = QtWidgets.QHBoxLayout()
        status_bar_layout.addWidget(self.status_info_label)
        status_bar_layout.addStretch()
        status_bar_layout.addWidget(self.login_info_button)
        status_bar_layout.setMargin(0)
        status_bar_layout.setSpacing(0)
        status_bar_widget = QtWidgets.QWidget()
        status_bar_widget.setLayout(status_bar_layout)
        status_bar_widget.setMaximumHeight(30)

        # main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(filter_layout)
        main_layout.addWidget(self.info_splitter)
        main_layout.addWidget(status_bar_widget)

    def __setup_connect(self):
        self.limit_slider.valueChanged.connect(self.__set_slider_label)

        # 保存工具栏最后一次选中的页面
        def save_tab_index(index):
            self.main_widget_settings.setValue("tools_current_tab_index", index)

        self.tools_tab_widget.currentChanged.connect(save_tab_index)

    def __set_slider_label(self):
        value = self.limit_slider.value()
        if value == self.limit_slider.maximum():
            self.limit_label.setText(self.current_lan.limit_all)
        else:
            self.limit_label.setText(self.current_lan.limit % str(self.limit_slider.value()))

    def get_current_task_id(self):
        current_item = self.task_listWidget.item_list.currentItem()
        if current_item:
            return current_item.id

    def set_title(self, name, icon_path=None):
        self.setWindowTitle(name)
        if icon_path:
            self.setWindowIcon(QtGui.QIcon(icon_path))

    def get_current_filter_info(self):
        project = self.project_combobox.currentText()
        task_status = self.task_status_combobox.currentText()
        value = self.limit_slider.value()
        if value == self.limit_slider.maximum():
            limit_num = 0
        else:
            limit_num = int(self.limit_slider.value())
        return project, task_status, limit_num

    def set_last_show_range(self, mini_mum, max_num, position=None):
        self.limit_slider.setMinimum(mini_mum)
        self.limit_slider.setMaximum(max_num)
        if position:
            self.limit_slider.setValue(position)

    def set_login_button_info(self, login_name, user):
        if login_name == user:
            self.login_info_button.setText("%s" % login_name)
        else:
            self.login_info_button.setText("%s | %s" % (login_name, user))

    @QtCore.Slot(list)
    def set_project_combobox_items(self, items_name):
        self.project_combobox.clear()
        self.project_combobox.addItems(items_name)

    @QtCore.Slot(list)
    def set_task_status_combobox_items(self, items_name):
        self.task_status_combobox.clear()
        self.task_status_combobox.addItems(items_name)

    @QtCore.Slot(bool)
    def ui_enabled(self, status):
        self.project_combobox.setEnabled(status)
        self.task_status_combobox.setEnabled(status)
        self.limit_slider.setEnabled(status)
        #self.load_button.setEnabled(status)
        self.task_listWidget.setEnabled(status)
        self.tools_tab_widget.setEnabled(status)

    @QtCore.Slot(str)
    def set_status_text(self, text):
        self.status_info_label.setText("%s" % text)

    @QtCore.Slot()
    def clear_ui(self):
        self.task_listWidget.item_list.clear()
        self.task_listWidget.search_line.clear()
        self.task_versions_widget.clear_items()
        self.task_info_widget.clear_items()
        self.publisher_widget.clear_info()

    @QtCore.Slot(str, str)
    def messagebox(self, type, info):
        if type == "warning":
            QtWidgets.QMessageBox.warning(self, self.current_lan.submission_status, info, QtWidgets.QMessageBox.Ok)
        if type == "critical":
            QtWidgets.QMessageBox.critical(self, self.current_lan.submission_status, info, QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(self, self.current_lan.submission_status, info, QtWidgets.QMessageBox.Ok)


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    mw = Main_Widget()
    mw.show()
    sys.exit(app.exec_())
