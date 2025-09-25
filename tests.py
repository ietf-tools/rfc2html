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

    def test_cross_rfc_section_simple(self):
        html = markup('Section 2.4 of RFC 2595')
        self.assertEqual(html, '<pre><a href="./rfc2595#section-2.4">Section 2.4 of RFC 2595</a></pre>')

    def test_cross_rfc_appendix_with_description(self):
        html = markup('Appendix B (Examples) of RFC 5678')
        self.assertEqual(html, '<pre><a href="./rfc5678#appendix-B">Appendix B (Examples) of RFC 5678</a></pre>')

    def test_mixed_same_and_cross_rfc_sections(self):
        html = markup('See Section 2.1 for details, but also Section 2.4 of RFC 2595 for comparison.')
        expected = ('<pre>See <a href="#section-2.1">Section 2.1</a> for details, '
                   'but also <a href="./rfc2595#section-2.4">Section 2.4 of RFC 2595</a> for comparison.</pre>')
        self.assertEqual(html, expected)

    def test_cross_bcp_section(self):
        html = markup('Section 3 of BCP 14')
        self.assertEqual(html, '<pre><a href="./bcp14#section-3">Section 3 of BCP 14</a></pre>')

    def test_cross_std_section(self):
        html = markup('Section 1.2 of STD 1')
        self.assertEqual(html, '<pre><a href="./std1#section-1.2">Section 1.2 of STD 1</a></pre>')

    def test_rfc7817_abstract_example(self):
        text = ('It replaces Section 2.4 (Server Identity Check) of RFC 2595 and updates '
                'Section 4.1 (Processing After the STARTTLS Command) of RFC 3207, '
                'Section 11.1 (STARTTLS Security Considerations) of RFC 3501, and '
                'Section 2.2.1 (Server Identity Check) of RFC 5804.')
        html = markup(text)

        # Check that all cross-RFC section references are correctly linked
        self.assertIn('href="./rfc2595#section-2.4"', html)
        self.assertIn('href="./rfc3207#section-4.1"', html)
        self.assertIn('href="./rfc3501#section-11.1"', html)
        self.assertIn('href="./rfc5804#section-2.2.1"', html)

        # Ensure no local section links for cross-RFC references
        self.assertNotIn('href="#section-2.4"', html)
        self.assertNotIn('href="#section-4.1"', html)
        self.assertNotIn('href="#section-11.1"', html)
        self.assertNotIn('href="#section-2.2.1"', html)


if __name__ == '__main__':
    import unittest
    unittest.main()
