# -*- coding: utf-8 -*-

def get_value(dict_name, object_key):
    """
    从嵌套的字典中找到需要的值\n
    dict_name: 要查询的字典\n
    object_key: 目标key\n
    返回目标key对应的value\n
    """

    if isinstance(dict_name, dict):
        # isinstance()函数来判断一个对象是否是一个已知的类型，类似type()优于type() P17
        for key, value in dict_name.items():
            if key == object_key:
                return value
            else:
                # 如果value是dict类型，采用递归
                if isinstance(value, dict):
                    ret = get_value(value, object_key)
                    if ret is not None:
                        return ret
                # 如果value是list类型，则依次进行递归
                elif isinstance(value, list):
                    for i in range(len(value)):
                        ret = get_value(value[i], object_key)
                        if ret is not None:
                            return ret
        # 如果找不到指定的key，返回None
        return None
    else:
        return None

