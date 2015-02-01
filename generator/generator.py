#!/usr/bin/python3

from jinja2 import Environment, FileSystemLoader
from  generator.loader.json_loader import JsonLoader
from pprint import pprint

class Generator(object):

    def __init__(self, content_path, templates_path, output_path):
        self.__content = JsonLoader(content_path).get_content()
        self.__templates = TemplateLoader(templates_path)

    def generate(self):
        print(
            self.__templates.get_template('devices.html').render(
               devices=self.__content['data']['device'].keys()
            )
        )
        for name, data in self.__content['data']['device'].items():
            print(
                name + ': ' +
                self.__templates.get_template('device.html').render(
                    data=data
                )
            )

class TemplateLoader(object):

    def __init__(self, path):
        self.__fs_loader = FileSystemLoader(path)
        self.__env = Environment(loader=self.__fs_loader)

    def get_template(self, filename):
        return self.__env.get_template(filename)
