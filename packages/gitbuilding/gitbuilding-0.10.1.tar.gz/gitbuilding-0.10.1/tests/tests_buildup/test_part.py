import unittest
import logging
from copy import copy
from gitbuilding.buildup.parts import UsedPart
from gitbuilding.buildup.partlist import PartList
from gitbuilding.buildup import ConfigSchema
from gitbuilding.buildup.link import make_link
from gitbuilding.buildup.buildup import parse_inline_data

class PartTestCase(unittest.TestCase):

    def setUp(self):
        self.config = ConfigSchema().load({})

    def test_compare_parts(self):
        link_dict = {"fullmatch": '[name](part.md){Qty: 1}',
                     "linktext": 'name',
                     "linklocation": 'part.m',
                     "alttext": '',
                     "buildup_data": parse_inline_data('Qty: 1')}
        link = make_link(link_dict, '')
        part1 = UsedPart(link, self.config)
        part2 = copy(part1)
        self.assertEqual(part1, part2)

    def test_invalid_parts(self):
        invalid_data = ['Qtty: 1', 'Qty', 'Qty: ']
        for data in invalid_data:
            with self.assertLogs(logger='BuildUp', level=logging.WARN):
                link_dict = {"fullmatch": '[name](part.md){Qty: 1}',
                             "linktext": 'name',
                             "linklocation": 'part.m',
                             "alttext": '',
                             "buildup_data": parse_inline_data(data)}
                link = make_link(link_dict, '')
                UsedPart(link, self.config)

    def test_add_parts(self):
        link_dict = {"fullmatch": '[name]{Qty: 1}',
                     "linktext": 'name',
                     "linklocation": 'part.m',
                     "alttext": '',
                     "buildup_data": parse_inline_data('Qty: 1')}
        link1 = make_link(link_dict, '')
        link_dict["buildup_data"] = parse_inline_data('Qty: 2')
        link2 = make_link(link_dict, '')
        partlist = PartList(self.config)
        partlist.count_link(link1)
        partlist.count_link(link2)
        self.assertEqual(str(partlist[0].qty), '3')
