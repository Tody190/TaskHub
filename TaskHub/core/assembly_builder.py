# -*- coding: utf-8 -*-
# author:yangtao
# time: 2022/04/27


import os

#
# cache_representation = ["abc", "gpu"]
# scene_representation = ["ma", "mb"]

# "Locator" "Cache" "Scene"
AD_TEMPLATE = {"mod_low_abc":
                   {"index": 1,
                    "type": "Cache"},
               "lay_assembly_ma":
                   {"index": 1,
                    "type": "Scene"},
               "mod_high_abc":
                   {"index": 2,
                    "type": "Cache"},
               "mod_high_ma":
                   {"index": 3,
                    "type": "Scene"}
               }


class Definition():
    def __init__(self):
        self.definition_template_file = os.path.dirname(__file__).replace("\\", "/").rsplit("/", 1)[0] \
                                        + "/templates/assembly_definition.ma"
        self.definition_file = ""
        self.name = ""
        self.step_name = ""
        self.task_name = ""
        self.file_type = ""
        self.data = ""

        self.already_inserted_ad_node = []

    def init_representation_content(self):
        content = """createNode assemblyDefinition -n "{name}_ad";
    setAttr ".isc" yes;
    setAttr ".icn" -type "string" "out_assemblyDefinition.png";
    setAttr ".rep[0].rna" -type "string" "{name}_locator";
    setAttr ".rep[0].rla" -type "string" "locator";
    setAttr ".rep[0].rty" -type "string" "Locator";
    setAttr ".rep[0].rda" -type "string" "{name}";
    """
        content = content.format(name=self.name,
                                 data=self.data
                                 )
        return content

    def representation_content(self, ad_index, ad_type):
        # 插入集合表示
        content = """    //assemblyDefinition Label:{step_name}_{task_name}_{file_type}
    setAttr ".rep[{ad_index}].rna" -type "string" "{name}_{step_name}_{task_name}_{file_type}";
    setAttr ".rep[{ad_index}].rla" -type "string" "{step_name}_{task_name}_{file_type}";
    setAttr ".rep[{ad_index}].rty" -type "string" "{ad_type}";
    setAttr ".rep[{ad_index}].rda" -type "string" "{data}";
"""
        content = content.format(ad_index=ad_index,
                                 name=self.name,
                                 step_name=self.step_name,
                                 task_name=self.task_name,
                                 file_type=self.file_type,
                                 ad_type=ad_type,
                                 data=self.data
                                 )

        return content

    def write_definition_node(self, content):
        # 先创建定义节点目录
        if not os.path.exists(os.path.dirname(self.definition_file)):
            os.makedirs(os.path.dirname(self.definition_file))
        # 将内容写入定义节点
        with open(self.definition_file, "w") as ad_f:
            # 将内容写入文件
            ad_f.write(content)

    def build_definition_node_init(self):
        content = ""
        with open(self.definition_template_file, "r") as tem_f:
            for tem_line in tem_f.readlines():
                if tem_line.startswith("//assemblyDefinition initialization"):
                    for representation_line in self.init_representation_content():
                        content += representation_line
                else:
                    content += tem_line

        self.write_definition_node(content)

    def build_definition_node(self):
        # 插入集合表示
        content = ""
        with open(self.definition_file, "r") as tem_f:
            label_name = "{step_name}_{task_name}_{file_type}".format(step_name=self.step_name,
                                                                      task_name=self.task_name,
                                                                      file_type=self.file_type)
            print("label_name:", label_name)
            for tem_line in tem_f.readlines():
                # 获取已经插入的集合表示节点,防止重复添加
                ad_node_label_locator = "//assemblyDefinition Label:"
                if ad_node_label_locator in tem_line:
                    self.already_inserted_ad_node.append(tem_line.split(ad_node_label_locator)[-1].strip("\n"))
                # 找到插入节点表示
                if "//assemblyDefinition insertion point" in tem_line:
                    # 确定没有添加此节点表示
                    if label_name not in self.already_inserted_ad_node:
                        # 确定此 label 的表示类型
                        if label_name in AD_TEMPLATE:
                            ad_index = AD_TEMPLATE[label_name]["index"]
                            ad_type = AD_TEMPLATE[label_name]["type"]
                            for representation_line in self.representation_content(ad_index, ad_type):
                                content += representation_line
                    content += "    //assemblyDefinition insertion point\n"
                else:
                    content += tem_line

        self.write_definition_node(content)

    def build(self):
        # 检查是否存在定义文件，如果没有创建定义文件
        # 初始化的节点包含一个 locator
        if not os.path.exists(self.definition_file):
            self.build_definition_node_init()

        # 创建定义节点
        self.build_definition_node()


if __name__ == "__main__":
    assembly_definition = Definition()
    assembly_definition.definition_file = "X:/projects/TST/assets/env/env_buildingA/mod.low/_assembly/ad/env_buildingA.ma"
    assembly_definition.name = "env_buildingA"
    assembly_definition.step_name = "mod"
    assembly_definition.task_name = "low"
    assembly_definition.file_type = "abc"
    assembly_definition.data = r"X:\projects\TST\assets\env\env_buildingA\mod.low\publish\env_buildingA.mod.low\abc\env_buildingA.abc"

    assembly_definition.build()
