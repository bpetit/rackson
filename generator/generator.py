#!/usr/bin/python3

from jinja2 import Environment, FileSystemLoader
from  generator.loader.json_loader import JsonLoader
from pprint import pprint
from os.path import isfile

class Generator(object):

    def __init__(self, content_path, templates_path, output_path):
        self.__content = JsonLoader(content_path).get_content()
        self.__templates = TemplateLoader(templates_path)
        if not output_path[-1] == '/':
            output_path += '/'
        self.__output_path = output_path

    def generate(self):
        self.__gen_devices_list()
        self.__gen_device()

    def __open_target_file(self, name):
        full_path = self.__output_path + name
        return open(full_path, "w")

    def __gen_devices_list(self):
        fd = self.__open_target_file("devices.html")
        fd.write(
            self.__templates.get_template('devices.html').render(
               devices=self.__content['data']['device'].keys()
            )
        )
        fd.close()

    def __gen_device(self):
        for name, data in self.__content['data']['device'].items():
            fd = self.__open_target_file(name + ".html")
            fd.write(
                self.__templates.get_template('device.html').render(
                    data=data
                )
            )
            fd.close()

class TemplateLoader(object):

    def __init__(self, path):
        self.__fs_loader = FileSystemLoader(path)
        self.__env = Environment(loader=self.__fs_loader)

    def get_template(self, filename):
        return self.__env.get_template(filename)
