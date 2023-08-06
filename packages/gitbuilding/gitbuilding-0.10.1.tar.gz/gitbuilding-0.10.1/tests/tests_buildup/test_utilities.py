import unittest

from gitbuilding.buildup import utilities


class UtilitiesTestCase(unittest.TestCase):

    def test_wildcard_check(self):
        self.assertFalse(utilities.contains_wildcards('sdkfjsndkfsd.txt'))
        self.assertFalse(utilities.contains_wildcards('sdkfjsndkfsdtxt'))
        self.assertFalse(utilities.contains_wildcards('sdkfjsnd[kfsd.txt'))
        self.assertTrue(utilities.contains_wildcards('sdkfjsn[dkfsd].txt'))
        self.assertTrue(utilities.contains_wildcards('sdkfjs?ndkfsd.txt'))
        self.assertTrue(utilities.contains_wildcards('sdkf*jsndk[fs]d.txt'))
        self.assertTrue(utilities.contains_wildcards('*/sdkfjsndkfsd.txt'))
        self.assertTrue(utilities.contains_wildcards('s*dkfjsndkfsd.txt'))