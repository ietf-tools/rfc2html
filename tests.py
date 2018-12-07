#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017-2018 Henrik Levkowtez, All Rights Reserved

from __future__ import unicode_literals, print_function, division

from unittest import TestCase
from rfc2html import markup


# This is a stub.  Needs a large number of test cases, to cover individual
# htmlization features.

class MarkupTestCase(TestCase):

    def test_rfc_nnnn_ref(self):
        html = markup('text RFC 1234 text')
        self.assertEqual(html, '<pre>text <a href="./rfc1234">RFC 1234</a> text</pre>')

    def test_rfcnnnn_ref(self):
        html = markup('text RFC1234 text')
        self.assertEqual(html, '<pre>text <a href="./rfc1234">RFC1234</a> text</pre>')

if __name__ == '__main__':
    unittest.main()
