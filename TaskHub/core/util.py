# -*- coding: utf-8 -*-
__author__ = "yangtao"


import re


  

def get_max_ver_num(name_list):
    ver_list = []
    for n in name_list:
        re_result = re.findall("\.(?P<ver>v|V)(?P<num>\d+)", n)
        if re_result:
            ver_list.append(int(re_result[-1][-1]))
    if ver_list:
        ver_list.sort()
        return int(ver_list[-1])
    else:
        return 0




if __name__ == "__main__":
    name_list =  ['veh_car.mdl.model_test.v003', 'veh_car.mdl.model_test.v003', 'S:/temp/ani_shot0230_v001001_.mov', 'TST_car_Model_v02', 'TST_car_Model_v01', 'vehicle', 'ScreenShot-b.png', 'ScreenShot-b.png', 'ScreenShot-c', 'scene']
    print(get_max_ver_num(name_list))