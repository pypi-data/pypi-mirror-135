import unittest
import logging
from fractions import Fraction
from gitbuilding.buildup.quantity import Quantity, largest_quantity, remaining_quantity

class QuantityTestCase(unittest.TestCase):

    def test_parse_numbers(self):
        in_out = [("34", 34),
                  ("1", 1),
                  ("1.24", 1.24),
                  ("0.25", 0.25),
                  ("1/5", Fraction(1, 5)),
                  ("1 1/3", Fraction(4, 3))]

        for in_string, value in in_out:
            quantity = Quantity(in_string)
            self.assertEqual(quantity.type, quantity.NUMERICAL)
            self.assertEqual(quantity.value, value)

    def test_parse_number_units(self):
        in_out = [('1 1/3 cups', Fraction(4, 3), 'cups'),
                  ('1 fl. oz.', 1, 'fl. oz.'),
                  ('1/2 pinch', Fraction(1, 2), 'pinch'),
                  ('.25 m^2', .25, 'm^2'),
                  ('5 ml', 5, 'ml')]

        for in_string, value, unit in in_out:
            quantity = Quantity(in_string)
            self.assertEqual(quantity.type, quantity.NUMERICAL_UNIT)
            self.assertEqual(quantity.value, value)
            self.assertEqual(quantity.unit, unit)

    def test_parse_string(self):
        input_str = ['Some stuff',
                     'things',
                     'a pinch']

        for string in input_str:
            quantity = Quantity(string)
            self.assertEqual(quantity.type, quantity.DESCRIPTIVE)
            self.assertEqual(quantity.description, string)

    def test_parse_string_warn(self):
        input_str = ['3.2.1things',
                     '.this',
                     '.']

        for string in input_str:
            with self.assertLogs(logger='BuildUp', level=logging.WARN):
                quantity = Quantity(string)
            self.assertEqual(quantity.type, quantity.DESCRIPTIVE)
            self.assertEqual(quantity.description, string)

    def test_equal_quantity(self):
        self.assertEqual(Quantity('1 1/5 barrels'),
                         Quantity('6/5 barrels'))
        self.assertEqual(Quantity('foo'),
                         Quantity('foo'))
        self.assertEqual(Quantity('1 L'),
                         Quantity('1 litre'))
        self.assertEqual(Quantity('1000 mL'),
                         Quantity('1 litre'))
        #They will test equal by using _close_enough
        self.assertEqual(Quantity('1000 mL') + Quantity(u'1 μL'),
                         Quantity('1 litre'))

    def test_not_equal_quantity(self):
        inputs = [('foo', 'bar'),
                  ('1', '1/2'),
                  ('1 ml', '1 L'),
                  ('2 L', '1 L'),
                  ('1', '1L'),
                  ('1 cc', '1g')]
        for in1, in2 in inputs:
            self.assertNotEqual(Quantity(in1), Quantity(in2))

    def test_equal_other_type(self):
        #Also check with a quantity and another type
        self.assertEqual(Quantity('1'), 1)
        self.assertEqual(Quantity('1'), 1.00000001)
        self.assertEqual(Quantity('1 L'), '1000 ml')
        self.assertEqual(Quantity('foo'), 'foo')

    def test_not_equal_other_type(self):
        #Also check with a quantity and another type
        self.assertNotEqual(Quantity('1'), 1.2)
        self.assertNotEqual(Quantity('2'), 1.00000001)
        self.assertNotEqual(Quantity('1 L'), 'bar')
        self.assertNotEqual(Quantity('foo'), 'bar')
        self.assertNotEqual(Quantity('1'), None)

    def test_addition(self):
        in_out = [('1 1/3 cups', '2 1/2 cups', '3 5/6 cups'),
                  ('1', '1/2', '1.5')]
        for in1, in2, output in in_out:
            self.assertEqual(Quantity(in1)+Quantity(in2),
                             Quantity(output))

    def test_addition_warn(self):
        inputs = [('foo', 'bar'),
                  ('1 foo', '1 bar')]
        for in1, in2 in inputs:
            with self.assertLogs(logger='BuildUp', level=logging.WARN):
                total = Quantity(in1)+Quantity(in2)
            self.assertEqual(total.type, Quantity.AMBIGUOUS)

    def test_addition_other_type(self):
        in_out = [(Quantity('1'), 1, Quantity('2')),
                  (2, Quantity('1'), Quantity('3')),
                  (Quantity('100 ml'), '1 L', Quantity('1.1 Litre')),]
        for in1, in2, output in in_out:
            self.assertEqual(in1+in2, output)

    def test_largest(self):
        inputs = [('1 1/2', '1'),
                  ('500 ml', '0.4 L')]
        for in1, in2 in inputs:
            q1 = Quantity(in1)
            q2 = Quantity(in2)
            largest = largest_quantity([q1, q2])
            self.assertEqual(largest, q1)

    def test_largest_reverse(self):
        inputs = [('1', '1 1/2'),
                  ('300 ml', '0.4 L')]
        for in1, in2 in inputs:
            q1 = Quantity(in1)
            q2 = Quantity(in2)
            largest = largest_quantity([q1, q2])
            self.assertEqual(largest, q2)

    def test_largest_warn(self):
        inputs = [('foo', 'bar'),
                  ('1 foo', '1 bar'),
                  ('1 foo', 'bar')]
        for in1, in2 in inputs:
            with self.assertLogs(logger='BuildUp', level=logging.WARN):
                largest = largest_quantity([Quantity(in1), Quantity(in2)])
            self.assertEqual(largest.type, Quantity.AMBIGUOUS)

    def test_format_add(self):
        """
        Test the format of the ouput string.
        """
        in_out = [('1 1/3 cups', '2 1/2 cups', '3 5/6 cups'),
                  ('1', '1/2', '1 1/2'),
                  ('1/2', '1/2', '1'),
                  ('1/4 ml', '1/4 ml', '1/2 ml'),
                  ('.6 m', '.7 m', '1.3 m'),
                  ('1/17', '2/17', '0.1765'),]
        for in1, in2, output in in_out:
            self.assertEqual(str(Quantity(in1)+Quantity(in2)),
                             output)

    def test_remaining_zero(self):
        inputs = [('foo', 'foo'),
                  ('1', '1'),
                  ('0.1', '0.1'),
                  ('1L', '1 litre'),
                  ('1kg', '1000.000001 g')]
        for in1, in2 in inputs:
            remaining = remaining_quantity(Quantity(in1), Quantity(in2))
            self.assertEqual(remaining.type, Quantity.ZERO)

    def test_remaining_value(self):
        in_out = [('3', '1', '2'),
                  ('0.2', '0.1', '0.1'),
                  ('2.2L', '1 litre', '1.2L'),
                  ('1kg', '10 g', '.99kg')]
        for in1, in2, output in in_out:
            remaining = remaining_quantity(Quantity(in1), Quantity(in2))
            self.assertEqual(remaining, Quantity(output))

    def test_remaining_negative(self):
        inputs = [('1', '2'),
                  ('1L', '2 litre')]
        for in1, in2 in inputs:
            with self.assertRaises(ValueError):
                remaining_quantity(Quantity(in1), Quantity(in2))

    def test_remaining_warn(self):
        inputs = [('5', '2 litre'),
                  ('5L', '2 kg')]
        for in1, in2 in inputs:
            with self.assertLogs(logger='BuildUp', level=logging.WARN):
                remaining = remaining_quantity(Quantity(in1), Quantity(in2))
            self.assertEqual(remaining.type, Quantity.AMBIGUOUS)
