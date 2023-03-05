# -*- coding: utf-8 -*-
__author__ = "yangtao"

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from . import language


class TaskListItemWidget(QtWidgets.QWidget):
    def __init__(self, title, subtitle, info):
        super(TaskListItemWidget, self).__init__()
        self.title = title
        self.subtitle = subtitle
        self.info = info

        self.__setup_ui()

    def __setup_ui(self):
        title_info = "<b><font size=\"10\" color=\"#5B5B5B\">%s</font></b>" % self.title
        title_info += "<font size=\"3\" color=\"#5B5B5B\">  %s</font>" % self.subtitle
        title_label = QtWidgets.QLabel(title_info)
        subtitle_label = QtWidgets.QLabel("<font size=\"3\" color=\"#ADADAD\">%s</font>" % self.info)
        self.item_layout = QtWidgets.QVBoxLayout()
        self.item_layout.addWidget(title_label)
        self.item_layout.addWidget(subtitle_label)
        self.setLayout(self.item_layout)


class Task_List_Widget(QtWidgets.QWidget):
    action_clicked = QtCore.Signal()
    def __init__(self, parent=None):
        super(Task_List_Widget, self).__init__(parent=parent)

        # 界面语言
        self.lan = language.lan()
        self.current_lan = self.lan.get_language()

        # 添加搜索框
        self.search_line = QtWidgets.QLineEdit()
        self.search_line.setPlaceholderText(self.current_lan.search)

        # 添加任务列表控件
        self.item_list = QtWidgets.QListWidget()
        self.item_list.setContextMenuPolicy(QtGui.Qt.CustomContextMenu)
        self.item_list.verticalScrollBar().setStyleSheet("QScrollBar{width:10px;}")

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setMargin(0)
        main_layout.setSpacing(3)

        main_layout.addWidget(self.search_line)
        main_layout.addWidget(self.item_list)
        # 设置滑块宽度

        # 连接搜索
        self.search_line.textChanged.connect(self.filter_item)
        # 连接右键菜单
        self.item_list.customContextMenuRequested.connect(self.__context_menu)
        # 菜单
        self.context_menu = QtWidgets.QMenu()
        # 自定义菜单列表
        self.__context_menu_items = []

    def filter_item(self):
        search_line_text = self.search_line.text()
        for i in range(self.item_list.count()):
            item = self.item_list.item(i)
            if search_line_text in item.title:
                item.setHidden(False)
            else:
                item.setHidden(True)

    def set_task_item(self, title, subtitle, info, id):
        task_table_item = QtWidgets.QListWidgetItem()

        task_table_item.setSizeHint(QtCore.QSize(200, 90))
        task_table_item.id = id
        task_table_item.title = title

        info = " | ".join(info)
        task_item_widget = TaskListItemWidget(title, subtitle, info)

        self.item_list.addItem(task_table_item)
        self.item_list.setItemWidget(task_table_item, task_item_widget)

    def add_menu(self, name, _func, index=None):
        """
        添加右键菜单
        :param name: 菜单名字
        :param _func: 菜单要执行的 func
        :param index: 菜单位置
        :return:
        """
        if index:
            self.__context_menu_items.insert(index, (name, _func))
        else:
            self.__context_menu_items.append((name, _func))

    def clear_menu(self):
        self.__context_menu_items = []

    def __context_menu(self):
        if self.__context_menu_items:
            self.context_menu.clear()
            for m in self.__context_menu_items:
                action = self.context_menu.addAction(m[0])  # 菜单项名
                action.triggered.connect(m[1])   # 菜单项相应的函数

            self.context_menu.exec_(QtGui.QCursor.pos())
