# -*- coding: utf-8 -*-
__author__ = "yangtao"
__version__ = '5.0'

import pprint
import shutil
import sys
import os
import time
from pathlib import Path
import threading as td
import multiprocessing as mp
import datetime

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
# pyinstaller 打包引用模块

from . import welcome
from . import config
from .ui import base64_pic, language
from .ui import main_ui
from .ui import login_dialog
from .core import secrets_tool
from .core import database
from .core import util
from .core import name_center
from .core import assembly_builder


class Signal_Wrapper(QtCore.QObject):
    set_projects = QtCore.Signal(list)
    set_current_project = QtCore.Signal(str)
    set_task_status = QtCore.Signal(list)
    set_current_task_status = QtCore.Signal(str)
    ui_enabled = QtCore.Signal(bool)
    publish_ui_enabled = QtCore.Signal(bool)
    set_status_text = QtCore.Signal(str)
    set_task_item = QtCore.Signal(str, str, list, int)
    clear_ui = QtCore.Signal()
    uploaded_status = QtCore.Signal(str, str)
    set_version_ui_info = QtCore.Signal(list, list)
    set_version_ui_heads = QtCore.Signal(list)
    set_version_ui_item = QtCore.Signal(int, datetime.datetime, list)
    set_task_ui_info = QtCore.Signal(dict)

    def __init__(self):
        super(Signal_Wrapper, self).__init__()


class Task_Hub_Setting():
    def __init__(self):
        self.settings = QtCore.QSettings("pipeline_tools", "task_hub")

    def save_current_project(self, current_project):
        self.settings.setValue("current_project", current_project)

    def get_save_project(self):
        return self.settings.value("current_project", None)

    def save_currrent_task_status(self, current_status):
        self.settings.setValue("current_task_status", current_status)

    def get_save_task_status(self):
        return self.settings.value("current_task_status", None)

    def save_login_info(self, sgurl, logname, password, user, local_storage):
        self.settings.setValue("sgurl", sgurl)
        self.settings.setValue("logname", logname)
        self.settings.setValue("password", secrets_tool.encrypt(password))
        self.settings.setValue("user", user)
        self.settings.setValue("localstorage", local_storage)

    def get_login_info(self):
        sgurl = self.settings.value("sgurl", None)
        logname = self.settings.value("logname", None)
        password = self.settings.value("password", None)
        if password:
            try:
                password = secrets_tool.decrypt(password)
            except:
                password = None
        user = self.settings.value("user", None)
        local_storage = self.settings.value("localstorage", None)
        return sgurl, logname, password, user, local_storage

    def save_slider_position(self, num):
        self.settings.setValue("slider_position", int(num))

    def get_slider_position(self):
        return self.settings.value("slider_position", 10)

    def save_current_language(self, language_name):
        self.settings.setValue("language", language_name)

    def get_current_language(self):
        self.settings.value("language", None)


class Main():
    def __init__(self):
        super(Main, self).__init__()
        # 实例化自定义信号
        self.db = None
        self.signal_wrapper = Signal_Wrapper()
        # 实例化设置保存
        self.settings = Task_Hub_Setting()
        # 获取资源路径
        self.res_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])).replace('\\', '/'), "res")
        self.login_dialog_icon = base64_pic.get_res("login.ico")
        self.main_widget_icon = base64_pic.get_res("task.ico")

        # 实例化启动画面
        self.welcome_screen = QtWidgets.QSplashScreen()
        self.welcome_screen.setPixmap(QtGui.QPixmap(base64_pic.get_res("welcome.jpg")))

        # 获取当前语言
        self.lan = language.lan()
        self.current_lan = self.lan.get_language()

        # 实例化登录框
        self.login_dialog = login_dialog.Dialog()
        # 初始化语言选项
        self.login_dialog.set_language_box(self.lan.language_list, self.lan.get_language_name())
        self.login_dialog.set_title(self.current_lan.login_title, self.login_dialog_icon)

        # 实例化主窗口
        self.main_widget = main_ui.Main_Widget()
        # 设置 "显示最近" 的最大最小值
        self.main_widget.set_last_show_range(1, 100, self.settings.get_slider_position())
        # 设置图标和名称
        self.main_widget.set_title("Task Hub %s" % __version__, self.main_widget_icon)

        # 初始化信号和槽的连接
        self.__setup_connect()

        # 当前版本文件文件名
        self.version_name = None

        # 命名字段的映射表
        self.name_data_map = {}

        # 为提交框添加重命名钩子
        # self.main_widget.publisher_widget.preview_box.show_name_hook = self.__show_name_hook
        self.main_widget.publisher_widget.publish_box.show_name_hook = self.__show_name_hook

        # 任务项切换状态, True 为正在切换， False 为切换完毕
        self.task_switching = True

    def __setup_connect(self):
        # 筛选栏控件
        # 启用关闭UI
        self.signal_wrapper.ui_enabled.connect(self.main_widget.ui_enabled)
        # 启用关闭提交UI
        self.signal_wrapper.publish_ui_enabled.connect(self.main_widget.publisher_widget.setEnabled)
        # 项目改变保存当前项目名
        self.main_widget.project_combobox.activated[str].connect(self.settings.save_current_project)
        # 筛选项改变重置任务项
        # self.main_widget.project_combobox.activated.connect(lambda: self.new_thread_run(self.init_filter_data))
        self.main_widget.project_combobox.activated.connect(self.clear_and_wait_load)
        self.main_widget.task_status_combobox.activated.connect(self.clear_and_wait_load)
        self.main_widget.limit_slider.valueChanged.connect(self.clear_and_wait_load)
        # 添加项目
        self.signal_wrapper.set_projects.connect(self.main_widget.set_project_combobox_items)
        # 设置当前项目
        self.signal_wrapper.set_current_project.connect(self.main_widget.project_combobox.setCurrentText)
        # 状态改变保存当前状态
        self.main_widget.task_status_combobox.activated[str].connect(self.settings.save_currrent_task_status)
        # 添加状态
        self.signal_wrapper.set_task_status.connect(self.main_widget.set_task_status_combobox_items)
        # 设置任务状态
        self.signal_wrapper.set_current_task_status.connect(self.main_widget.task_status_combobox.setCurrentText)
        # 保存滑条当前值
        self.main_widget.limit_slider.sliderReleased.connect(lambda: self.settings.save_slider_position(
            self.main_widget.limit_slider.value()))
        # 加载按钮
        self.main_widget.load_button.clicked.connect(lambda: self.new_thread_run(self.set_task_items))
        # 设置任务
        self.signal_wrapper.set_task_item.connect(self.main_widget.task_listWidget.set_task_item)
        # 清空 UI
        self.signal_wrapper.clear_ui.connect(self.main_widget.clear_ui)
        # 重新登录
        self.main_widget.login_info_button.clicked.connect(lambda: self.run(reset=True))
        # 设置底部状态栏
        self.signal_wrapper.set_status_text.connect(self.main_widget.set_status_text)
        # 任务切换
        self.main_widget.task_listWidget.item_list.currentItemChanged.connect(
            lambda: self.new_thread_run(self.task_selected))
        # 提交
        self.main_widget.publisher_widget.submit_button.clicked.connect(
            lambda: self.new_thread_run(self.publish_version))
        # 提交状态信息提示框
        self.signal_wrapper.uploaded_status.connect(self.main_widget.messagebox)
        # 向任务详情页添加信息
        self.signal_wrapper.set_task_ui_info.connect(self.main_widget.task_info_widget.add_items)
        # 向版本详情页面添加信息
        self.signal_wrapper.set_version_ui_info.connect(self.main_widget.task_versions_widget.add_items)
        # 向版本详情页面添加头
        self.signal_wrapper.set_version_ui_heads.connect(self.main_widget.task_versions_widget.set_head_labels)
        # 向版本详情页面添加一项
        self.signal_wrapper.set_version_ui_item.connect(self.main_widget.task_versions_widget.add_item)
        # 选中版本详情某一项
        self.main_widget.task_versions_widget.itemClicked.connect(self.select_version_item)
        # # 删除版本
        # self.main_widget.task_versions_widget.del_button.clicked.connect(lambda: self.new_thread_run(self.del_version))
        # 设置当前语言
        self.login_dialog.language_combobox.activated[str].connect(self.switch_language)

        # 打开 wrok 目录
        self.main_widget.task_listWidget.add_menu("打开工作目录", self.open_work)
        # 打开 publish 目录
        self.main_widget.task_listWidget.add_menu("打开提交目录", self.open_publish)
        # 跳转到 shotgun
        self.main_widget.task_listWidget.add_menu("跳转到 ShotGrid", self.jump_to_shotgun)
        # 刷新
        self.main_widget.task_listWidget.add_menu("刷新", lambda: self.new_thread_run(self.set_task_items))

    def clear_and_wait_load(self):
        self.signal_wrapper.clear_ui.emit()
        self.signal_wrapper.set_status_text.emit("筛选项已改变，请点击 [加载] 按钮重新加载")

    def __show_name_hook(self, items_info):
        """
        :param item_widget_list:
        :param current_item_widget:
        :return:
        """
        ext_map = {}
        for info in items_info:
            ext = Path(info["file_name"]).suffix.lower()
            if ext in ext_map.keys():
                ext_map[ext].append(info)
            else:
                ext_map[ext] = [info]

        new_item_info = []
        for ext in ext_map.keys():
            for i, info in enumerate(ext_map[ext]):
                self.name.ext = Path(info["file_name"]).suffix.lower()
                info["show_name"] = self.name.name()
                info["name_type"] = self.name.ext.split(".")[-1]
                # 为多个文件添加编号
                if len(ext_map[ext]) < 2:
                    new_item_info.append(info)
                else:
                    if i > 0:
                        info["name_type"] += str(i)
                    else:
                        info["name_type"]
                    new_item_info.append(info)
        return new_item_info

    def open_publish(self):
        while self.task_switching:
            time.sleep(0.5)
        os.startfile(Path(self.name.publish_path()).parent)

    def open_work(self):
        while self.task_switching:
            time.sleep(0.5)

        items = self.main_widget.task_listWidget.item_list.selectedItems()
        if items:
            # 创建 work 文件夹
            work_path = Path(self.name.work_path())
            work_path.mkdir(parents=True, exist_ok=True)
            os.startfile(work_path)
        else:
            QtWidgets.QMessageBox.warning(self.main_widget,
                                          u"警告",
                                          u"你得先选中一个任务啊",
                                          QtWidgets.QMessageBox.Ok)

    def jump_to_shotgun(self):
        while self.task_switching:
            time.sleep(0.5)

        items = self.main_widget.task_listWidget.item_list.selectedItems()
        if items:
            task_id = items[0].id
            sgurl, _, _, _, _ = self.settings.get_login_info()
            task_url = config.sg_task_url.format(sgurl=sgurl, id=str(task_id))
            os.startfile(task_url)
            print("jump to %s" % task_url)
        else:
            QtWidgets.QMessageBox.warning(self.main_widget,
                                          u"注意",
                                          u"请选中一个任务再执行",
                                          QtWidgets.QMessageBox.Ok)

    def switch_language(self, language_name):
        self.settings.save_current_language(language_name)
        self.login_dialog.done(0)
        new_ui = mp.Process(target=show, args=(True,))
        new_ui.start()

    def new_thread_run(self, target):
        tr = td.Thread(target=target)
        tr.start()

    def del_version(self):
        selected_items = self.main_widget.task_versions_widget.selectedItems()
        if selected_items:
            db = self.__get_db()
            selected_item_id = selected_items[0].id
            self.signal_wrapper.set_status_text.emit(self.current_lan.del_version % (str(selected_item_id)))
            result = db.del_version(selected_item_id)
            if not result:
                self.signal_wrapper.set_status_text.emit(self.current_lan.failed_delete)
            else:
                self.task_selected(db=db)

    def select_version_item(self, item):
        created_time = item.created_time.replace(tzinfo=None)
        if not created_time:
            self.main_widget.task_versions_widget.del_button.setVisible(False)

        current_time = datetime.datetime.now()
        timedelta = current_time - created_time
        max_timedelta = datetime.timedelta(hours=config.version_del_time_hours)
        if timedelta > max_timedelta:
            self.main_widget.task_versions_widget.del_button.setVisible(False)
        else:
            self.main_widget.task_versions_widget.del_button.setVisible(True)

    def __copy_file(self, src_file, dst_file):
        # 创建提交目录
        dst_file.parent.mkdir(parents=True, exist_ok=True)
        if str(src_file) == str(dst_file):  # 如果文件已经在提交目录下就不拷贝
            rsl = str(src_file)
        else:
            if src_file.is_file():
                rsl = shutil.copy2(src_file, dst_file)
            elif src_file.is_dir():
                rsl = shutil.copytree(src_file, dst_file)

        # self.signal_wrapper.set_status_text.emit("publish_files: {}".format(rsl))
        rsl = (r"%s" % rsl).replace("\\", "/")
        print("publish_files: {}".format(rsl))
        return rsl

    def publish_version(self):
        self.signal_wrapper.ui_enabled.emit(False)
        # 获取版本关联信息
        task_id = self.main_widget.get_current_task_id()
        if task_id:
            # 提交
            self.signal_wrapper.set_status_text.emit(self.current_lan.sub_task % task_id)

            upload_info = self.main_widget.publisher_widget.get_info()
            # 创建版本
            self.db = self.__get_db()
            version_entity = self.db.create_version(task_id,
                                                    version_name=upload_info["version_name"],
                                                    description=upload_info["description"])

            # 提交文件
            version_image = None
            version_mov = None
            for src_file_info in upload_info["publish_files"]:
                src_file = Path(src_file_info["file_name"])
                # 提交文件
                if src_file.is_file():
                    self.name.ext = src_file.suffix.lower()
                    # 添加版本图片
                    if not version_image and self.name.ext in config.img:
                        self.db.sg.upload(version_entity["type"],
                                          version_entity["id"],
                                          src_file,
                                          field_name="image")
                        version_image = src_file
                    # 添加版本视频
                    if not version_mov and self.name.ext in config.video:
                        self.db.sg.upload(version_entity["type"],
                                          version_entity["id"],
                                          src_file,
                                          field_name="sg_uploaded_movie")
                        version_mov = src_file
                # 提交文件夹
                elif src_file.is_dir():
                    # 文件夹的后缀是 .grp
                    self.name.ext = ".grp"

                # 获取提交路径, 无版本号路径和有版本号路径
                pub_path_no_version = self.name.publish_path_no_version()

                # 提交无版本号版本
                no_version_pub_file = self.__copy_file(src_file, Path(pub_path_no_version) /
                                                       src_file_info["name_type"] /
                                                       Path(src_file_info["show_name"]))
                # 创建 file entity
                self.db.create_published_file(pub_file=no_version_pub_file,
                                              entity_name=self.name.no_version_name() +
                                                          ".%s" % src_file_info["name_type"],
                                              version=version_entity)

                pub_path_has_version = self.name.publish_path()
                # 提交有版本号版本
                has_version_pub_file = self.__copy_file(src_file, Path(pub_path_has_version) /
                                                        src_file_info["name_type"] /
                                                        Path(src_file_info["show_name"]))
                self.db.create_published_file(pub_file=has_version_pub_file,
                                              entity_name=self.name.version_name() +
                                                          ".%s" % src_file_info["name_type"],
                                              version=version_entity)

                # 提交 assembly definition 文件
                assembly_definition = assembly_builder.Definition()
                assembly_definition.definition_file = self.name.assembly_definition()
                assembly_definition.name = self.name_data_map["code_name"]
                assembly_definition.step_name = self.name_data_map["step"]
                assembly_definition.task_name = self.name_data_map["task_name"]
                assembly_definition.file_type = src_file_info["name_type"]
                assembly_definition.data = no_version_pub_file
                assembly_definition.build()

                self.db.create_published_file(pub_file=self.name.assembly_definition(),
                                              entity_name="%s.assemblyDefinition" % self.name_data_map["code_name"],
                                              version=version_entity)

            self.signal_wrapper.uploaded_status.emit("information", "完成")
        else:
            self.signal_wrapper.set_status_text.emit(self.current_lan.select_task_submit)

        self.task_selected(db=self.db)
        self.signal_wrapper.ui_enabled.emit(True)

    def task_selected(self, db=None):
        self.main_widget.publisher_widget.publish_box.clear_list()
        self.task_switching = True
        self.signal_wrapper.publish_ui_enabled.emit(False)
        # # 隐藏删除按钮
        # self.main_widget.task_versions_widget.del_button.setVisible(False)
        # self.signal_wrapper.ui_enabled.emit(False)
        task_id = self.main_widget.get_current_task_id()
        print("Task ID: %s" % str(task_id))
        if task_id:
            # 锁工具栏
            self.main_widget.tools_tab_widget.setEnabled(True)

            if not db:
                db = self.__get_db()

            # 设置任务详情页
            self.signal_wrapper.set_status_text.emit(self.current_lan.get_task_details % task_id)
            task_info = db.get_task_info(task_id)
            task_info.pop("type")
            self.main_widget.task_info_widget.clear_items()
            # self.main_widget.task_info_widget.add_items(task_info)
            self.signal_wrapper.set_task_ui_info.emit(task_info)

            # 设置版本详情页
            self.signal_wrapper.set_status_text.emit(self.current_lan.get_version_details % task_id)
            versions_info = db.get_task_versions(task_id)
            versions_info.reverse()
            self.main_widget.task_versions_widget.clear_items()
            if versions_info:
                [version.pop("type") for version in versions_info]
                head_labels = [str(head_label) for head_label in versions_info[0]]
                # 添加头
                self.signal_wrapper.set_version_ui_heads.emit(head_labels)
                # 添加项
                for version_entity in versions_info:
                    id = version_entity["id"]
                    created_time = version_entity["created_at"]
                    item_info = [str(v) for v in version_entity.values()]
                    self.signal_wrapper.set_version_ui_item.emit(id, created_time, item_info)

            # 获取最新 version name
            # 当前版本文件文件名
            # self.name = name_center.SGGetName(db.sg, task_id)
            self.name_data_map = db.get_publish_data(task_id)
            self.name = name_center.Name()
            self.name.root = db.get_local_path()
            self.name.set_map(self.name_data_map)
            # 版本号
            versins_name = [version_entity["code"] for version_entity in versions_info]
            self.name.version_num = util.get_max_ver_num(versins_name) + 1

            # 设置提交框右上角的Ver
            self.main_widget.publisher_widget.set_version_label(self.name.version)

            self.main_widget.publisher_widget.clear_version_name()
            self.main_widget.publisher_widget.set_version_name(self.name.version_name())

            # # 创建 work 文件夹
            # work_path = Path(self.name.work_path())
            # work_path.mkdir(parents=True, exist_ok=True)
            #
            # self.signal_wrapper.set_status_text.emit(str(work_path))
            self.signal_wrapper.set_status_text.emit(u"完成")
        # self.signal_wrapper.ui_enabled.emit(True)
        self.signal_wrapper.publish_ui_enabled.emit(True)
        self.task_switching = False

    def set_task_items(self):
        self.signal_wrapper.clear_ui.emit()
        self.signal_wrapper.ui_enabled.emit(False)
        self.signal_wrapper.set_status_text.emit(self.current_lan.get_sg_data)

        db = self.__get_db()
        project, task_status, limit_num = self.main_widget.get_current_filter_info()
        if task_status == "All":
            task_status = None
        tasks_entity = db.get_task(project, task_status, limit_num)
        if not tasks_entity:
            tasks_entity = []
        tasks_entity.reverse()
        for te in tasks_entity:
            id = te["id"]
            entity = te["entity"]
            title = ""
            subtitle = ""
            if entity:
                title = entity["name"]
                subtitle = te["content"]
            info = []
            type = entity["type"]
            if type:
                info.append(type)
            content = te["sg_status_list"]
            if content:
                info.append(content)
            start_date = te["start_date"]
            due_date = te["due_date"]
            if start_date and due_date:
                info.append("%s -- %s" % (str(start_date), str(due_date)))

            self.signal_wrapper.set_task_item.emit(title, subtitle, info, id)

        self.signal_wrapper.ui_enabled.emit(True)
        self.signal_wrapper.set_status_text.emit(self.current_lan.find_task % len(tasks_entity))

    def init_filter_data(self):
        self.signal_wrapper.publish_ui_enabled.emit(False)
        # 锁住功能栏
        self.signal_wrapper.ui_enabled.emit(False)
        # 清空ui数据
        self.signal_wrapper.clear_ui.emit()

        # 独立线程重新获取 db
        self.signal_wrapper.set_status_text.emit(self.current_lan.get_sg_data)
        db = self.__get_db()
        # 将项目名添加到 combobox
        self.signal_wrapper.set_status_text.emit(self.current_lan.get_projects)
        projects_entity = db.get_proejcts()
        all_projects_name = [entity["name"] for entity in projects_entity]
        self.signal_wrapper.set_projects.emit(all_projects_name)
        # 设置 project combobox 默认值
        if all_projects_name:
            save_project_name = self.settings.get_save_project()
            if save_project_name in all_projects_name:
                current_project_name = save_project_name
            else:
                current_project_name = all_projects_name[0]
            self.settings.save_current_project(current_project_name)
            self.signal_wrapper.set_current_project.emit(current_project_name)
            # 设置 task 状态到 combobox
            current_index = self.main_widget.project_combobox.currentIndex()
            current_project_entity = projects_entity[current_index]
            # 获取任务状态
            self.signal_wrapper.set_status_text.emit(self.current_lan.get_status)
            task_display_status = db.get_task_display_status(current_project_entity)
            task_display_status.insert(0, "All")
            self.signal_wrapper.set_task_status.emit(task_display_status)
            save_status_name = self.settings.get_save_task_status()
            # 设置状态的默认值
            if save_status_name in task_display_status:
                self.signal_wrapper.set_current_task_status.emit(save_status_name)
            # 将 filter 控件开启
            self.signal_wrapper.ui_enabled.emit(True)
            self.signal_wrapper.set_status_text.emit(self.current_lan.complete)

            # 加载数据
            self.set_task_items()

    def __get_db(self):
        sgurl, logname, password, user, local_storage = self.settings.get_login_info()
        if sgurl and logname and password and local_storage:
            db = database.SGDB()
            db.local_storage_code = local_storage
            login_status = db.login(sgurl, logname, password, current_user=user)
            if login_status:
                self.main_widget.set_login_button_info(logname, user)
                return db

    def show_main_ui(self):
        self.main_widget.show()
        # 将数据初始化放到独立线程，防止界面卡顿
        self.new_thread_run(self.init_filter_data)

    def show_login_dialog(self):
        # 设置登录框显示上次保存的内容
        sgurl, logname, password, user, local_storage = self.settings.get_login_info()
        self.login_dialog.set_defaults_values(sgurl, logname, user, local_storage)

        db = None
        while not db:
            result = self.login_dialog.exec_()
            values = self.login_dialog.get_current_values()
            self.settings.save_login_info(values["sgurl"],
                                          values["logname"],
                                          values["password"],
                                          values["user"],
                                          values["local_storage"])
            if result == 0:
                sys.exit(0)
            if result == 1:
                self.welcome_screen.show()
                db = self.__get_db()
                self.welcome_screen.close()
                # 显示登陆失败提示窗
                if not db:
                    info = self.current_lan.login_failed_info
                    self.login_dialog.show_retry_messagebox(info)
        return db

    def login(self, reset=False):
        # 获取保存的账号密码登录
        db = None
        if not reset:
            self.welcome_screen.show()
            db = self.__get_db()
            self.welcome_screen.close()
        else:
            self.main_widget.close()

        # 从登录框获取账号密码登录
        while not db:
            db = self.show_login_dialog()

        print("login successful")
        print("current user: %s" % db.current_user)
        return db

    def run(self, reset=False):
        # 登陆
        db = self.login(reset)
        if db:
            # 初始化 ui
            self.show_main_ui()


def show(reset=False):
    welcome.show(__author__, __version__)
    app = QtWidgets.QApplication()
    main = Main()
    main.run(reset)
    sys.exit(app.exec_())


if __name__ == "__main__":
    show()
