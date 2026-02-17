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

        self.assertTrue(file._links is list_of_links)

    def test_File_init_rejects_non_links(self):
        """Test File creation rejects non-Link entries."""
        with self.assertRaises(TypeError):
            dut.File([dut.Link('x', 'p', 'PDF'), 'not-a-link'])

    def test_Link_from_string(self):
        """Test Link creation from string."""
        string = 'Pref:Bks\\Chpt0.pdf:PDF;Chapter 1:Bks\\Chpt1.pdf:PDF'
        file = dut.File.from_string(string)

        self.assertTrue(file._links[0].name == 'Pref')
        self.assertTrue(file._links[0].path == 'Bks\\Chpt0.pdf')
        self.assertTrue(file._links[0].filetype == 'PDF')
        self.assertTrue(file._links[1].name == 'Chapter 1')
        self.assertTrue(file._links[1].path == 'Bks\\Chpt1.pdf')
        self.assertTrue(file._links[1].filetype == 'PDF')

    def test_File_repr(self):
        """Test File string representation."""
        link1 = dut.Link(name='a', path='b:c', filetype='d')
        link2 = dut.Link(name='e', path='f', filetype='g;h')
        file = dut.File([link1, link2])
        self.assertTrue(str(file) == r'a:b\:c:d;e:f:g\;h')


class Test_File_List_Behavior(unittest.TestCase):
    """Test list operations on File"""

    def setUp(self):
        self.list_of_links = [dut.Link('A', './docs/A.docx', 'DOCX'),
                              dut.Link('B', 'pdfs/B.pdf', 'PDF')]
        self.file = dut.File(self.list_of_links)

    def test_indexing(self):
        self.assertTrue(self.file[0] == self.list_of_links[0])

    def test_len(self):
        self.assertTrue(len(self.file) == 2)

    def test_append(self):
        new_link = dut.Link('C', r'.\presentations\C.pptx', 'PPTX')
        self.file.append(new_link)
        self.assertTrue(len(self.file) == 3)

    def test_append_rejects_non_link(self):
        with self.assertRaises(TypeError):
            self.file.append('not-a-link')

    def test_setitem_rejects_non_link(self):
        with self.assertRaises(TypeError):
            self.file[0] = 'not-a-link'

    def test_setitem(self):
        new_link = dut.Link('C', 'docs/C.pdf', 'PDF')
        self.file[1] = new_link
        self.assertTrue(self.file[1] is new_link)

    def test_remove(self):
        original_link = self.list_of_links[0]
        popped_link = self.file.pop(0)
        self.assertTrue(len(self.file) == 1)
        self.assertTrue(popped_link is original_link)


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    unittest.main()
