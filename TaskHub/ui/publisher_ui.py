# -*- coding: utf-8 -*-
__author__ = "yangtao"

import os
import pprint

from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from . import base64_pic
from . import language
from .. import config


# class Drop_List(QtWidgets.QListWidget):
#     drop_file = QtCore.Signal(str)
#     def __init__(self, parent=None):
#         super(Drop_List, self).__init__(parent)
#         self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
#         self.setAcceptDrops(True)
#         self.setDragEnabled(True)
#         self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
#
#     def dragEnterEvent(self, event):
#         if event.mimeData().hasUrls():
#             event.acceptProposedAction()
#         else:
#             super(Drop_List, self).dragEnterEvent(event)
#
#     def dropEvent(self, event):
#         if event.mimeData().hasUrls():
#             for url_object in event.mimeData().urls():
#                 url_text = url_object.toLocalFile()
#                 self.drop_file.emit(url_text)
#         else:
#             super(Drop_List, self).dropEvent(event)
#
#
# class Creator_Widget(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super(Creator_Widget, self).__init__(parent)
#
#         # 界面语言
#         self.lan = language.lan()
#         self.current_lan = self.lan.get_language()
#
#         self.__init_ui()
#         self.__init_connect()
#
#     def __init_ui(self):
#         # 版本名
#         self.version_name_label = QtWidgets.QLabel(self.current_lan.version_name)
#         self.version_name_line_edit = QtWidgets.QLineEdit()
#         self.version_name_description_label = QtWidgets.QLabel(self.current_lan.name_description)
#         self.version_name_description = QtWidgets.QLineEdit()
#         self.version_name_description.setMaximumWidth(150)
#         version_name_layout = QtWidgets.QHBoxLayout()
#         version_name_layout.addWidget(self.version_name_line_edit)
#         version_name_layout.addWidget(self.version_name_description_label)
#         version_name_layout.addWidget(self.version_name_description)
#         # 上传框
#         self.uploaded_label = QtWidgets.QLabel(self.current_lan.upload)
#         self.preview_files = Drop_List()
#         self.preview_files.setMaximumHeight(60)
#         self.preview_files.setViewMode(QtWidgets.QListView.IconMode)
#         self.preview_files.setWrapping(False)
#         self.preview_files.setFlow(QtWidgets.QListView.LeftToRight)
#         self.preview_files.setHorizontalScrollMode(QtWidgets.QListWidget.ScrollPerPixel)
#         self.preview_files.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#         self.preview_files.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
#         # 清空上传按钮
#         self.clear_uploaded_button = QtWidgets.QPushButton(self.current_lan.clear)
#         self.uploaded_layout = QtWidgets.QVBoxLayout()
#         self.uploaded_layout.addWidget(self.preview_files)
#         self.uploaded_layout.addWidget(self.clear_uploaded_button)
#         self.uploaded_layout.setSpacing(0)
#         self.uploaded_layout.setMargin(0)
#         # 描述
#         self.description_label = QtWidgets.QLabel(self.current_lan.description)
#         self.description_text_edit = QtWidgets.QTextEdit()
#         # # 任务总用时
#         # self.time_logged_label = QtWidgets.QLabel("任务总用时")
#         # self.time_logged_num_label = QtWidgets.QLabel("0天")
#         # 当前版本用时
#         self.current_time_logged_label = QtWidgets.QLabel(self.current_lan.time_logged)
#         self.current_time_logged_spinbox = QtWidgets.QSpinBox()
#         self.current_time_logged_spinbox.setMaximumWidth(50)
#         self.current_time_logged_spinbox.setMaximum(999)
#         # 提交按钮
#         self.submit_button = QtWidgets.QPushButton(self.current_lan.submit)
#
#         grid_layout = QtWidgets.QGridLayout(self)
#         grid_layout.addWidget(self.version_name_label, 0, 0)
#         grid_layout.addLayout(version_name_layout, 0, 1)
#         grid_layout.addWidget(self.uploaded_label, 1, 0)
#         grid_layout.addLayout(self.uploaded_layout, 1, 1)
#         grid_layout.addWidget(self.description_label, 2, 0)
#         grid_layout.addWidget(self.description_text_edit, 3, 1)
#         grid_layout.addWidget(self.description_label, 3, 0)
#         grid_layout.addWidget(self.description_text_edit, 3, 1)
#         grid_layout.addWidget(self.current_time_logged_label, 4, 0)
#         grid_layout.addWidget(self.current_time_logged_spinbox, 4, 1)
#         grid_layout.addWidget(self.submit_button, 5, 0, 1, 0)
#
#     def __init_connect(self):
#         self.preview_files.drop_file.connect(self.replace_uploaded_item)
#         self.clear_uploaded_button.clicked.connect(self.preview_files.clear)
#         #self.submit_button.clicked.connect(self.get_current_edit_info)
#
#     def clear_info(self):
#         self.version_name_line_edit.clear()
#         self.version_name_description.clear()
#         self.preview_files.clear()
#         self.description_text_edit.clear()
#         self.current_time_logged_spinbox.setValue(0)
#
#     def clear_version_name(self):
#         self.version_name_line_edit.clear()
#         self.version_name_description.clear()
#
#     def add_uploaded_item(self, path):
#         img_icon = QtGui.QIcon()
#         img_icon.addFile(path)
#         item = QtWidgets.QListWidgetItem(img_icon, os.path.basename(path))
#         item.file = path
#         self.preview_files.addItem(item)
#
#     def replace_uploaded_item(self, path):
#         self.preview_files.clear()
#         self.add_uploaded_item(path)
#
#     def get_current_edit_info(self):
#         current_edit_info = {"version_name": None,
#                              "upload_files": [],
#                              "description": None,
#                              "logged_time": 0}
#
#         current_edit_info["version_name"] = self.version_name_line_edit.show_name()
#
#         preview_list_count = self.preview_files.count()
#         for item in range(preview_list_count):
#             current_edit_info["upload_files"].append(self.preview_files.item(item).file)
#
#         current_edit_info["description"] = self.description_text_edit.toPlainText()
#         current_edit_info["logged_time"] = self.current_time_logged_spinbox.value()
#
#         return current_edit_info
#
#     @QtCore.Slot(str, str)
#     def messagebox(self, type, info):
#         if type == "warning":
#             QtWidgets.QMessageBox.warning(self, self.current_lan.submission_status, info, QtWidgets.QMessageBox.Ok)
#         if type == "critical":
#             QtWidgets.QMessageBox.critical(self, self.current_lan.submission_status, info, QtWidgets.QMessageBox.Ok)
#         else:
#             QtWidgets.QMessageBox.information(self, self.current_lan.submission_status, info, QtWidgets.QMessageBox.Ok)


class PublishBoxWidgetItem(QtWidgets.QWidget):
    def __init__(self, name_type, file_name, show_name):
        super(PublishBoxWidgetItem, self).__init__()
        self.name_type = name_type
        self.file_name = file_name
        self.show_name = show_name

        self.__setup_ui()
        self.set_show_info()

    def __setup_ui(self):
        self.text_label = QtWidgets.QLabel()
        self.img_label = QtWidgets.QLabel()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(self.img_label)
        main_layout.addStretch()
        main_layout.addWidget(self.text_label)
        self.setLayout(main_layout)

    def __get_icon(self, path):
        # 通过格式显示图标
        if os.path.isfile(path):
            ext = os.path.splitext(os.path.basename(path))[-1].lower()
        else:
            return base64_pic.get_res("folder.ico")
        if ext in config.img:
            return path
        elif ext in config.video:
            return base64_pic.get_res("video.ico")
        else:
            return base64_pic.get_res("file.ico")

    def set_show_info(self):
        # 添加标题
        self.text_label.setText(self.show_name)
        self.widget_width = self.text_label.fontMetrics().width(self.show_name)
        if self.widget_width < 64:
            self.widget_width = 64
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)

        # 添加图片
        img_pix = QtGui.QPixmap(self.__get_icon(self.file_name))
        # 宽度和文字宽度相同，高度和图标最大高度相同，图片大小自适应
        img_pix = img_pix.scaled(self.widget_width, img_pix.size().height(), QtCore.Qt.KeepAspectRatio,
                                 QtCore.Qt.SmoothTransformation)
        self.img_label.setMargin(0)
        self.img_label.setAlignment(QtCore.Qt.AlignCenter)
        self.img_label.setPixmap(img_pix)


class RenameWidget(QtWidgets.QDialog):
    def __init__(self, parent=None, src_name=None):
        super(RenameWidget, self).__init__(parent)
        self.setWindowTitle("重命名")
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.line_edit = QtWidgets.QLineEdit()
        if src_name:
            self.line_edit.setText(src_name)
            src_name_width = self.fontMetrics().width(src_name)
            self.line_edit.setMinimumWidth(src_name_width + 10)

        ok_button = QtWidgets.QPushButton("确定")
        ok_button.setMinimumHeight(35)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.line_edit)
        main_layout.addWidget(ok_button)
        self.setLayout(main_layout)

        ok_button.clicked.connect(self.close)

    def get_new_name(self):
        return self.line_edit.text()


class PublishBox(QtWidgets.QWidget):
    def __init__(self):
        super(PublishBox, self).__init__()
        # self.__items_path = []  # 用于判断是否重复添加多个项
        self.__items_widget = []  # 所有 item 对应的 widget 合集
        self.__single_file = False
        self.__only_file = False
        self.show_name_hook = None  # 用于重命名显示名称的 hook

        self.__setup_ui()

    def __setup_ui(self):
        self.setAcceptDrops(True)
        # self.setMaximumHeight(100)
        self.setContextMenuPolicy(QtGui.Qt.CustomContextMenu)  # 自定义右键菜单
        # 提交列表
        self.upload_list = QtWidgets.QListWidget()
        self.upload_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.upload_list.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)

        # self.upload_list.setViewMode(QtWidgets.QListView.IconMode)
        self.upload_list.setFlow(QtWidgets.QListView.LeftToRight)
        # self.upload_list.setWrapping(True)
        self.upload_list.setHorizontalScrollMode(QtWidgets.QListWidget.ScrollPerPixel)
        # self.upload_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.upload_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)  #横向滑条
        # 清空按钮
        # self.clear_button = QtWidgets.QPushButton(u"清空")
        # 右键菜单
        self.context_menu = QtWidgets.QMenu()

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setMargin(0)
        self.main_layout.addWidget(self.upload_list)
        # self.main_layout.addWidget(self.clear_button)

        # connect
        # self.clear_button.clicked.connect(self.clear_list)
        self.customContextMenuRequested.connect(self.__context_menu_activate)

    def __context_menu_activate(self):
        self.context_menu.clear()
        # 清空按钮
        clear_action = self.context_menu.addAction("清空")
        clear_action.triggered.connect(self.clear_list)
        # 重命名
        rename_action = self.context_menu.addAction("重命名")
        rename_action.triggered.connect(self.rename_current_item)
        self.context_menu.exec_(QtGui.QCursor.pos())

    def rename_current_item(self):
        item = self.upload_list.currentItem()  # 获取当前选中的项
        if item:
            item_widget = self.upload_list.itemWidget(item)
            show_name = item_widget.show_name  # 显示的名
            # 显示重命名UI
            RW = RenameWidget(self, src_name=show_name)
            RW.exec_()
            # 更改显示的名
            item_widget.show_name = RW.get_new_name()
            item_widget.set_show_info()
            items_info = self.get_items_info().copy()
            self.clear_list()
            self.__add_items_from_items_info(items_info)
        else:
            QtWidgets.QMessageBox.warning(self,
                                          u"注意",
                                          u"请选中一项再执行",
                                          QtWidgets.QMessageBox.Ok)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super(PublishBox, self).dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url_object in event.mimeData().urls():
                url_text = url_object.toLocalFile()
                self.add_item(url_text)
        else:
            super(PublishBox, self).dropEvent(event)

    def clear_list(self):
        self.__items_widget.clear()
        self.upload_list.clear()

    def add_item(self, file_name):
        """

        :param file_name:
        :return:
        """
        # 只能提交文件
        if self.__only_file:
            if not os.path.isfile(file_name):
                return

        # 只能提交一个文件
        if self.__single_file:
            self.clear_list()

        # 添加ui
        items_info = self.get_items_info()  # 获取当前项
        # 防止重复添加
        if file_name in [info["file_name"] for info in items_info]:
            return
        items_info.append({"file_name": file_name,
                           "show_name": os.path.basename(file_name)})

        # 通过 hook 重命名
        if self.show_name_hook:
            items_info = self.show_name_hook(items_info)

        self.clear_list()
        self.__add_items_from_items_info(items_info)

    def __add_items_from_items_info(self, items_info):
        for info in items_info:
            publishbox_widget = PublishBoxWidgetItem(info["name_type"], info["file_name"], info["show_name"])
            publishbox_item = QtWidgets.QListWidgetItem()
            publishbox_item.setToolTip(info["file_name"])
            publishbox_item.setSizeHint(QtCore.QSize(publishbox_widget.widget_width + 28, 80))
            self.upload_list.addItem(publishbox_item)
            self.upload_list.setItemWidget(publishbox_item, publishbox_widget)

            self.__items_widget.append(publishbox_widget)

    def get_items_info(self):
        """

        :return: [{file_name:file_name,
                   show_name: show_name}]
        """
        items_info = []
        for w in self.__items_widget:
            items_info.append({"file_name": w.file_name,
                               "show_name": w.show_name,
                               "name_type":w.name_type})
        return items_info

    def set_single_file(self, _bool):
        # 只允许添加一个文件
        self.__single_file = _bool

    def only_file(self, _bool):
        # 只允许文件，不允许文件夹
        self.__only_file = _bool


class PublisherWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PublisherWidget, self).__init__(parent)

        # 界面语言
        self.lan = language.lan()
        self.current_lan = self.lan.get_language()

        self.step = None
        self.version_name = None

        self.__setup_ui()

    def __setup_ui(self):
        # 版本名
        self.version_name_label = QtWidgets.QLabel(self.current_lan.version_name)
        self.version_name_line = QtWidgets.QLabel("Version Name")
        self.version_name_line.setStyleSheet("font-weight:bold;font-size:15px;color:#5B5B5B")
        self.version_label = QtWidgets.QLabel("[VER]")
        self.version_label.setStyleSheet("font-weight:bold;font-size:30px;color:#5B5B5B")

        self.version_name_layout = QtWidgets.QHBoxLayout()
        self.version_name_layout.addWidget(self.version_name_line)
        self.version_name_layout.addStretch()
        self.version_name_layout.addWidget(self.version_label)
        # # 上传预览文件框
        # self.preview_box_label = QtWidgets.QLabel(self.current_lan.upload)
        # self.preview_box = PublishBox()
        # self.preview_box.only_file(True)
        # # 清空上传按钮
        # # self.clear_uploaded_button = QtWidgets.QPushButton(self.current_lan.clear)
        # # self.uploaded_layout = QtWidgets.QVBoxLayout()
        # # self.uploaded_layout.addWidget(self.preview_files)
        # # self.uploaded_layout.addWidget(self.clear_uploaded_button)
        # # self.uploaded_layout.setSpacing(0)
        # # self.uploaded_layout.setMargin(0)

        # 文件提交
        self.publish_box_label = QtWidgets.QLabel(self.current_lan.files_publish)
        self.publish_box = PublishBox()

        # 描述
        self.description_label = QtWidgets.QLabel(self.current_lan.description)
        self.description_text_edit = QtWidgets.QTextEdit()

        # 提交按钮
        self.submit_button = QtWidgets.QPushButton(self.current_lan.submit)
        self.submit_button.setStyleSheet("font-weight:bold;font-size:25px;color:#5B5B5B")
        self.submit_button.setMinimumHeight(50)

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(self.version_name_label, 0, 0)
        grid_layout.addLayout(self.version_name_layout, 0, 1)
        # grid_layout.addWidget(self.preview_box_label, 1, 0)
        # grid_layout.addWidget(self.preview_box, 1, 1)
        grid_layout.addWidget(self.publish_box_label, 2, 0)
        grid_layout.addWidget(self.publish_box, 2, 1)
        grid_layout.addWidget(self.description_label, 3, 0)
        grid_layout.addWidget(self.description_text_edit, 3, 1)
        grid_layout.addWidget(self.submit_button, 5, 0, 1, 0)

    def set_version_name(self, name):
        self.version_name = name
        self.version_name_line.setText(name)

    def set_version_label(self, name):
        self.step = name
        self.version_label.setText("[%s]" % name)

    def get_info(self):
        current_edit_info = {"version_name": self.version_name_line.text(),
                             # "preview_files": self.preview_box.get_items_info(),  # 获取预览文件
                             "publish_files": self.publish_box.get_items_info(),  # 获取提交文件
                             "description": self.description_text_edit.toPlainText()}

        return current_edit_info

    def clear_info(self):
        self.version_name_line.clear()
        # self.preview_box.clear_list()
        self.publish_box.clear_list()

    def clear_version_name(self):
        self.version_name_line.clear()


class ADARChooseWindow(QtWidgets.QDialog):
    def __init__(self):
        self.choose = None

        self.__setup_ui()
        self.__connect()

    def __setup_ui(self):
        self.ar_button = QtWidgets.QPushButton("assemblyReference")
        self.ad_button = QtWidgets.QPushButton("assemblyDefinition")

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addWidget(self.ad_button)
        self.main_layout.addWidget(self.ar_button)

    def set_choose(self, value):
        self.choose = value

    def get_choose(self):
        return self.choose

    def __connect(self):
        self.ad_button.clicked.connect(self.set_choose("assemblyDefinition"))
        self.ar_button.clicked.connect(self.set_choose("assemblyReference"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication()
    cw = PublisherWidget()
    cw.show()
    sys.exit(app.exec_())
