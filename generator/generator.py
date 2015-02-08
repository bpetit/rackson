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
        self.__gen_dcs_list()
        self.__gen_dc()

    def __open_target_file(self, name):
        full_path = self.__output_path + name
        return open(full_path, "w")

    def __gen_something(self, target_file, template, vars_dict):
        fd = self.__open_target_file(target_file)
        fd.write(
            self.__templates.get_template(template).render(vars_dict)
        )
        fd.close()

    def __gen_devices_list(self):
        my_vars = { "devices": self.__content['data']['device'].keys() }
        self.__gen_something("device/index.html", "devices.html", my_vars)

    def __gen_device(self):
        for name, data in self.__content['data']['device'].items():
            my_vars = { "data": data }
            self.__gen_something(
                "device/" + name + ".html", "device.html", my_vars
            )

    def __gen_dcs_list(self):
        my_vars = { "dcs": self.__content['data']['dc'].keys() }
        self.__gen_something("dc/index.html", "dcs.html", my_vars)

    def __gen_dc(self):
        for name, data in self.__content['data']['dc'].items():
            pprint(data)
            my_vars = { "data": data }
            self.__gen_something("dc/" + name + ".html", "dc.html", my_vars)

class TemplateLoader(object):

    def __init__(self, path):
        self.__fs_loader = FileSystemLoader(path)
        self.__env = Environment(loader=self.__fs_loader)

    def get_template(self, filename):
        return self.__env.get_template(filename)
