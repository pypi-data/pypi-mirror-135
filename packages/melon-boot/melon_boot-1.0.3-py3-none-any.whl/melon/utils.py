# -*- encoding: utf-8 -*-
"""
@Author  : zh_o
"""
import csv
import os
from typing import Text, List, Set, Dict, Union


class CollUtil:

    @staticmethod
    def is_not_empty(coll: Union[List, Set]) -> bool:
        return coll and len(coll) > 0

    @staticmethod
    def is_empty(coll: Union[List, Set]) -> bool:
        return not CollUtil.is_not_empty(coll)


class DictUtil:

    @staticmethod
    def is_not_empty(dictionary: Dict) -> bool:
        return dictionary and len(dictionary.items()) > 0

    @staticmethod
    def is_empty(dictionary: Dict) -> bool:
        return not DictUtil.is_not_empty(dictionary)


class StrUtil:

    @staticmethod
    def is_not_blank(string: Text) -> bool:
        return string and len(string.strip()) > 0

    @staticmethod
    def is_blank(string: Text) -> bool:
        return not StrUtil.is_not_blank(string)


class ParameterizeUtil:
    """
    参数化工具
    """

    @staticmethod
    def read_csv_dict(path: Text, headers: List[Text] = None) -> List[Dict]:
        """
        读取csv内容
        :param path: csv文件路径
        :param headers: 表头(为空则默认取首行为表头)
        """
        with open(path) as csv_file:
            contents = [line for line in csv_file if not line.startswith('#')]
            if CollUtil.is_empty(headers):
                reader = csv.DictReader(contents)
            else:
                reader = csv.DictReader(contents, fieldnames=headers)
            lines = list(reader)
        return lines

    @staticmethod
    def read_csv(path: Text, ignore_first_line=True) -> List[List]:
        """
        读取csv内容
        :param path: csv文件路径
        :param ignore_first_line: 是否忽略首行
        """
        with open(path) as csv_file:
            contents = [line for line in csv_file if not line.startswith('#')]
            reader = csv.reader(contents)
            lines = list(reader)
        if ignore_first_line:
            del lines[0]
        return lines


class FileUtil:

    def locate_file(start_path: Text, file_name: Text) -> Text:
        """ locate filename and return absolute file path.
            searching will be recursive upward until system root dir.

        Args:
            file_name (str): target locate file name
            start_path (str): start locating path, maybe file path or directory path

        Returns:
            str: located file path. None if file not found.

        Raises:
            exceptions.FileNotFound: If failed to locate file.

        """
        if os.path.isfile(start_path):
            start_dir_path = os.path.dirname(start_path)
        elif os.path.isdir(start_path):
            start_dir_path = start_path
        else:
            raise Exception(f"invalid path: {start_path}")

        file_path = os.path.join(start_dir_path, file_name)
        if os.path.isfile(file_path):
            # ensure absolute
            return os.path.abspath(file_path)

        # system root dir
        # Windows, e.g. 'E:\\'
        # Linux/Darwin, '/'
        parent_dir = os.path.dirname(start_dir_path)
        if parent_dir == start_dir_path:
            raise Exception(f"{file_name} not found in {start_path}")

        # locate recursive upward
        return FileUtil.locate_file(parent_dir, file_name)
