# -*- coding: utf-8 -*-
"""
Test citationkey mapping Functions.
"""

import unittest
# import code to be tested here (add to your python path!)
import ppf.jabref as dut
from functools import reduce


class Test_CitationkeyMapping(unittest.TestCase):
    """Test counter2citationkey() and citationkey2counter functions."""

    def test_counter2citationkey(self):
        """Test counter2citationkey with known values."""
        numbers = [0, 26, 26 + 26**2]
        ckeys_true = ['a', 'aa', 'aaa']
        ckeys = [dut.counter2citationkey(c) for c in numbers]

        equal = reduce(lambda a, b: a and b,
                       map(lambda p, q: p == q, ckeys_true, ckeys),
                       True)
        self.assertTrue(equal)

    def test_citationkey2counter(self):
        """Test citationkey2counter with known values."""
        numbers_true = [0, 26, 26 + 26**2]
        ckeys = ['a', 'aa', 'aaa']
        numbers = [dut.citationkey2counter(c) for c in ckeys]

        equal = reduce(lambda a, b: a and b,
                       map(lambda p, q: p == q, numbers_true, numbers),
                       True)
        self.assertTrue(equal)


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    unittest.main()
