
import unittest
import posixpath
import logging
import time
import threading
from gitbuilding.buildup import buildup

class InLineDataTestCase(unittest.TestCase):

    def test_variants(self):
        data_strs = ['qty:6',
                     'Qty:6,   ',
                     'qty:6 , ',
                     '  QTY  :  6']
        for data_str in data_strs:
            expected_dict = {'qty': '6'}
            data_dict = buildup.parse_inline_data(data_str)
            self.assertEqual(data_dict, expected_dict)

    def test_difficult_parse(self):
        data_str = """Qty:6 ,  note: 'This Note is annoying to parse _!"?}}'"""
        expected_dict = {'qty': '6', "note": 'This Note is annoying to parse _!"?}}'}
        data_dict = buildup.parse_inline_data(data_str)
        self.assertEqual(data_dict, expected_dict)

    def test_missing(self):
        data_str = "Step"
        # standard
        expected_dict = {'step': True}
        data_dict = buildup.parse_inline_data(data_str)
        self.assertTrue(data_dict, expected_dict)
        # empty_is_true: false
        data_str = "other"
        expected_dict = {'other': None}
        data_dict = buildup.parse_inline_data(data_str)
        self.assertEqual(data_dict, expected_dict)

    def test_bool(self):
        data_strs = ['step:True',
                     'step:TRUE',
                     'step:true']
        expected_dict = {'step': True}
        for data_str in data_strs:
            data_dict = buildup.parse_inline_data(data_str)
            self.assertTrue(data_dict, expected_dict)
        # step is false
        data_strs = ['step:False',
                     'step:FALSE',
                     'step:false']
        expected_dict = {'step': False}
        for data_str in data_strs:
            data_dict = buildup.parse_inline_data(data_str)
            self.assertTrue(data_dict, expected_dict)

    def test_broken(self):
        data_strs = ['foo1',
                     'foo:bar:foo',
                     'bar:foo,foo-foo',
                     'foo: "bar']
        for data_str in data_strs:
            with self.assertLogs(logger='BuildUp', level=logging.WARN):
                buildup.parse_inline_data(data_str)


class BuildUpParserTestCase(unittest.TestCase):

    def test_parse_link(self):
        filepath = posixpath.join('folder', 'file.md')
        bup = buildup.BuildUpParser("[name](part.md){Qty: 1}", filepath)
        self.assertTrue('name' in bup.part_links)
        self.assertEqual(bup.part_links[0].link_rel_to_page, 'part.md')
        self.assertEqual(bup.part_links[0].link_rel_to_root,
                         posixpath.join('folder', 'part.md'))
        self.assertEqual(bup.plain_links, [])
        self.assertEqual(bup.step_links, [])

    def test_parse_overdefined_link(self):
        filepath = posixpath.join('folder', 'file.md')
        bup = buildup.BuildUpParser("[name](../folder/part.md){Qty: 1}", filepath)
        self.assertTrue('name' in bup.part_links)
        self.assertEqual(bup.part_links[0].link_rel_to_page, 'part.md')
        self.assertEqual(bup.part_links[0].link_rel_to_root,
                         posixpath.join('folder', 'part.md'))
        self.assertEqual(bup.plain_links, [])
        self.assertEqual(bup.step_links, [])

    def test_parse_absolute_link(self):
        bup = buildup.BuildUpParser("[name](/folder/part.md){Qty: 1}", 'file.md')
        self.assertTrue('name' in bup.part_links)
        self.assertEqual(bup.part_links[0].link_rel_to_page, '')
        self.assertEqual(bup.part_links[0].link_rel_to_root, '')
        self.assertEqual(bup.plain_links, [])
        self.assertEqual(bup.step_links, [])

    def test_parse_ref_link(self):
        filepath = posixpath.join('folder', 'file.md')
        in_txt = '[name]: part.md\n\n[name]{Qty: 1}'
        bup = buildup.BuildUpParser(in_txt, filepath)
        self.assertTrue('name' in bup.part_links)
        self.assertEqual(bup.part_links[0].link_rel_to_page, 'part.md')
        self.assertEqual(bup.part_links[0].link_rel_to_root,
                         posixpath.join('folder', 'part.md'))
        # Commented out due to issue #164
        #self.assertEqual(bup.plain_links, [])
        self.assertEqual(bup.step_links, [])

    def test_parse_missing_link(self):
        filepath = posixpath.join('folder', 'file.md')
        bup = buildup.BuildUpParser("[name]{Qty: 1}", filepath)
        self.assertTrue('name' in bup.part_links)
        self.assertEqual(bup.part_links[0].link_rel_to_page, '')
        self.assertEqual(bup.part_links[0].link_rel_to_root, '')
        self.assertEqual(bup.plain_links, [])
        self.assertEqual(bup.step_links, [])

    def test_parse_explicit_missing_ref_link(self):
        filepath = posixpath.join('folder', 'file.md')
        in_txt = '[name]: missing\n\n[name]{Qty: 1}'
        bup = buildup.BuildUpParser(in_txt, filepath)
        self.assertTrue('name' in bup.part_links)
        self.assertEqual(bup.part_links[0].link_rel_to_page, '')
        self.assertEqual(bup.part_links[0].link_rel_to_root, '')
        # Commented out due to issue #164
        #self.assertEqual(bup.plain_links, [])
        self.assertEqual(bup.step_links, [])

    def test_parse_anchor_only_link(self):
        filepath = posixpath.join('folder', 'file.md')
        bup = buildup.BuildUpParser("[name](#place){Qty: 1}", filepath)
        self.assertTrue('name' in bup.part_links)
        self.assertEqual(bup.part_links[0].link_rel_to_page, '#place')
        self.assertEqual(bup.part_links[0].link_rel_to_root, filepath+'#place')
        self.assertEqual(bup.plain_links, [])
        self.assertEqual(bup.step_links, [])

    def test_parse_web_link(self):
        url = 'http://gitbuilding.io'
        bup = buildup.BuildUpParser("[name]("+url+"){Qty: 1}", 'file.md')
        self.assertTrue('name' in bup.part_links)
        self.assertEqual(bup.part_links[0].link_rel_to_page, url)
        self.assertEqual(bup.part_links[0].link_rel_to_root, url)
        self.assertEqual(bup.plain_links, [])
        self.assertEqual(bup.step_links, [])

    def test_parse_library_link(self):
        filepath = posixpath.join('folder', 'file.md')
        bup = buildup.BuildUpParser("[name](../parts.yaml#m3screw){Qty: 1}", filepath)
        self.assertTrue('name' in bup.part_links)
        outpath = posixpath.join('..', 'parts', 'm3screw.md')
        self.assertEqual(bup.part_links[0].link_rel_to_page, outpath)
        outpath = posixpath.join('parts', 'm3screw.md')
        self.assertEqual(bup.part_links[0].link_rel_to_root, outpath)
        self.assertEqual(bup.plain_links, [])
        self.assertEqual(bup.step_links, [])

    def test_parse_link_challenge(self):
        in_txt = """[name](part.md){Qty:6 ,  note: 'This Note is annoying to parse _!"?}}'}"""
        bup = buildup.BuildUpParser(in_txt, 'fiel.md')
        self.assertTrue('name' in bup.part_links)
        self.assertEqual(bup.part_links[0].buildup_data.qty, '6')
        self.assertEqual(bup.part_links[0].buildup_data.note,
                         'This Note is annoying to parse _!"?}}')

    def test_parse_link_challenge2(self):
        in_txt = """Normal text [text inside bracket [link_name](url) more text] and more"""
        bup = buildup.BuildUpParser(in_txt, "file.md")
        self.assertTrue('link_name' in bup.plain_links)

    def test_parse_link_challenge3(self):
        in_txt = """[lots of text that is here for backtracking [link_name]"""
        thread = threading.Thread(name='Parse',
                                  target=buildup.BuildUpParser,
                                  args=(in_txt, "file.md"))
        thread.setDaemon(True)
        thread.start()
        time.sleep(2)
        self.assertFalse(thread.is_alive())

    def test_parse_link_image(self):
        in_txt = """Normal text [![](file.jpg)](page.md) blah"""
        bup = buildup.BuildUpParser(in_txt, "file.md")
        self.assertTrue('![](file.jpg)' in bup.plain_links)
        self.assertEqual(len(bup.images), 1)

    def test_parse_step(self):
        bup = buildup.BuildUpParser("[text](page.md){step}", 'file.md')
        self.assertEqual(bup.step_links[0].link_rel_to_page, 'page.md')
        self.assertEqual(bup.plain_links, [])
        self.assertEqual(bup.part_links, [])

    def test_parse_image(self):
        bup = buildup.BuildUpParser("![Some text](file.jpg)", 'file.md')
        self.assertEqual(len(bup.images), 1)
        self.assertEqual(bup.step_links, [])
        self.assertEqual(bup.plain_links, [])
        self.assertEqual(bup.part_links, [])

    def test_parse_in_page_step(self):
        bup = buildup.BuildUpParser("## Step name{pagestep: an_id}", 'file.md')
        self.assertEqual(bup.in_page_steps[0]["id"], 'an_id')

    def test_parse_in_page_step_correct_id(self):
        bup = buildup.BuildUpParser("## Step name{pagestep: An id}", 'file.md')
        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            self.assertEqual(bup.in_page_steps[0]["id"], 'an-id')

    def test_parse_in_page_step_no_id(self):
        bup = buildup.BuildUpParser("## Step name{pagestep}", 'file.md')
        self.assertEqual(bup.in_page_steps[0]["id"], 'step-name')

    def test_parse_in_page_step_clash(self):
        in_txt = "## Step name{pagestep: foo}\n\n## Another step{pagestep: foo}"
        with self.assertLogs(logger='BuildUp', level=logging.WARN):
            bup = buildup.BuildUpParser(in_txt, 'file.md')
            self.assertEqual(len(bup.in_page_steps), 2)
