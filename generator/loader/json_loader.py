#!/usr/bin/python3

import json, re, os
from pprint import pprint

class JsonLoader(object):

    def __init__(self, path):
        self.path = path
        self.documents = {}
        self.__root = self.documents
        self.__old_root = self.__root

    def get_content(self):
        self.__get_content(self.path)
        return self.documents

    def __get_content(self, path):
        name = os.path.basename(path)
        self.__root[name] = {}
        if os.path.isdir(path):
            self.__old_root = self.__root
            self.__root = self.__root[name]
            for i in os.listdir(path):
                if path[-1] == '/':
                    self.__get_content(path + i)
                else:
                    self.__get_content(path + '/' + i)
                self.__root = self.__old_root
        else:
            if re.match("^.*json$", path):
                fd = open(path)
                self.__root[
                    os.path.basename(path).split('.')[0]
                ] = json.load(fd)
