import copy

import numpy as np
import pandas as pd


def sum_list(nested_list):
    temp = []
    for _ in nested_list:
        temp.extend(_)
    return temp


flatten_list = sum_list


def recursive_sum_list(nested_list: list) -> list:
    """
    Recursively flatten list consist of both list/tuple and un-iterable items
    TODO append method will take much time?
        # inner_item_is_list = [isinstance(_, _) for _ in l]
        # if any(inner_item_is_list):
    """
    temp = []
    for item in nested_list:
        if isinstance(item, (list, tuple)):
            temp.extend(recursive_sum_list(item))
        else:
            temp.append(item)
    return temp


def drop_list_duplicates(initial_list: list) -> list:
    return sorted(list(set(initial_list)), key=initial_list.index)


def intersect_lists(*lists, drop_duplicates=True):
    temp = lists[0]
    if drop_duplicates:
        temp = drop_list_duplicates(temp)
    for l in lists[1:]:
        temp = [_ for _ in temp if _ in l]
    return temp


def subtract_list(list_1, list_2, drop_duplicates=True):
    subtracted_list = [_ for _ in list_1 if _ not in list_2]
    if drop_duplicates:
        return drop_list_duplicates(subtracted_list)
    else:
        return subtracted_list


def union_dicts(*dicts: dict, init=None, copy_init=True, iter_depth=-1):
    if init is None:
        temp = {}
    else:
        temp = copy.deepcopy(init) if copy_init else init
    for d in dicts:
        temp.update(d)
    return temp


def intersect_dict(*dicts) -> dict:
    shared_keys = intersect_sets(*dicts)
    return {k: v for k, v in dicts[0].items() if k in shared_keys}


def align_dict(*dn: dict, columns=None, none_value=np.nan):
    aligned_list = []
    key_union = sorted(set(sum_list(dn)))
    for key in key_union:
        aligned_list.append([di.get(key, none_value) for di in dn])
    if columns is None:
        columns = [f'D{i}' for i in range(1, len(dn) + 1)]
    return pd.DataFrame(aligned_list, index=key_union, columns=columns)


def union_sets(*sets):
    _set = sets[0]
    for s in sets[1:]:
        _set = _set | s
    return _set


def intersect_sets(*sets, iter_depth=-1):
    _set = sets[0]
    for s in sets[1:]:
        _set = _set & s
    return _set


def split_two_set(set1, set2):
    overlapped = set1 & set2
    set1_unique = set1 - set2
    set2_unique = set2 - set1
    return set1_unique, set2_unique, overlapped


def str_mod_to_list(mod):
    mod_list = [each_mod.split(',') for each_mod in mod.strip(';').split(';')]
    mod_list = [(int(_[0]), _[1]) for _ in mod_list]
    return mod_list


def check_value_len_of_dict(checked_dict: dict, thousands_separator=True, sort_keys=False, ):
    # TODO sort_keys 可以为 lambda 函数
    # TODO return length dict or print
    if sort_keys:
        keys = sorted(checked_dict.keys())
    else:
        keys = checked_dict.keys()
    for k in keys:
        v = checked_dict[k]
        v_len = len(v)
        if thousands_separator:
            print(f'{k}: {format(v_len, ",")}')
        else:
            print(f'{k}: {v_len}')


class XmlListConfig(list):
    def __init__(self, x_list):
        super(XmlListConfig, self).__init__()
        for element in x_list:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    def __init__(self, parent_element):
        super(XmlDictConfig, self).__init__()
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    x_dict = XmlDictConfig(element)
                else:
                    x_dict = {element[0].tag: XmlListConfig(element)}
                if element.items():
                    x_dict.update(dict(element.items()))
                self.update({element.tag: x_dict})
            elif element.items():
                self.update({element.tag: dict(element.items())})
            else:
                self.update({element.tag: element.text})


def xml_to_dict(xml_context):
    from xml.etree import cElementTree as ElementTree

    _root = ElementTree.XML(xml_context)
    _xml_dict = XmlDictConfig(_root)
    return _xml_dict
