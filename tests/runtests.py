#!/usr/bin/python3

import unittest
import sys
from pprint import pprint

sys.path.append('..')

import generator.loader.json_loader

class GeneratorTest(unittest.TestCase):
    def test_get_content(self):
        ld = generator.loader.json_loader.JsonLoader('data/devices')
        content = ld.get_content()
        pprint(content)
        self.assertIn("firewalls", str(content))

if __name__ == '__main__':
    unittest.main()
