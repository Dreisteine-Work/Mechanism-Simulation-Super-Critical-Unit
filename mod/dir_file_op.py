# -*- coding: utf-8 -*-
"""
Created on 2024/08/05 15:24:15

@File -> dir_file_op.py

@Author: luolei

@Email: dreisteine262@163.com

@Describe: 目录文件操作
"""

from typing import Optional
import pickle
import json
import os


def search_files_in_current_dir(dir_path: str, target_names: Optional[list] = None) -> list:
    """
    从当前目录dir_path中搜索含有目标名字的文件, 返回名字列表

    Params:
    ------
    dir_path: 目录名
    target_names: 包含的目标文件名列表
    """
    all_files_names = [p for p in os.listdir(dir_path)]
    if target_names is None:
        return []
    else:
        target_files = []
        for name in target_names:
            target_files += [p for p in all_files_names if name in p]
        target_files = list(set(target_files))
        return target_files


def erase_files(dir_path: str, names2erase: Optional[list] = None, names2keep: Optional[list] = None):
    """
    删除目录中匹配目标名称的文件。

    Params:
    ------
    dir_path: 目标目录路径。
    names2erase: 需要删除的文件名列表。
    names2keep: 需要保留的文件名列表。如果文件名同时出现在删除和保留列表中，则优先保留。
    """
    if (names2erase is None) & (names2keep is None):
        all_files_names = [p for p in os.listdir(dir_path)]
        final_files2erase = all_files_names  # delete all files in the directory
    else:
        files2erase = search_files_in_current_dir(dir_path, names2erase)
        files2keep = search_files_in_current_dir(dir_path, names2keep)
        final_files2erase = list(
            set([p for p in files2erase if p not in files2keep]))

    for name in final_files2erase:
        os.remove(os.path.join(dir_path, name))


def mk_file(file_dir: str, file_name: str):
    if file_name not in os.listdir(file_dir):
        with open(os.path.join(file_dir, file_name), "w") as f:
            f.write("")


def load_json_file(fp: str) -> dict:
    with open(fp, "r") as f:
        results = json.load(f)
    return results


def save_json_file(obj: dict, fp: str):
    with open(fp, "w") as f:
        json.dump(obj, f, ensure_ascii=False)


def save_pickle(obj, fp: str):
    with open(fp, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(fp: str):
    with open(fp, "rb") as f:
        results = pickle.load(f)
    return results