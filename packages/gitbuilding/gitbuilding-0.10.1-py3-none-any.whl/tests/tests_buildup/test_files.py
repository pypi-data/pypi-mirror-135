import unittest
import os
from gitbuilding.buildup import FileInfo, read_directory

class FilesTestCase(unittest.TestCase):

    def setUp(self):
        self._test_dir = os.path.join(os.path.dirname(__file__),'TestFolder')
        self._exclude_file = 'exclude_me.md'
        self._hidden_file = '.hidden'
        self._file = 'file.md'
        self._image = 'fake_image.png'
        self._ignore_file = '_ignore.md'
        self._file_hidden_dir = os.path.join('.hidden_dir', 'file.md')
        self._file_ignore_dir = os.path.join('_ignore_dir', 'file.md')


    def test_read_directory(self):
        files = read_directory(self._test_dir)
        self.assertEqual(len(files), 3)
        self.assertIn(self._exclude_file, files)
        self.assertNotIn(self._hidden_file, files)
        self.assertIn(self._file, files)
        self.assertIn(self._image, files)
        self.assertNotIn(self._ignore_file, files)
        self.assertNotIn(self._file_hidden_dir, files)
        self.assertNotIn(self._file_ignore_dir, files)

    def test_read_directory_exclude(self):
        files = read_directory(self._test_dir, exclude_list=['exclude_me.md'])
        self.assertEqual(len(files), 2)
        self.assertNotIn(self._exclude_file, files)
        self.assertNotIn(self._hidden_file, files)
        self.assertIn(self._file, files)
        self.assertIn(self._image, files)
        self.assertNotIn(self._ignore_file, files)
        self.assertNotIn(self._file_hidden_dir, files)
        self.assertNotIn(self._file_ignore_dir, files)

    def test_read_directory_show_hidden(self):
        files = read_directory(self._test_dir,
                               exclude_list=['exclude_me.md'],
                               allow_hidden=True)
        self.assertEqual(len(files), 4)
        self.assertNotIn(self._exclude_file, files)
        self.assertIn(self._hidden_file, files)
        self.assertIn(self._file, files)
        self.assertIn(self._image, files)
        self.assertNotIn(self._ignore_file, files)
        self.assertIn(self._file_hidden_dir, files)
        self.assertNotIn(self._file_ignore_dir, files)

    def test_read_directory_show_underscore(self):
        files = read_directory(self._test_dir,
                               exclude_list=['exclude_me.md'],
                               allow_leading_underscore=True)
        self.assertEqual(len(files), 4)
        self.assertNotIn(self._exclude_file, files)
        self.assertNotIn(self._hidden_file, files)
        self.assertIn(self._file, files)
        self.assertIn(self._image, files)
        self.assertIn(self._ignore_file, files)
        self.assertNotIn(self._file_hidden_dir, files)
        self.assertIn(self._file_ignore_dir, files)

    def test_file_info_dict(self):
        files = read_directory(self._test_dir, exclude_list=['exclude_me.md'])
        for file_obj in files:
            file_dict = file_obj.as_dict()
            file_obj_from_dict = FileInfo(**file_dict)
            #check they are different objects that are equal
            self.assertIsNot(file_obj, file_obj_from_dict)
            self.assertEqual(file_obj, file_obj_from_dict)
