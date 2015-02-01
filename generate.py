#!/usr/bin/python3

from generator.generator import Generator
from os.path import abspath
import settings

if __name__ == '__main__':
    Generator(
        content_path=abspath('data'),
        templates_path=abspath('templates'),
        output_path=abspath('output')
    ).generate()
