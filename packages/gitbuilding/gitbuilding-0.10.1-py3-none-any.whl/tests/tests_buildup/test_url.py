import unittest
from copy import copy
from gitbuilding.buildup.url import URLRules, URLTranslator

class URLRulesTestCase(unittest.TestCase):

    def setUp(self):
        self.root_rules = URLRules(True)
        self.rel_rules = URLRules(False)

    def test_set_relative(self):
        self.assertTrue(self.root_rules.rel_to_root)
        self.assertFalse(self.rel_rules.rel_to_root)

    def test_translator(self):
        translator = self.root_rules.create_translator('index.md')
        self.assertTrue(isinstance(translator, URLTranslator))

    def test_modifier(self):
        def mod(url, anchor):
            return url[:-3], anchor
        rules = copy(self.root_rules)
        rules.add_modifier(mod)
        translator = rules.create_translator('dir/index.md')
        self.assertEqual(translator.simple_translate('dir/file.jpg'), 'dir/file.')
        rules = copy(self.rel_rules)
        rules.add_modifier(mod)
        translator = rules.create_translator('dir/index.md')
        self.assertNotEqual(translator.simple_translate('dir/file.jpg'), 'dir/file.')
