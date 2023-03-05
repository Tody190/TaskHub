# -*- coding: utf-8 -*-
__author__ = "yangtao"

import os.path
import pprint
import sys

import shotgun_api3

from .. import config


class SGDB:
    def __init__(self):
        self.sg = None
        self.supper_sg = None
        self.current_user = None
        self.local_storage_code = None
        self.local_storage = {}

    def login(self, sgurl, login, password, current_user=None):
        self.sg = shotgun_api3.Shotgun(sgurl,
                                       login=login,
                                       password=password)
        if not current_user:
            return self.sg
        else:
            self.current_user = self.get_user(current_user)
            if self.current_user:
                return self.sg

    def get_user(self, login_name):
        try:
            return self.sg.find_one("HumanUser", [["login", "is", login_name]], ["name"])
        except Exception as e:
            print(e)
            return None

    def get_proejcts(self):
        fields = ["name"]
        filters = [["sg_status", "is", "Active"],
                   ["users", "is", self.current_user]]
        return self.sg.find("Project", filters, fields)

    def get_task_display_status(self, project_entity):
        status_schema = self.sg.schema_field_read("Task",
                                                  field_name="sg_status_list",
                                                  project_entity=project_entity)
        display_values = []
        for value in status_schema["sg_status_list"]["properties"]["display_values"]["value"].values():
            display_values.append(value)
        return display_values

    def get_status_short_code(self, name):
        fields = ["code"]
        filters = [["name", "is", name]]
        status_entity = self.sg.find_one("Status", filters, fields)
        if status_entity:
            return status_entity["code"]

    def get_asset_info(self, asset_id):
        fields = ["code", "short_name", "sg_asset_type"]
        filters = [["id", "is", int(asset_id)]]
        return self.sg.find_one("Asset", filters, fields)

    def get_shot_info(self, shot_id):
        fields = ["code", "short_name", "sg_sequence"]
        filters = [["id", "is", int(shot_id)]]
        return self.sg.find_one("Shot", filters, fields)

    def get_task(self, project_name, task_status=None, limit=0):
        fields = ["content", "entity", "sg_status_list",
                  "start_date", "due_date"]
        filters = [["project", "name_is", project_name],
                   ["task_assignees", "in", self.current_user]]
        if task_status:
            status_short_code = self.get_status_short_code(task_status)
            filters.append(["sg_status_list", "is", status_short_code])

        return self.sg.find("Task", filters, fields, limit=limit)

    def get_task_info(self, task_id):
        fields = ["project", "step", "content", "entity",
                  "entity.Asset.sg_asset_type", "entity.Asset.code",
                  "entity.Shot.sg_sequence.Sequence.code", "entity.Shot.code",
                  "sg_status_list", "sg_description",
                  "start_date", "due_date", "time_logs_sum"]
        filters = [["id", "is", int(task_id)]]
        return self.sg.find_one("Task", filters, fields)

    def get_step(self, step_id):
        fields = ["short_name"]
        filters = [["id", "is", int(step_id)]]
        return self.sg.find_one("Step", filters, fields)

    def get_task_versions(self, task_id):
        fields = ["code", "sg_status_list", "created_at", "description"]
        filters = [["sg_task", "is", {"type": "Task", "id": int(task_id)}]]
        return self.sg.find("Version", filters, fields)

    def get_published_files(self, file_name):
        fields = ["entity", "project", "sg_task", "code"]
        filters = [["code", "is", file_name]]
        return self.sg.find("PublishedFile", filters, fields)

    def get_versions(self, version_name):
        fields = ["entity", "project", "sg_task", "code"]
        filters = [["code", "is", version_name]]
        return self.sg.find("Version", filters, fields)

    def del_version(self, id):
        return self.sg.delete("Version", id)

    def create_published_file(self, pub_file, entity_name, version):
        # file_name = os.path.basename(pub_file)
        published_path = str(pub_file).replace("\\", "/")
        path_cache = published_path.replace(self.get_local_path().replace("\\", "/"), "")
        if path_cache.startswith("/"):
            path_cache = path_cache.split("/", 1)[-1]

        published_file_data = {
            "code": entity_name,
            "sg_file_storage_name": self.local_storage_code,
            "path_cache": path_cache,
            "sg_published_path": published_path,
            # "user": self.current_user,
            "project": version["project"],
            "entity": version["entity"],
            "task": version["sg_task"],
            "version": version,
        }

        published_files = self.get_published_files(entity_name)
        if published_files:
            published_file_entity = published_files[0]
            self.sg.update("PublishedFile", published_file_entity["id"], published_file_data)
        else:
            published_file_entity = self.sg.create("PublishedFile", published_file_data)

        # 上传缩略图截图
        if os.path.splitext(pub_file)[-1] in config.img:
            try:
                self.sg.upload(published_file_entity["type"],
                               published_file_entity["id"],
                               pub_file,
                               field_name="image")
            except Exception as e:
                print(e)

    def create_version(self, task_id, version_name, description):
        # 将文件路径添加到 version 的 publish_files 字段
        # publish_files_text = ""
        # for p in publish_files:
        #     publish_files_text += str(p) + "\n"

        # 创建
        task_entity = self.get_task_info(task_id)
        if task_entity:
            project_entity = task_entity["project"]
            entity_entity = task_entity["entity"]

        version_data = {"sg_task": task_entity,
                        "user": self.current_user,
                        "project": project_entity,
                        "entity": entity_entity,
                        "code": version_name,
                        "description": description}
        # 查找版本
        version_entity = self.get_versions(version_name)
        if version_entity:
            version_entity = version_entity[0]
            self.sg.update("PublishedFile", version_entity["id"], version_data)
        else:
            # 创建版本
            version_entity = self.sg.create("Version", version_data)
        if not version_entity:
            return

        # # 上传视频
        # if mov:
        #     try:
        #         self.sg.upload(version_entity["type"],
        #                        version_entity["id"],
        #                        mov,
        #                        field_name="sg_uploaded_movie")
        #     except Exception as e:
        #         print(e)
        # # 上传图片
        # if image:
        #     try:
        #         self.sg.upload(version_entity["type"],
        #                        version_entity["id"],
        #                        image,
        #                        field_name="image")
        #     except Exception as e:
        #         print(e)

        return version_entity

    def get_version_info(self, version_id):
        fields = ["sg_uploaded_movie"]
        filters = [["id", "is", int(version_id)]]
        return self.sg.find_one("Version", filters, fields)

    def get_publish_data(self, task_id):
        task_info = self.get_task_info(task_id)
        step = self.get_step(task_info[u"step"][u"id"])

        entity_type = task_info["entity"]["type"].lower()
        asset_name = task_info["entity.Asset.code"]
        shot = task_info["entity.Shot.code"]
        if entity_type == "shot":
            code_name = shot
        elif entity_type == "asset":
            code_name = asset_name

        return {"project": task_info[u"project"][u"name"],
                "step": step["short_name"],
                "type": entity_type,
                "asset_type": task_info["entity.Asset.sg_asset_type"],
                "asset_name": asset_name,
                "sequence": task_info["entity.Shot.sg_sequence.Sequence.code"],
                "shot": shot,
                "code_name": code_name,
                "task_name": task_info[u"content"]}

    def get_local_path(self):
        filters = [["code", "is", self.local_storage_code]]
        fields = ["code", "windows_path", "linux_path", "mac_path"]
        self.local_storage = self.sg.find_one("LocalStorage", filters, fields)
        if self.local_storage:
            if sys.platform.startswith("win"):
                return self.local_storage["windows_path"]


if __name__ == "__main__":
    pass