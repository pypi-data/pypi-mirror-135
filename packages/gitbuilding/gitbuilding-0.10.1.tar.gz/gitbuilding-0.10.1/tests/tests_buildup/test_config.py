import unittest
from marshmallow.exceptions import ValidationError
from gitbuilding.buildup import config

class ConfigTestCase(unittest.TestCase):

    def test_custom_category(self):
        custom_categories = {'PrintedPart': {'Reuse': False,
                                             'DisplayName': 'Printed Parts'}}
        conf = config.ConfigSchema().load({'CustomCategories': custom_categories})
        self.assertEqual(len(conf.categories), 3)
        #note all part names are stored in lowercase to enable the case insensitive
        # matching in BuildUp
        self.assertIn('printedpart', conf.categories)
        self.assertFalse(conf.categories['printedpart'].reuse)
        self.assertEqual(conf.categories['printedpart'].display_name, 'Printed Parts')
        self.assertEqual(conf.default_category, 'part')

    def test_default_category(self):
        custom_categories = {'PrintedPart': {'Reuse': False,
                                             'DisplayName': 'Printed Parts'}}
        conf = config.ConfigSchema().load({'CustomCategories': custom_categories,
                                           'DefaultCategory': 'PrintedPart'})
        self.assertEqual(conf.default_category, 'printedpart')

    def test_missing_default_category(self):
        with self.assertRaises(ValidationError):
            config.ConfigSchema().load({'DefaultCategory': 'PrintedPart'})
