# -*- coding: utf-8 -*-
"""
Test Link Class
"""

import unittest
# import code to be tested here (add to your python path!)
import ppf.jabref as dut


class Test_Link(unittest.TestCase):
    """Test Link class."""

    def test_Link_init(self):
        """Test Link creation."""
        link = dut.Link(name='Preface',
                        path='/There/is/a/preface/somewhere.pdf',
                        filetype='PDF')
        self.assertTrue(link.name == 'Preface')
        self.assertTrue(link.path == '/There/is/a/preface/somewhere.pdf')
        self.assertTrue(link.filetype == 'PDF')

    def test_Link_from_string(self):
        """Test Link creation from string."""
        string = 'Preface:/There/is/a/preface/somewhere.pdf:PDF'
        link = dut.Link.from_string(string)
        self.assertTrue(link.name == 'Preface')
        self.assertTrue(link.path == '/There/is/a/preface/somewhere.pdf')
        self.assertTrue(link.filetype == 'PDF')


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    unittest.main()
