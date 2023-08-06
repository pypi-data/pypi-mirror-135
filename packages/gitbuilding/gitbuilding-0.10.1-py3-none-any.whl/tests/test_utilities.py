import unittest
import logging
from copy import deepcopy
from gitbuilding import utilities
from gitbuilding.config import GBConfigSchema

class UtilitiesTestCase(unittest.TestCase):

    def test_no_license(self):
        conf = GBConfigSchema().load({})
        conf_copy = deepcopy(conf)
        lic_file = utilities.handle_licenses(conf)
        self.assertIsNone(lic_file)
        self.assertEqual(conf, conf_copy)

    def test_non_spdx_license(self):
        conf = GBConfigSchema().load({'License': 'Something_madeup'})
        conf_copy = deepcopy(conf)
        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            lic_file = utilities.handle_licenses(conf)
        self.assertIsNone(lic_file)
        self.assertEqual(conf, conf_copy)

    def test_spdx_license(self):
        conf = GBConfigSchema().load({'License': 'MIT', 'Authors': ['Jane Doe']})
        conf_copy = deepcopy(conf)
        lic_file = utilities.handle_licenses(conf)
        self.assertIsNotNone(lic_file)
        self.assertNotEqual(conf, conf_copy)
        self.assertTrue('Jane Doe' in lic_file.content)

    def test_custom_license(self):
        conf = GBConfigSchema().load({'License': 'MIT', 'LicenseFile': '/path/to/a/licence.txt'})
        conf_copy = deepcopy(conf)
        lic_file = utilities.handle_licenses(conf)
        self.assertIsNone(lic_file)
        #Not equal as it will force the output of the LicenseFile
        self.assertNotEqual(conf, conf_copy)

    def test_default_author_list(self):
        conf = GBConfigSchema().load({'Authors': []})
        self.assertIsNone(utilities.author_list(conf))
        self.assertEqual(utilities.author_list(conf, default='Default list'), 'Default list')

    def test_one_author(self):
        authors = ['Jane Doe']
        expected = 'Jane Doe'
        conf = GBConfigSchema().load({'Authors': authors})
        self.assertEqual(utilities.author_list(conf), expected)
        self.assertEqual(utilities.author_list(conf, default='Default list'), expected)

    def test_two_authors(self):
        authors = ['Jane Doe', 'Aaron A. Aaronson']
        expected = 'Jane Doe and Aaron A. Aaronson'
        conf = GBConfigSchema().load({'Authors': authors})
        self.assertEqual(utilities.author_list(conf), expected)
        self.assertEqual(utilities.author_list(conf, default='Default list'), expected)

    def test_three_authors(self):
        authors = ['Jane Doe', 'Aaron A. Aaronson', 'Bilbo Baggins']
        expected = 'Jane Doe, Aaron A. Aaronson, and Bilbo Baggins'
        conf = GBConfigSchema().load({'Authors': authors})
        self.assertEqual(utilities.author_list(conf), expected)
        self.assertEqual(utilities.author_list(conf, default='Default list'), expected)
