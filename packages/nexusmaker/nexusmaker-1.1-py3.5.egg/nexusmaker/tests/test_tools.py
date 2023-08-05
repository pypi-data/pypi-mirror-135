#!/usr/bin/env python3
#coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2016 Simon J. Greenhill'
__license__ = 'New-style BSD'

import unittest

from nexusmaker.tools import slugify

class Test_Slugify(unittest.TestCase):
    def test_brackets(self):
        self.assertEqual(slugify('Banggai (W.dialect)'), 'Banggai_Wdialect')

    def test_dash(self):
        self.assertEqual(slugify('Aklanon - Bisayan'), 'Aklanon_Bisayan')

    def test_accents(self):
        self.assertEqual(slugify('Gimán'), 'Giman')
        self.assertEqual(slugify('Hanunóo'), 'Hanunoo')

    def test_colon(self):
        self.assertEqual(slugify('Kakiduge:n Ilongot'), 'Kakidugen_Ilongot')

    def test_slash(self):
        self.assertEqual(slugify('Angkola / Mandailin'), 'Angkola_Mandailin')
    
    def test_apostrophe(self):
        self.assertEqual(slugify('V’ënen Taut'), 'Venen_Taut')



if __name__ == '__main__':
    unittest.main()

