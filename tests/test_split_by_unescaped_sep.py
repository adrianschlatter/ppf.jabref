# -*- coding: utf-8 -*-
"""
Test Link Class
"""

import unittest
# import code to be tested here (add to your python path!)
import ppf.jabref as dut


class Test_split_by_unescaped_sep(unittest.TestCase):
    """Test split_by_unescaped_sep() function."""

    def test_harmless(self):
        """Test string without escaped chars."""
        str = 'bla:di:bla'
        split = dut.split_by_unescaped_sep(str, sep=':')
        self.assertTrue(split[0] == 'bla')
        self.assertTrue(split[1] == 'di')
        self.assertTrue(split[2] == 'bla')

    def test_escaped_colon(self):
        """Test string with escaped colon."""
        str = r'bla\:bla:di:bla'
        split = dut.split_by_unescaped_sep(str, sep=':')
        self.assertTrue(split[0] == r'bla\:bla')
        self.assertTrue(split[1] == 'di')
        self.assertTrue(split[2] == 'bla')

    def test_backslash_before_colon(self):
        """Test string with backslash before colon."""
        str = r'bla:di\\:bla'
        split = dut.split_by_unescaped_sep(str, sep=':')
        self.assertTrue(split[0] == 'bla')
        self.assertTrue(split[1] == r'di\\')
        self.assertTrue(split[2] == 'bla')

    def test_multibackslash(self):
        """Test string with multiple backslashs."""
        str = r'bla:di\\\::\\bla'
        split = dut.split_by_unescaped_sep(str, sep=':')
        self.assertTrue(split[0] == 'bla')
        self.assertTrue(split[1] == r'di\\\:')
        self.assertTrue(split[2] == r'\\bla')


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    unittest.main()
