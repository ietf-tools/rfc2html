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

    def test_draft_ref_with_linebreak(self):
        html = markup('draft-ietf-\n              some-name-00')
        self.assertEqual(
            html,
            '<pre>{open_tag}draft-ietf-</a>\n              {open_tag}some-name-00</a></pre>'.format(
                open_tag='<a href="./draft-ietf-some-name-00">',
            ))

    def test_draft_ref_with_linebreak_in_header(self):
        html = markup('draft-ietf-   S. Author\n              some-name-00   Org')
        self.assertEqual(
            html,
            '<pre>{open_tag}draft-ietf-</a>   S. Author\n              {open_tag}some-name-00</a>   Org</pre>'.format(
                open_tag='<a href="./draft-ietf-some-name-00">',
            ))


if __name__ == '__main__':
    import unittest
    unittest.main()
