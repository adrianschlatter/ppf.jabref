# -*- coding: utf-8 -*-
"""
Test File Class
"""

import unittest
# import code to be tested here (add to your python path!)
import ppf.jabref as dut


class Test_File(unittest.TestCase):
    """Test File class."""

    def test_File_init(self):
        """Test File creation."""
        link1 = dut.Link(name='x', path='/bla/di/bla', filetype='DOCX')
        link2 = dut.Link(name='whatever', path=r'..\what\ever', filetype='PDF')

        list_of_links = [link1, link2]
        file = dut.File(list_of_links)

        self.assertTrue(file.links is list_of_links)

    def test_Link_from_string(self):
        """Test Link creation from string."""
        string = 'Pref:Bks\\Chpt0.pdf:PDF;Chapter 1:Bks\\Chpt1.pdf:PDF'
        file = dut.File.from_string(string)

        self.assertTrue(file.links[0].name == 'Pref')
        self.assertTrue(file.links[0].path == 'Bks\\Chpt0.pdf')
        self.assertTrue(file.links[0].filetype == 'PDF')
        self.assertTrue(file.links[1].name == 'Chapter 1')
        self.assertTrue(file.links[1].path == 'Bks\\Chpt1.pdf')
        self.assertTrue(file.links[1].filetype == 'PDF')


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    unittest.main()
