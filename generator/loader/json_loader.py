#!/usr/bin/python3

import json, re, os

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
        if os.path.isdir(path):
            self.__root[name] = {}
            last_index = name
            self.__old_root = self.__root
            self.__root = self.__root[name]
            for i in os.listdir(path):
                if path[-1] == '/':
                    if self.__get_content(path + i):
                        break
                else:
                    if self.__get_content(path + '/' + i):
                        break
                self.__root = self.__old_root
            return False
        else:
            path = os.path.dirname(path)
            for leaf in os.listdir(path):
                if re.match("^.*json$", leaf):
                    fd = open(path+'/'+leaf)
                    self.__root[
                        os.path.basename(path+'/'+leaf).split('.')[0]
                    ] = json.load(fd)
                    fd.close()
            return True
