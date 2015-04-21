#!/usr/bin/python3

from jinja2 import Environment, FileSystemLoader
from generator.loader.json_loader import JsonLoader
from generator.iphandler import IpHandler
from pprint import pprint
from os.path import isfile, dirname, isdir, abspath
from os import makedirs
from shutil import rmtree
import ipaddress

class Generator(object):

    def __init__(self, content_path, templates_path, output_path):
        self.__content = JsonLoader(content_path).get_content()
        self.__templates = TemplateLoader(templates_path)
        if not output_path[-1] == '/':
            output_path += '/'
        self.__output_path = output_path
        pprint(self.__content)

    def generate(self):
        self.__gen_devices_index()
        self.__gen_devices()
        self.__gen_dcs_index()
        self.__gen_dcs()
        self.__gen_subnets()

    def __open_target_file(self, name):
        full_path = self.__output_path + name
        if not isdir(dirname(full_path)):
            makedirs(dirname(full_path))
        return open(full_path, "w")

    def __gen_something(self, target_file, template, vars_dict):
        fd = self.__open_target_file(target_file)
        fd.write(
            self.__templates.get_template(template).render(vars_dict)
        )
        fd.close()

    def __gen_devices_index(self):
        my_vars = { "devices": self.__content['data']['device'].keys() }
        self.__gen_something("device/index.html", "devices.html", my_vars)

    def __gen_devices(self):
        for name, data in self.__content['data']['device'].items():
            my_vars = { "data": data }
            self.__gen_something(
                "device/" + name + ".html", "device.html", my_vars
            )

    def __gen_dcs_index(self):
        my_vars = { "dcs": self.__content['data']['dc'].keys() }
        self.__gen_something("dc/index.html", "dcs.html", my_vars)

    def __gen_dcs(self):
        for name, data in self.__content['data']['dc'].items():
            my_vars = { "data": data }
            self.__gen_something("dc/" + name + ".html", "dc.html", my_vars)
            for rack_name, rack_data in data['racks'].items():
                self.__gen_something(
                    "dc/" + name + "/" + rack_name + ".html",
                    "rack.html", { "data": rack_data, "name": rack_name }
                )

    def __gen_subnets(self, ):
        self.__clean_subnets_output()
        subnets = {}
        for dev,val in self.__content['data']['device'].items():
            if 'network-interfaces' in val.keys():
                for iface,content in val['network-interfaces'].items():
                    if "ip" in content.keys():
                        for ip in content['ip']:
                            net = ipaddress.ip_network(ip, strict=False)
                            addr = ipaddress.ip_address(ip.split('/')[0])
                            if net in subnets.keys():
                                subnets[net].append((dev, addr))
                            else:
                                subnets[net] = [(dev, addr)]
        for net, data in subnets.items():
            name = str(net).replace(':', '-').replace('.', '-').replace('/', '_')
            pprint(data)
            self.__gen_something(
                "subnets/" + name + '.html',
                'subnet.html', { 'data': data, 'name': str(net), 'object': net }
            )

    def __clean_subnets_output(self):
        path = self.__output_path + 'subnets'
        if isdir(path):
            rmtree(path)


class TemplateLoader(object):

    def __init__(self, path):
        self.__fs_loader = FileSystemLoader(path)
        self.__env = Environment(loader=self.__fs_loader)

    def get_template(self, filename):
        return self.__env.get_template(filename)
