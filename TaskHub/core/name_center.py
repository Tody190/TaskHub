# -*- coding: utf-8 -*-
__author__ = "yangtao"


class Name():
    def __init__(self, ):
        super(Name, self).__init__()
        self.version_num = 1  # 默认版本

    @property
    def version(self):
        return "v%03d" % self.version_num

    def set_map(self, dict):
        # 批量添加名称字段属性的映射
        self.__dict__.update(dict)

    def no_version_asset_name(self):
        return "{asset_name}.{step}.{task_name}".format(asset_type=self.asset_type,
                                                        asset_name=self.asset_name,
                                                        step=self.step,
                                                        task_name=self.task_name)

    def no_version_shot_name(self):
        return "{shot}.{step}.{task_name}".format(asset_type=self.asset_type,
                                                  shot=self.shot,
                                                  step=self.step,
                                                  task_name=self.task_name)

    def no_version_name(self):
        if self.type.lower() == "asset":
            return self.no_version_asset_name()
        elif self.type.lower() == "shot":
            return self.no_version_shot_name()

    def asset_version_name(self):
        return self.no_version_asset_name() + ".{ver_num}".format(ver_num=self.version)

    def shot_version_name(self):
        return self.no_version_shot_name() + ".{ver_num}".format(ver_num=self.version)

    def asset_file_name(self):
        format_data = {"asset_type": self.asset_type,
                       "asset_name": self.asset_name,
                       "step": self.step,
                       "task_name": self.task_name,
                       "version": self.version,
                       "ext": self.ext}

        return "{asset_name}{ext}".format(**format_data)

    def shot_file_name(self):
        format_data = {"sequence": self.sequence,
                       "shot": self.shot,
                       "step": self.step,
                       "task_name": self.task_name,
                       "version": self.version,
                       "ext": self.ext}

        return "{shot}.{step}.{task_name}.{version}{ext}".format(**format_data)

    def asset_work_path(self):
        pub_path = "{root}/{project}/"
        pub_path += "assets/{asset_type}/{asset_name}/"
        pub_path += "{step}.{task_name}/work"
        return pub_path.format(root=self.root,
                               project=self.project,
                               asset_type=self.asset_type,
                               asset_name=self.asset_name,
                               step=self.step,
                               task_name=self.task_name)

    def asset_publish_path(self):
        pub_path = "{root}/{project}/"
        pub_path += "assets/{asset_type}/{asset_name}/"
        pub_path += "{step}.{task_name}/publish/"

        pub_path_has_version = pub_path + "{asset_name}.{step}.{task_name}.{version}"
        pub_path_has_version = pub_path_has_version.format(root=self.root,
                                                           project=self.project,
                                                           asset_type=self.asset_type,
                                                           asset_name=self.asset_name,
                                                           step=self.step,
                                                           task_name=self.task_name,
                                                           version=self.version)
        return pub_path_has_version

    def asset_publish_path_no_version(self):
        pub_path = "{root}/{project}/"
        pub_path += "assets/{asset_type}/{asset_name}/"
        pub_path += "{step}.{task_name}/publish/"

        pub_path_no_version = pub_path + "{asset_name}.{step}.{task_name}"
        pub_path_no_version = pub_path_no_version.format(root=self.root,
                                                         project=self.project,
                                                         asset_type=self.asset_type,
                                                         asset_name=self.asset_name,
                                                         step=self.step,
                                                         task_name=self.task_name,
                                                         version=self.version)
        return pub_path_no_version

    def shot_work_path(self):
        pub_path = "{root}/{project}/"
        pub_path += "shots/{sequence}/{shot}/"
        pub_path += "{step}.{task_name}/work"
        return pub_path.format(root=self.root,
                               project=self.project,
                               sequence=self.sequence,
                               shot=self.shot,
                               step=self.step,
                               task_name=self.task_name)

    def shot_publish_path(self):
        pub_path = "{root}/{project}/"
        pub_path += "shots/{sequence}/{shot}/"
        pub_path += "{step}.{task_name}/publish/"

        pub_path_has_version = pub_path + "{shot}.{step}.{task_name}.{version}"
        pub_path_has_version = pub_path_has_version.format(root=self.root,
                                                           project=self.project,
                                                           sequence=self.sequence,
                                                           shot=self.shot,
                                                           step=self.step,
                                                           task_name=self.task_name,
                                                           version=self.version)

        return pub_path_has_version

    def shot_publish_path_no_version(self):
        pub_path = "{root}/{project}/"
        pub_path += "shots/{sequence}/{shot}/"
        pub_path += "{step}.{task_name}/publish/"

        pub_path_no_version = pub_path + "{shot}.{step}.{task_name}"
        pub_path_no_version = pub_path_no_version.format(root=self.root,
                                                         project=self.project,
                                                         sequence=self.sequence,
                                                         shot=self.shot,
                                                         step=self.step,
                                                         task_name=self.task_name,
                                                         version=self.version)

        return pub_path_no_version

    def version_name(self):
        if self.type.lower() == "asset":
            return self.asset_version_name()
        elif self.type.lower() == "shot":
            return self.shot_version_name()

    def name(self):
        if self.type.lower() == "asset":
            return self.asset_file_name()
        elif self.type.lower() == "shot":
            return self.shot_file_name()

    # def publish_file(self, more=""):
    #     if self.type.lower() == "asset":
    #         return self.asset_publish_path() + "/" + self.asset_file_name(more=more)
    #     elif self.type.lower() == "shot":
    #         return self.shot_publish_path() + "/" + self.shot_file_name(more=more)

    def publish_path(self):
        if self.type.lower() == "asset":
            return self.asset_publish_path()
        elif self.type.lower() == "shot":
            return self.shot_publish_path()

    def publish_path_no_version(self):
        if self.type.lower() == "asset":
            return self.asset_publish_path_no_version()
        elif self.type.lower() == "shot":
            return self.shot_publish_path_no_version()

    def preview_file(self, more=""):
        if self.type.lower() == "asset":
            return self.preview_path() + "/" + self.asset_file_name(more=more)
        elif self.type.lower() == "shot":
            return self.preview_path() + "/" + self.shot_file_name(more=more)

    def preview_path(self):
        if self.type.lower() == "asset":
            publish_path = self.asset_publish_path()
        elif self.type.lower() == "shot":
            publish_path = self.shot_publish_path()
        return publish_path + "/_preview"

    def work_path(self):
        if self.type.lower() == "asset":
            return self.asset_work_path()
        elif self.type.lower() == "shot":
            return self.shot_work_path()

    def assembly_definition_shot(self):
        pub_path = "{root}/{project}/"
        pub_path += "shots/{sequence}/{shot}/"
        pub_path += "_assembly/ad/{shot}.ma"

        pub_path = pub_path.format(root=self.root,
                                   project=self.project,
                                   sequence=self.sequence,
                                   shot=self.shot,
                                   step=self.step,
                                   task_name=self.task_name,
                                   version=self.version)

        return pub_path

    def assembly_definition_asset(self):
        pub_path = "{root}/{project}/"
        pub_path += "assets/{asset_type}/{asset_name}/"
        pub_path += "_assembly/ad/{asset_name}.ma"

        pub_path = pub_path.format(root=self.root,
                                   project=self.project,
                                   asset_type=self.asset_type,
                                   asset_name=self.asset_name,
                                   task_name=self.task_name,
                                   step=self.step)

        return pub_path

    def assembly_definition(self):
        if self.type.lower() == "asset":
            return self.assembly_definition_asset()
        elif self.type.lower() == "shot":
            return self.assembly_definition_shot()

if __name__ == "__main__":
    # b = Base()
    # b.version = 3
    # print(b.version)
    sgurl = "https://pjsh.shotgrid.autodesk.com/"
    login = "tao.yang@mihoyo.com"
    password = "MHY@yang"

    import shotgun_api3

    sg = shotgun_api3.Shotgun(sgurl,
                              login=login,
                              password=password)
    import database

    db = database.SGDB()
    db.sg = sg

    name_data_map = db.get_publish_data(6685)
    print(name_data_map)
    name = Name()
    name.set_map(name_data_map)
    name.ext = ".ma"
    name.root = "x:/projects"
    print(name.work_path())

    # print(SGGetName.mro())
