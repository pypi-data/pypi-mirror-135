"""
Basic testing of the unit framework.
"""

import unittest
from gitbuilding.buildup.unit import UnitLibrary

class UnitTestCase(unittest.TestCase):
    """
    Testing unit matching and conversion via the UnitLibrary
    """

    def setUp(self):
        """
        Making a unit library object for tests
        """
        self.unitlib = UnitLibrary()

    def test_match(self):
        """assertEqual
        Checking common units prvide a match
        """
        self.assertIsNotNone(self.unitlib.get_group('l'))
        self.assertIsNotNone(self.unitlib.get_group('ml'))
        self.assertIsNotNone(self.unitlib.get_group(u'μl'))
        self.assertIsNotNone(self.unitlib.get_group('cc'))
        self.assertIsNotNone(self.unitlib.get_group('m^3'))
        self.assertIsNotNone(self.unitlib.get_group('cm^3'))
        self.assertIsNotNone(self.unitlib.get_group('mm^3'))
        self.assertIsNotNone(self.unitlib.get_group('m^2'))
        self.assertIsNotNone(self.unitlib.get_group('cm^2'))
        self.assertIsNotNone(self.unitlib.get_group('mm^2'))
        self.assertIsNotNone(self.unitlib.get_group('m'))
        self.assertIsNotNone(self.unitlib.get_group('cm'))
        self.assertIsNotNone(self.unitlib.get_group('mm'))
        self.assertIsNotNone(self.unitlib.get_group('g'))
        self.assertIsNotNone(self.unitlib.get_group('mg'))
        self.assertIsNotNone(self.unitlib.get_group(u'μg'))

    def test_case_insensitive_match(self):
        """
        Check all give the same unit
        """

        strings = ['milligram', 'Milligram', 'MILLIGRAM', 'milliGRAM']
        for n, string in enumerate(strings):
            group = self.unitlib.get_group(string)
            ind = group.index(string)
            if n > 0:
                self.assertEqual(last_group, group)
                self.assertEqual(last_ind, ind)
            last_group = group
            last_ind = ind

    def test_convertable(self):
        """
        Test similar units convert
        """

        self.assertTrue(self.unitlib.convertable('ml', 'cc'))
        self.assertTrue(self.unitlib.convertable('ml', 'm^3'))
        self.assertTrue(self.unitlib.convertable('m^3', 'cm^3'))
        self.assertTrue(self.unitlib.convertable('mm^2', 'cm^2'))
        self.assertTrue(self.unitlib.convertable('m', 'cm'))
        self.assertTrue(self.unitlib.convertable('mm', 'cm'))
        self.assertTrue(self.unitlib.convertable('g', u'μg'))

    def test_not_convertable(self):
        """
        Test dissimilar units dont convert
        """
        self.assertFalse(self.unitlib.convertable('g', 'cm'))
        self.assertFalse(self.unitlib.convertable('g', 'mm^2'))
        self.assertFalse(self.unitlib.convertable('g', 'mm^3'))
        self.assertFalse(self.unitlib.convertable('m', 'mm^3'))
        self.assertFalse(self.unitlib.convertable('m', 'cc'))

    def test_not_convertable_strange(self):
        """
        Test unknown units dont convert
        """
        self.assertFalse(self.unitlib.convertable('g', 'tins'))
        self.assertFalse(self.unitlib.convertable('blocks', 'mm^2'))
        self.assertFalse(self.unitlib.convertable('good old splash', 'mm^3'))
        self.assertFalse(self.unitlib.convertable('m', 'enough'))
        self.assertFalse(self.unitlib.convertable('foo', 'bar'))

    def test_unify(self):
        """
        Test unifying units produces correct results
        """

        scale_ml, scale_m3, unit = self.unitlib.unify_units('ml', 'm^3')
        self.assertAlmostEqual(scale_ml, 1e-3)
        self.assertAlmostEqual(scale_m3, 1e3)
        self.assertEqual(unit.name, 'L')
        scale_ug, scale_g, unit = self.unitlib.unify_units(u'μg', 'g')
        self.assertAlmostEqual(scale_ug, 1e-6)
        self.assertAlmostEqual(scale_g, 1)
        self.assertEqual(unit.name, 'g')

    def test_unify_fail(self):
        """
        Test unifying of unconvertable units raises error
        """
        with self.assertRaises(RuntimeError):
            self.unitlib.unify_units('m', 'cc')

    def test_scale(self):
        """
        Test direct scaling of quantity gives expected result
        """
        value, unit = self.unitlib.scale_quantity(0.1, u'μg')
        self.assertAlmostEqual(value, 0.1)
        self.assertEqual(unit.name, u'μg')
        value, unit = self.unitlib.scale_quantity(0.1, u'mg')
        self.assertAlmostEqual(value, 100.0)
        self.assertEqual(unit.name, u'μg')

    def test_scale_fail(self):
        """
        Tests caling of unknown units raises error
        """
        with self.assertRaises(RuntimeError):
            self.unitlib.scale_quantity(1, 'foo')

    def test_parent_group_fail(self):
        "Check parent group match fails if in reverse"
        group_cm = self.unitlib.get_group("cm")
        group_m = self.unitlib.get_group("m")
        with self.assertRaises(RuntimeError):
            group_m.get_parent_group_scale(group_cm)

    def test_prefferd_group_fail(self):
        "Check preffered group fails for incompatible units"
        group_cc = self.unitlib.get_group("cc")
        group_m = self.unitlib.get_group("m")
        with self.assertRaises(RuntimeError):
            group_m.preffered_group(group_cc)
