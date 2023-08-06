import unittest

from markdown import markdown
from gitbuilding.buildup.core import Documentation
from gitbuilding.buildup.url import URLRules
from gitbuilding.buildup.partlist import PartList
from gitbuilding.buildup import ConfigSchema
from gitbuilding.buildup.link import make_link
from gitbuilding.buildup.buildup import parse_inline_data

class PartListTestCase(unittest.TestCase):

    def setUp(self):
        self.config = ConfigSchema().load({})
        link_dict = {"fullmatch": '[name](part.md){Qty: 1}',
                     "linktext": 'name',
                     "linklocation": 'part.md',
                     "alttext": '',
                     "buildup_data": parse_inline_data("Qty: 1")}
        link_dict2 = {"fullmatch": '[name2](part2.md){Qty: 2}',
                      "linktext": 'name2',
                      "linklocation": 'part2.md',
                      "alttext": '',
                      "buildup_data": parse_inline_data("Qty: 2, Cat: Tool")}
        self.example_link = make_link(link_dict, '')
        self.example_link2 = make_link(link_dict2, '')
        self.url_rules = URLRules(rel_to_root=False)
        self.url_translator = self.url_rules.create_translator(page="index.md")

    def test_basic(self):
        pl = PartList(self.config)
        pl.count_link(self.example_link)
        self.assertIsNotNone(pl[0])

    def test_add_same_part(self):
        pl = PartList(self.config)
        pl.count_link(self.example_link)
        pl.count_link(self.example_link)
        self.assertEqual(len(pl), 1)

    def test_bom_md(self):
        pl = PartList(self.config)
        pl.count_link(self.example_link)
        pl.count_link(self.example_link)
        md = pl.bom_md("## Bill of Materials", self.url_translator)
        self.assertIsNotNone(md)
        self.assertTrue('* 2 [name]' in md)
        self.assertTrue('[name]:part.md' in md)
        html = markdown(md)
        self.assertIsNotNone(html)

    def test_bom_md_divide(self):
        pl = PartList(self.config)
        pl.count_link(self.example_link)
        pl.count_link(self.example_link2)
        md = pl.bom_md("## Bill of Materials", self.url_translator)
        self.assertIsNotNone(md)
        self.assertTrue('### Parts' in md)
        self.assertTrue('### Tools' in md)
        html = markdown(md)
        self.assertIsNotNone(html)

    def test_bom_md_no_divide(self):
        pl = PartList(self.config)
        pl.count_link(self.example_link)
        pl.count_link(self.example_link2)
        md = pl.bom_md("## Bill of Materials", self.url_translator, divide=False)
        print(md)
        self.assertIsNotNone(md)
        self.assertFalse('### Parts' in md)
        self.assertFalse('### Tools' in md)
        self.assertTrue('* 1 [name]' in md)
        self.assertTrue('* 2 [name2]' in md)

    def test_bom_csv(self):
        pl = PartList(self.config)
        pl.count_link(self.example_link)
        pl.count_link(self.example_link)
        csv = pl.bom_csv(Documentation(self.config))
        self.assertIsNotNone(csv)
        a = [line.split('\t') for line in csv.split('\n')]
        self.assertEqual(a[1][0], "name")
