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
        self.assertEqual(html, '<pre><a href="./rfc2595#section-2.4">Section&nbsp;2.4 of RFC 2595</a></pre>')

    def test_cross_rfc_appendix_with_description(self):
        html = markup('Appendix B (Examples) of RFC 5678')
        self.assertEqual(html, '<pre><a href="./rfc5678#appendix-B">Appendix&nbsp;B (Examples) of RFC 5678</a></pre>')

    def test_mixed_same_and_cross_rfc_sections(self):
        html = markup('See Section 2.1 for details, but also Section 2.4 of RFC 2595 for comparison.')
        expected = ('<pre>See <a href="#section-2.1">Section 2.1</a> for details, '
                   'but also <a href="./rfc2595#section-2.4">Section&nbsp;2.4 of RFC 2595</a> for comparison.</pre>')
        self.assertEqual(html, expected)

    def test_cross_bcp_section(self):
        html = markup('Section 3 of BCP 14')
        self.assertEqual(html, '<pre><a href="./bcp14#section-3">Section&nbsp;3 of BCP 14</a></pre>')

    def test_cross_std_section(self):
        html = markup('Section 1.2 of STD 1')
        self.assertEqual(html, '<pre><a href="./std1#section-1.2">Section&nbsp;1.2 of STD 1</a></pre>')

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

    def test_cross_rfc_section_with_newline(self):
        html = markup('Section 5.1 of\n   RFC 4279')
        # The newline should be preserved within the link, and nbsp should be used between Section and number
        self.assertIn('Section&nbsp;5.1 of\n   RFC 4279', html)
        self.assertIn('href="./rfc4279#section-5.1"', html)

    def test_rfc_section_split_across_lines(self):
        # Test case for issue where "RFC-XXX Section\n   Y.Z" was being merged into one anchor
        html = markup('         4.2.2.9  Initial Sequence Number Selection: RFC-793 Section\n            3.3, page 27')
        # Should have two separate anchor tags with newline preserved
        self.assertIn('<a href="./rfc793#section-3.3">RFC-793 Section&nbsp;</a>', html)
        self.assertIn('<a href="#section-3.3">3.3</a>', html)
        # Ensure the newline is preserved (line count should be 1)
        content = html.replace('<pre>', '').replace('</pre>', '')
        self.assertEqual(content.count('\n'), 1)


if __name__ == '__main__':
    import unittest
    unittest.main()
