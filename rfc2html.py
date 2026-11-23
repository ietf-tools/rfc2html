# Copyright 2017-2021 Henrik Levkowtez Killi and the IETF Trust, All Rights Reserved
# -*- indent-with-tabs: 0 -*-

# pylint: disable=C0301,C0103,C0303,C0209,R1705

from __future__ import unicode_literals, print_function, division

import argparse
import re
try:
    from html import escape
except ImportError:
    from cgi import escape
import urllib

__version__ = '2.2.0'

BOM_CODE = 65279

# Constants for cross-reference markers using Unicode private use area
CROSSREF_START_TAG = "\uE000"
CROSSREF_END_TAG = "\uE001"


# Paragraph link support (opt-in, see markup(paragraph_links=True)).
#
# The ids follow the scheme used by the xml2rfc HTML renderer, e.g.
# section-abstract-1, section-boilerplate.1-1, section-2.1-3 and
# section-appendix.a-2.  The text format carries no explicit structure, so
# only plain paragraphs get a link target and a pilcrow; figures, tables and
# lists are recognised heuristically and only advance the paragraph counter.

_PL_FOOTER = re.compile(r"\[Page \w+\](</span>)?\s*$")
_PL_UNNUMBERED = re.compile(
    r"(?i)^(?:(?P<abstract>Abstract)|(?P<status>Status of this Memo)|(?P<copyright>Copyright Notice)"
    r"|(?P<toc>Table of Contents)"
    r"|(?P<back>Acknowledg(?:e)?ments?|Contributors?|Index|(?:Authors?|Editors?)(?:'|&#x27;)? Add?resses?))$")
_PL_LIST_ITEM = re.compile(r"^ *(?:[-*o+]|\d+[.)]|[a-z][.)]|\([a-z0-9]+\))\s+\S")
_PL_DEFINITION = re.compile(r"^ *\S.{0,60}?:  +\S")
_PL_ART = re.compile(r"\+[-=+]{2,}|[-=_]{5,}|^\s*[|+].*[|+]\s*$|\|\s{2,}\||/\s+\\|\\\s+/|\.{4,}|\S {6,}\S|\b[0-9a-f]{16,}\b", re.M)
_PL_SENTENCE_END = re.compile(r"(?:[.:?!;)\]]|&quot;|&#x27;|&gt;)$")


def _plain(line):
    return re.sub(r"<[^>]*>", "", line)


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _paragraph_links(text):
    """Add a link target at the start, and a pilcrow link at the end, of each
    paragraph.  Operates on already htmlized text, as the last step before the
    page breaks are converted."""
    lines = text.split("\n")
    count = len(lines)

    # Classify lines
    kinds = []
    for line in lines:
        plain = _plain(line)
        if re.match(r"<h\d>", line):
            kinds.append("heading")
        elif line.startswith("\f") or _PL_FOOTER.search(line):
            kinds.append("furniture")
        elif not plain.strip():
            kinds.append("blank")
        elif plain == plain.lstrip() and _PL_UNNUMBERED.match(plain.rstrip()):
            kinds.append("unnumbered")
        else:
            kinds.append("text")

    # Group text lines into blocks.  Page headers and footers are transparent,
    # so a block can continue across a page break.
    def continues(block, i):
        previous = lines[block[-1]]
        if _indent(lines[i]) != _indent(previous):
            return False
        first = _plain(lines[i]).strip()
        return not _PL_SENTENCE_END.search(_plain(previous).rstrip()) or first[:1].islower()

    items = []
    block = []
    pending_break = False
    for i in range(count):
        kind = kinds[i]
        if kind == "blank":
            if block and not pending_break:
                j = i + 1
                while j < count and kinds[j] == "blank":
                    j += 1
                if j < count and kinds[j] == "furniture":
                    pending_break = True
                else:
                    items.append(("text", block))
                    block = []
        elif kind == "furniture":
            if block:
                pending_break = True
        elif kind in ("heading", "unnumbered"):
            if block:
                items.append(("text", block))
                block = []
            pending_break = False
            items.append((kind, i))
        else:
            if block and pending_break and not continues(block, i):
                items.append(("text", block))
                block = []
            pending_break = False
            block.append(i)
    if block:
        items.append(("text", block))

    # The body text indentation is the most common indentation of block starts
    starts = {}
    for kind, value in items:
        if kind == "text":
            indent = _indent(lines[value[0]])
            if indent:
                starts[indent] = starts.get(indent, 0) + 1
    base = max(starts, key=lambda k: (starts[k], -k)) if starts else 3

    section = None          # id prefix of the current section
    skip = True             # no paragraph links in this section
    counter = 0
    previous_nonpara = False
    seen_numbered = False
    boilerplate = 0
    appendix_letter = ord("a") - 1
    last_heading = False
    for kind, value in items:
        if kind == "heading":
            line = lines[value]
            match = re.search(r'class="selflink" id="(section|appendix)-([^"]+)"', line)
            if match:
                seen_numbered = True
                number = match.group(2)
                if match.group(1) == "section":
                    section = "section-" + number
                elif "." in number:
                    section = "section-" + number.lower()
                else:
                    section = "section-appendix." + number.lower()
                    appendix_letter = ord(number.lower())
                counter = 0
                previous_nonpara = False
                skip = "reference" in _plain(line).lower()
            elif last_heading and section:
                skip = skip or "reference" in _plain(line).lower()
            last_heading = True
            continue
        last_heading = False
        if kind == "unnumbered":
            match = _PL_UNNUMBERED.match(_plain(lines[value]).rstrip())
            counter = 0
            previous_nonpara = False
            skip = False
            if match.group("abstract") and not seen_numbered:
                section = "section-abstract"
            elif (match.group("status") or match.group("copyright")) and not seen_numbered:
                boilerplate += 1
                section = "section-boilerplate.%d" % boilerplate
            elif match.group("toc") and not seen_numbered:
                section = None
            elif match.group("back") and seen_numbered:
                appendix_letter += 1
                section = "section-appendix." + chr(appendix_letter)
                skip = bool(re.search(r"(?i)index|address", match.group("back")))
            else:
                # Not a heading after all; treat as ordinary text
                kind = "text"
                value = [value]
            if kind == "unnumbered":
                continue
        if section is None or skip:
            continue

        # A block of text
        block = value
        indents = [_indent(lines[i]) for i in block]
        plain = "\n".join(_plain(lines[i]) for i in block)
        is_paragraph = (all(indent == base for indent in indents)
                        and not _PL_LIST_ITEM.match(plain)
                        and not _PL_DEFINITION.match(plain)
                        and not _PL_ART.search(plain))
        if is_paragraph:
            counter += 1
            previous_nonpara = False
            target = "%s-%d" % (section, counter)
            first = lines[block[0]]
            lines[block[0]] = first[:base] + '<a id="%s"></a>' % target + first[base:]
            pilcrow = '<a href="#%s" class="pilcrow">\u00b6</a>' % target
            last = lines[block[-1]]
            if last.endswith("</pre>"):
                last = last[:-len("</pre>")] + pilcrow + "</pre>"
            else:
                last += pilcrow
            lines[block[-1]] = last
        else:
            # Figures, tables and lists count as one element; adjacent
            # non-paragraph blocks are taken to be part of the same element.
            if not previous_nonpara:
                counter += 1
            previous_nonpara = True

    return "\n".join(lines)


def markup(text, path=".", script="", extra="", name=None, paragraph_links=False):

    # ------------------------------------------------------------------------
    # Start of markup handling

    # Strip BOM if present
    if ord(text[0]) == BOM_CODE:
        text = text[1:]

    # Convert \r which is not followed or preceded by a \n to \n
    #  (in case this is a mac document)
    text = re.sub(r"([^\n])\r([^\n])", r"\g<1>\n\g<2>", text)
    # Strip control characters with the exception of \t, \b and \n (we'll
    # deal with \b later)
    text = re.sub(r'[\x00-\x07\x0b-\x1f]', '', text)

    # -------------
    # Normalization

    # Remove whitespace at the end of lines
    text = re.sub(r"[\t ]+\n", "\n", text)

    # Remove whitespace (including formfeeds) at the end of the document.
    # (Trailing formfeeds will result in trailing blank pages.)
    text = re.sub(r"[\t \r\n\f]+$", "\n", text)

    text = text.expandtabs()

    # Remove extra blank lines at the start of the document
    text = re.sub(r"^\n*", "", text, 1)

    # Fix up page breaks:
    # \f should aways be preceeded and followed by \n
    text = re.sub(r"([^\n])\f", r"\g<1>\n\f", text)
    text = re.sub(r"\f([^\n])", r"\f\n\g<1>", text)
    # Limit the number of blank lines after page break
    text = re.sub(r"\f\n+", "\f\n", text)

    # [Page nn] should be followed by \n\f\n
    text = re.sub(r"(?i)(\[Page [0-9ivxlc]+\])[\n\f\t ]*(\n *[^\n\f\t ])", r"\g<1>\n\f\g<2>", text)

    # Normalize indentation
    linestarts = re.findall(r"(?m)^([ ]*)\S", text)
    prefixlen = 72
    for start in linestarts:
        if len(start) < prefixlen:
            prefixlen = len(start)
    if prefixlen:
        text = re.sub(r"\n"+(" "*prefixlen), "\n", text)

    # reference name tag markup
    reference = {}
    ref_url = {}

    ## Locate the start of the References section as the first reference
    ## definition after the last reference usage

    ref_beg = re.search(r"(?im)^(\d+(\.\d+)*)(\.?[ ]+)(References?|Normative References?|Informative References?)", text)
    ref_text = text[ref_beg.end():] if ref_beg else text

    ref_stop_list = re.findall(r'(?im)^(?:Appendix\s+[A-Z]\.|[0-9]+\.)(?:[0-9.]+)?\s+\S.+$', ref_text)
    ref_stop_text = [ t for t in ref_stop_list if not 'reference' in t.lower() ][:1]
    if ref_stop_text:
        ref_end = ref_text.index(ref_stop_text[0])
        ref_text = ref_text[:ref_end]

    ##ref_usages = re.findall("(\W)(\[)([-\w.]+)((, ?[-\w.]+)*\])", text)
    ref_defs = re.findall(r"(?sm)^( *\n *)\[([-\w.]+?)\]( +)(.*?)(\n *)$", ref_text)

    ##ref_pos = [ match.start() for match in ref_usages ]
    ##def_pos = [ match.start() for match in ref_defs ]
    ##ref_pos = [ pos for pos in ref_pos if not pos in ref_defs ]
    ##last_ref_pos = ref_pos[-1] if ref_pos else None

    #sys.stderr.write("ref_defs: %s\n" % repr(ref_defs))
    for tuple in ref_defs:
        title_match = re.search(r'(?sm)^(.*?("[^"]+?").+?|.*?(,[^,]+?,)[^,]+?)$', tuple[3])
        if title_match:
            reftitle = title_match.group(2) or title_match.group(3).strip("[ ,]+")
            # Get rid of page break information inside the title
            reftitle = re.sub(r"(?s)\n\n\S+.*\n\n", "", reftitle)
            reftitle = escape(reftitle, quote=True)
            reftitle = re.sub(r"[\n\t ]+", " ", reftitle) # Remove newlines and tabs
            reference[tuple[1]] = reftitle if not re.search(r'(?i)(page|section|appendix)[- ]', reftitle) else ''
        url_match = re.search(r"(http|https|ftp)://\S+", tuple[3])
        if url_match:
            ref_url[tuple[1]] = url_match.group(0)

    # -------------
    # escape any html significant characters
    text = escape(text)


    # -------------
    # Adding markup

    text = "<pre>"+text+"</pre>"

    # Typewriter-style underline:
    text = re.sub(r"_[\b](.)", r"<u>\g<1></u>", text)
    # Strip remaining instances of \b
    text = text.replace('\b', '')

    # Document-specific fixes
    if name and name == "draft-ietf-dnsop-interim-signed-root-01":
        text = text.replace("F\x84ltstr\xF7m", "F\u00e4ltstr\u00f6m")
        text = text.replace("Ihr\x89n", "Ihr\u00e9n")


    # Line number markup goes here


    # Obsoletes: ... markup
    
    def rfclist_replace(keyword, text):
        def replacement(match):
            group = list(match.groups(""))
            group[3] = re.sub(r"\d+", r'<a href="%s?%srfc=\g<0>">\g<0></a>' % (script, extra), group[3])
            if group[8]:
                group[8] = re.sub(r"\d+", r'<a href="%s?%srfc=\g<0>">\g<0></a>' % (script, extra), group[8])
            else:
                group[8] = ""
            return "\n%s%s%s\n%s%s" % (group[0], group[3], group[5], group[7], group[8])
        text = re.sub(r"\n(%s( RFCs| RFC)?: ?( RFCs| RFC)?)(( \d+,| \d+)+)(.*)\n(( *)((\d+, )*(\d+)))*" % keyword, replacement, text, 1)
        return text

    text = rfclist_replace("Obsoletes", text)
    text = rfclist_replace("Updates", text)
    
    lines = text.splitlines(True)
    head  = "".join(lines[:28])
    rest  = "".join(lines[28:])

    # title markup
    head = re.sub(r'(?im)(([12][0-9][0-9][0-9]|^Obsoletes.*|^Category: (Standards Track|Informational|Experimental|Best Current Practice)) *\n\n+ +)([A-Z][^\n]+)$', r'\g<1><h1>\g<4></h1>', head, 1)
    head = re.sub(r'(?i)(<h1.+</h1>)(\n +)([^<\n]+)\n', r'\g<1>\g<2><h1>\g<3></h1>\n', head, 1)
    head = re.sub(r'(?i)(<h1.+</h1>)(\n +)([^<\n]+)\n', r'\g<1>\g<2><h1>\g<3></h1>\n', head, 1)

    text = head + rest

    # http link markup
    # link crossing a line.  Not permitting ":" after the line break will
    # result in some URLs broken across lines not being recognized, but
    # will on the other hand correctly handle a series of URL listed line
    # by line, one on each line.
    #  Link crossing a line, where the continuation contains '.' or '/'
    text = re.sub(r'(?im)(\s|^|[^=]"|\()((http|https|ftp)://([:A-Za-z0-9_./@%&?#~=-]+)?)(\n +)([A-Za-z0-9_./@%&?#~=-]+[./][A-Za-z0-9_./@%&?#~=-]+[A-Za-z0-9_/@%&?#~=-])([.,)"\s]|$)',
                    r'\g<1><a href="\g<2>\g<6>">\g<2></a>\g<5><a href="\g<2>\g<6>">\g<6></a>\g<7>', text)
    text = re.sub(r"(?im)(&lt;)((http|https|ftp)://([:A-Za-z0-9_./@%&?#~=-]+)?)(\n +)([A-Za-z0-9_./@%&?#~=-]+[A-Za-z0-9_/@%&?#~=-])(&gt;)",
                    r'\g<1><a href="\g<2>\g<6>">\g<2></a>\g<5><a href="\g<2>\g<6>">\g<6></a>\g<7>', text)
    #  Link crossing a line, where first line ends in '-' or '/'
    text = re.sub(r'(?im)(\s|^|[^=]"|\()((http|https|ftp)://([:A-Za-z0-9_./@%&?#~=-]+)?[-/])(\n +)([A-Za-z0-9_./@%&?#~=-]+[A-Za-z0-9_/@%&?#~=-])([.,)"\s]|$)',
                    r'\g<1><a href="\g<2>\g<6>">\g<2></a>\g<5><a href="\g<2>\g<6>">\g<6></a>\g<7>', text)
    text = re.sub(r"(?im)(&lt;)((http|https|ftp)://([:A-Za-z0-9_./@%&?#~=-]+)?)(\n +)([A-Za-z0-9_./@%&?#~=-]+[A-Za-z0-9_/@%&?#~=-])(&gt;)",
                    r'\g<1><a href="\g<2>\g<6>">\g<2></a>\g<5><a href="\g<2>\g<6>">\g<6></a>\g<7>', text)
    # link crossing a line, enclosed in "<" ... ">"
    text = re.sub(r"(?im)<((http|https|ftp)://([:A-Za-z0-9_./@%&?#~=-]+)?)(\n +)([A-Za-z0-9_./@%&?#~=-]+[A-Za-z0-9_/@%&?#~=-])>",
                    r'<\g<1><a href="\g<1>\g<5>">\g<1></a>\g<4><a href="\g<1>\g<5>">\g<5></a>>', text)
    text = re.sub(r"(?im)(&lt;)((http|https|ftp)://([:A-Za-z0-9_./@%&?#~=-]+)?)(\n +)([A-Za-z0-9_./@%&;?#~=-]+[A-Za-z0-9_/@%&;?#~=-])(&gt;)",
                    r'\g<1><a href="\g<2>\g<6>">\g<2></a>\g<5><a href="\g<2>\g<6>">\g<6></a>\g<7>', text)
    # link crossing two lines, enclosed in "<" ... ">"
    text = re.sub(r"(?im)<((http|https|ftp)://([:A-Za-z0-9_./@%&?#~=-]+)?)(\n +)([A-Za-z0-9_./@%&?#~=-]+[A-Za-z0-9_/@%&?#~=-])(\n +)([A-Za-z0-9_./@%&?#~=-]+[A-Za-z0-9_/@%&?#~=-])>",
                    r'<\g<1><a href="\g<1>\g<5>\g<7>">\g<1></a>\g<4><a href="\g<1>\g<5>\g<7>">\g<5></a>\g<6><a href="\g<1>\g<5>\g<7>">\g<7></a>>', text)
    text = re.sub(r"(?im)(&lt;)((http|https|ftp)://([:A-Za-z0-9_./@%&?#~=-]+)?)(\n +)([A-Za-z0-9_./@%&?#~=-]+[A-Za-z0-9_/@%&?#~=-])(\n +)([A-Za-z0-9_./@%&;?#~=-]+[A-Za-z0-9_/@%&;?#~=-])(&gt;)",
                    r'\g<1><a href="\g<2>\g<6>\g<8>">\g<2></a>\g<5><a href="\g<2>\g<6>\g<8>">\g<6></a>\g<7><a href="\g<2>\g<6>\g<8>">\g<8></a>\g<9>', text)
    # link on a single line
    text = re.sub(r'(?im)(\s|^|[^=]"|&lt;|\()((http|https|ftp)://[:A-Za-z0-9_./@%&?#~=-]+[A-Za-z0-9_/@%&?#~=-])([.,)"\s]|&gt;|$)',
                    r'\g<1><a href="\g<2>">\g<2></a>\g<4>', text)
#         # Special case for licensing boilerplate
#         text = text.replace('<a href="http://trustee.ietf.org/">http://trustee.ietf.org/</a>\n   license-info',
#                             '<a href="http://trustee.ietf.org/licence-info">http://trustee.ietf.org/</a>\n   <a href="http://trustee.ietf.org/licence-info">licence-info</a>')

    # undo markup if RFC2606 domain
    text = re.sub(r'(?i)<a href="[a-z]*?://([a-z0-9_-]+?\.)?example(\.(com|org|net))?(/.*?)?">(.*?)</a>', r"\g<5>", text)

    # draft markup
    # draft name crossing line break
    text = re.sub(r"([^/#=\?\w-])(draft-([-a-zA-Z0-9]+-)?)((?: {3,}\S.*)?\n +)([-a-zA-Z0-9]+[a-zA-Z0-9](.txt)?)",
                    r'\g<1><a href="%s?%sdraft=\g<2>\g<5>">\g<2></a>\g<4><a href="%s?%sdraft=\g<2>\g<5>">\g<5></a>' % (script, extra, script, extra), text)
    # draft name on one line (but don't mess with what we just did above)
    text = re.sub(r"([^/#=\?\w>=-])(draft-[-a-zA-Z0-9]+[a-zA-Z0-9](.txt)?)",
                    r'\g<1><a href="%s?%sdraft=\g<2>">\g<2></a>' % (script, extra), text)

    # Handle cross-RFC section references BEFORE RFC linking
    for n in ['rfc', 'bcp', 'fyi', 'std']:
        # section x of rfc y markup (unlinked) - mark RFC as processed with special marker
        # Use more restrictive pattern to avoid matching across sentences
        # Pattern for same-line references (don't match newlines)
        text = re.sub(r"(?i)(section)\s+(\d+(\.\d+)*)([^.\n]*?)[ \t](of|in)[ \t]+(%s[- ]?)(\d+)" % n,
            r'<a href="%s?%s%s=\g<7>#section-\g<2>">\g<1>&nbsp;\g<2>\g<4> \g<5> \g<6>%s\g<7>%s</a>' % (script, extra, n, CROSSREF_START_TAG, CROSSREF_END_TAG), text)
        # Pattern for when "of/in RFC" spans lines (preserve the newline)
        text = re.sub(r"(?i)(section)\s+(\d+(\.\d+)*)([^.\n]*?)[ \t](of|in)\n([ \t]+)(%s[- ]?)(\d+)" % n,
            r'<a href="%s?%s%s=\g<8>#section-\g<2>">\g<1>&nbsp;\g<2>\g<4> \g<5>\n\g<6>\g<7>%s\g<8>%s</a>' % (script, extra, n, CROSSREF_START_TAG, CROSSREF_END_TAG), text)
        text = re.sub(r"(?i)(section)\n(\s+)(\d+(\.\d+)*)([^.\n]*?)\s(of|in)\s+(%s[- ]?)(\d+)" % n,
            r'<a href="%s?%s%s=\g<8>#section-\g<3>">\g<1></a>\n\g<2><a href="%s?%s%s=\g<8>#section-\g<3>">\g<3>\g<5> \g<6> \g<7>%s\g<8>%s</a>' % (script, extra, n, script, extra, n, CROSSREF_START_TAG, CROSSREF_END_TAG), text)
        # appendix x of rfc y markup (unlinked)
        # Pattern for same-line references (don't match newlines)
        text = re.sub(r"(?i)(appendix)\s+([A-Z](\.\d+)*)([^.\n]*?)[ \t](of|in)[ \t]+(%s[- ]?)(\d+)" % n,
            r'<a href="%s?%s%s=\g<7>#appendix-\g<2>">\g<1>&nbsp;\g<2>\g<4> \g<5> \g<6>%s\g<7>%s</a>' % (script, extra, n, CROSSREF_START_TAG, CROSSREF_END_TAG), text)
        # Pattern for when "of/in RFC" spans lines (preserve the newline)
        text = re.sub(r"(?i)(appendix)\s+([A-Z](\.\d+)*)([^.\n]*?)[ \t](of|in)\n([ \t]+)(%s[- ]?)(\d+)" % n,
            r'<a href="%s?%s%s=\g<8>#appendix-\g<2>">\g<1>&nbsp;\g<2>\g<4> \g<5>\n\g<6>\g<7>%s\g<8>%s</a>' % (script, extra, n, CROSSREF_START_TAG, CROSSREF_END_TAG), text)
        text = re.sub(r"(?i)(appendix)\n(\s+)([A-Z](\.\d+)*)([^.\n]*?)\s(of|in)\s+(%s[- ]?)(\d+)" % n,
            r'<a href="%s?%s%s=\g<8>#appendix-\g<3>">\g<1></a>\n\g<2><a href="%s?%s%s=\g<8>#appendix-\g<3>">\g<3>\g<5> \g<6> \g<7>%s\g<8>%s</a>' % (script, extra, n, script, extra, n, CROSSREF_START_TAG, CROSSREF_END_TAG), text)

    # rfc markup
    # rfc and number on the same line (skip RFC numbers already processed in cross-refs)
    text = re.sub(r'(?i)([^[/>\w\-' + re.escape(CROSSREF_START_TAG) + r'])(rfc([- ]?))([0-9]+)(?!' + re.escape(CROSSREF_END_TAG) + r')(\W)',
                    r'\g<1><a href="%s?%srfc=\g<4>">\g<2>\g<4></a>\g<5>' % (script, extra), text)
    # rfc and number on separate lines
    text = re.sub(r"(?i)([^[/>\w-])(rfc([-]?))(\n +)([0-9]+)(\W)",
                    r'\g<1><a href="%s?%srfc=\g<5>">\g<2></a>\g<4><a href="%s?%srfc=\g<5>">\g<5></a>\g<6>' % (script, extra, script, extra), text)
    # spelled out Request For Comments markup
    text = re.sub(r"(?i)(\s)(Request\s+For\s+Comments\s+\([^)]+\)\s+)([0-9]+)",
                    r'\g<1>\g<2><a href="%s?%srfc=\g<3>">\g<3></a>' % (script, extra), text)
    # bcp markup
    text = re.sub(r"(?i)([^[/>\w.-])(bcp([- ]?))([0-9]+)(\W)",
                    r'\g<1><a href="%s?%sbcp=\g<4>">\g<2>\g<4></a>\g<5>' % (script, extra), text)
    text = re.sub(r"(?i)([^[/>\w.-])(bcp([-]?))(\n +)([0-9]+)(\W)",
                    r'\g<1><a href="%s?%sbcp=\g<5>">\g<2></a>\g<4><a href="%s?%sbcp=\g<5>">\g<5></a>\g<6>' % (script, extra, script, extra), text)

    def workinprogress_replacement(match):
        g1 = match.group(1)
        g2 = match.group(2)
        g3 = match.group(3)
        # eliminate embedded hyperlinks in text we'll use as anchor text
        g4 = match.group(4)
        g4 = re.sub(r"<a.+?>(.+?)</a>", r"\g<1>", g4)
        g4url = urllib.parse.quote_plus(g4)
        g5 = match.group(5)
        return '%s[<a id="ref-%s">%s</a>]%s<a style="text-decoration: none" href="https://www.google.com/search?sitesearch=datatracker.ietf.org%%2Fdoc%%2Fhtml%%2F&amp;q=inurl:draft-+%s">%s</a>%s' % (g1, g2, g2, g3, g4url, g4, g5)

    text = re.sub(r'(\n *\n *)\[([-\w.]+)\](\s+.*?)(".+")(,\s+Work\s+in\s+Progress.)', workinprogress_replacement, text)
    text = re.sub(r'(\n *\n *)\[([-\w.]+)\](\s)', r'\g<1>[<a id="ref-\g<2>">\g<2></a>]\g<3>', text)

    text = re.sub(r"(\n *\n *)\[(RFC [-\w.]+)\](\s)", r'\g<1>[<a id="ref-\g<2>">\g<2></a>]\g<3>', text)

    ref_targets = re.findall(r'<a id="ref-(.*?)"', text)

    # reference link markup
    def reference_replacement(match):
        pre = match.group(1)
        beg = match.group(2)
        tag = match.group(3)
        end = match.group(4)
        isrfc = re.match(r"(?i)^rfc[ -]?([0-9]+)$", tag)
        if isrfc:
            rfcnum = isrfc.group(1)
            if tag in reference:
                return '%s%s<a href="%s?%srfc=%s" title="%s">%s</a>%s' % (pre, beg, script, extra, rfcnum, reference[tag], tag, end)
            else:
                return '%s%s<a href="%s?%srfc=%s">%s</a>%s' % (pre, beg, script, extra, rfcnum , tag, end)
        else:
            if tag in ref_targets:
                if tag in reference:
                    return '%s%s<a href="#ref-%s" title="%s">%s</a>%s' % (pre, beg, tag, reference[tag], tag, end)
                else:
                    return '%s%s<a href="#ref-%s">%s</a>%s' % (pre, beg, tag, tag, end)
            else:
                return match.group(0)

    # Group:       1   2   3        45
    text = re.sub(r"(\W)(\[)([-\w.]+)((, ?[-\w.]+)*\])", reference_replacement, text)
    text = re.sub(r"(\W)(\[)(RFC [0-9]+)((, ?RFC [0-9]+)*\])", reference_replacement, text)
    while True:
        old = text
        text = re.sub(r"(\W)(\[(?:<a.*?>.*?</a>, ?)+)([-\w.]+)((, ?[-\w.]+)*\])", reference_replacement, text)
        if text == old:
            break
    while True:
        old = text
        text = re.sub(r"(\W)(\[(?:<a.*?>.*?</a>, ?)+)(RFC [-\w.]+)((, ?RFC [-\w.]+)*\])", reference_replacement, text)
        if text == old:
            break

    # greying out the page headers and footers
    text = re.sub(r"\n(.+\[Page \w+\])\n\f\n(.+)\n", r'\n<span class="grey">\g<1></span>\n\f<span class="grey">\g<2></span>\n', text)

    # contents link markup: section links
    #                   1    2   3        4        5        6         7
    text = re.sub(r"(?m)^(\s*)(\d+(\.\d+)*)(\.?[ ]+)(.*[^ .])( *\. ?\.)(.*[0-9])$", r'\g<1><a href="#section-\g<2>">\g<2></a>\g<4>\g<5>\g<6>\g<7>', text)
    text = re.sub(r"(?m)^(\s*)(Appendix |)([A-Z](\.\d+)*)(\.?[ ]+)(.*[^ .])( *\. ?\.)(.*[0-9])$", r'\g<1><a href="#appendix-\g<3>">\g<2>\g<3></a>\g<5>\g<6>\g<7>\g<8>', text)

    # page number markup
    multidoc_separator = r"========================================================================"
    if re.search(multidoc_separator, text):
        parts = re.split(multidoc_separator, text)
        for i in range(len(parts)):
            parts[i] = re.sub(r"(?si)(\f)([^\f]*\[Page (\w+)\])", r'\g<1><span id="%(page)s-\g<3>" ></span>\g<2>'%{"page": "page-%s"%(i+1)}, parts[i])
            parts[i] = re.sub(r"(?i)(\. ?\. +|\. \. \.|\.\.\. *)([0-9ivxlc]+)( *\n)", r'\g<1><a href="#%(page)s-\g<2>">\g<2></a>\g<3>'%{"page": "page-%s"%(i+1)}, parts[i])
        text = multidoc_separator.join(parts)
    else:
        # page name tag markup
        text = re.sub(r"(?si)(\f)([^\f]*\[Page (\w+)\])", r'\g<1><hr class="noprint" id="page-\g<3>">\g<2>', text)
        # contents link markup: page numbers
        text = re.sub(r"(?i)(\. ?\. +|\. \. \.|\.\.\. *)([0-9ivxlc]+)( *\n)", r'\g<1><a href="#page-\g<2>">\g<2></a>\g<3>', text)

    # section number tag markup
    def section_anchor_replacement(match):
        # exclude TOC entries
        mstring = match.group(0)
        if r" \. \. " in mstring or r"\.\.\." in mstring:
            return mstring

        level = len(re.findall(r"[^\.]+", match.group(1)))+1
        level = min(level, 6)
        html = '<h%s><a class="selflink" id="section-%s" href="#section-%s">%s</a>%s</h%s>' % (level, match.group(1), match.group(1), match.group(1), match.group(3), level)
        html = html.replace("\n", '</h%s>\n<h%s>' % (level, level))
        return html


    text = re.sub(r"(?im)^(\d+(\.\d+)*)(\.?[ ]+\S.*?(\n +\w+.*)?(  |$))", section_anchor_replacement, text)
    #text = re.sub("(?i)(\n *\n *)(\d+(\.\d+)*)(\.?[ ].*)", section_replacement, text)
    # section number link markup (only for local sections not already inside links)
    # Use negative lookbehind to avoid matching inside existing links
    text = re.sub(r"(?i)(?<!>)(section[ \t]+)(\d+(\.\d+)*)", r'<a href="#section-\g<2>">\g<1>\g<2></a>', text)
    text = re.sub(r"(?i)(?<!>)(section)\n(\s+)(\d+(\.\d+)*)", r'<a href="#section-\g<3>">\g<1></a>\n\g<2><a href="#section-\g<3>">\g<3></a>', text)

    # Special cases for licensing boilerplate
    text = text.replace('<a href="#section-4">Section 4</a>.e of the Trust Legal Provisions',
                        'Section 4.e of the <a href="https://trustee.ietf.org/license-info">Trust Legal Provisions</a>')

    while True:
        old = text
        text = re.sub(r"(?i)(sections\s(<a.*?>.*?</a>(,\s|\s?-\s?|\sthrough\s|\sor\s|\sto\s|,?\sand\s))*)(\d+(\.\d+)*)", r'\g<1><a href="#section-\g<4>">\g<4></a>', text)
        if text == old:
            break

    # appendix number tag markup
    def appendix_replacement(match):
        # exclude TOC entries
        mstring = match.group(0)
        if r" \. \. " in mstring or r"\.\.\." in mstring:
            return mstring

        txt = match.group(4)
        num = match.group(2).rstrip('.')
        if num != match.group(2):
            txt = "." + txt
        level = len(re.findall(r"[^\.]+", num))+1
        level = min(level, 6)
        return '<h%s><a class="selflink" id="appendix-%s" href="#appendix-%s">%s%s</a>%s</h%s>' % (level, num, num, match.group(1), num, txt, level)

    text = re.sub(r"(?m)^(Appendix |)([A-Z](\.|\.\d+)+)(\.?[ ].*)$", appendix_replacement, text)
    #text = re.sub("(?i)(\n *\n *)(\d+(\.\d+)*)(\.?[ ].*)", appendix_replacement, text)
    # appendix number link markup
    text = re.sub(r" ([Aa]ppendix[ \t])([A-Z](\.\d+)*)", r' <a href="#appendix-\g<2>">\g<1>\g<2></a>', text)
    text = re.sub(r" ([Aa]ppendix)\n(\s+)([A-Z](\.\d+)*)", r' <a href="#appendix-\g<3>">\g<1></a>\n\g<2><a href="#appendix-\g<3>">\g<3></a>', text)

#        # section x of draft-y markup
#        text = re.sub("(?i)<a href=\"[^\"]*\">(section)\s(\d+(\.\d+)*)</a>(\.?\s+(of|in)\s+)<a href=\"[^\"]*\">(draft-[-.a-zA-Z0-9]+[a-zA-Z0-9])</a>", "<a href=\"%s?%surl=%s/rfc\g<7>.txt#section-\g<2>\">\g<1>&nbsp;\g<2>\g<4>\g<6>\g<7></a>" % (script, extra, rfcs), text)
#        # draft-y, section x markup
#        text = re.sub("(?i)<a href=\"[^\"]*\">(draft-[-.a-zA-Z0-9]+[a-zA-Z0-9])</a>(,?\s)<a href=\"[^\"]*\">(section)\s(\d+(\.\d+)*)</a>", "<a href=\"%s?%surl=%s/rfc\g<2>.txt#section-\g<5>\">\g<1>\g<2>\g<3>\g<4>&nbsp;\g<5></a>" % (script, extra, rfcs), text)
#        # [draft-y], section x markup
#        text = re.sub("(?i)\[<a href=\"[^>\"]+\">(draft-[-.a-zA-Z0-9]+[a-zA-Z0-9])</a>\](,?\s)<a href=\"[^>\"]*\">(section)\s(\d+(\.\d+)*)</a>", "<a href=\"%s?%surl=%s/rfc\g<2>.txt#section-\g<5>\">[\g<1>\g<2>]\g<3>\g<4>&nbsp;\g<5></a>" % (script, extra, rfcs), text)

    for n in ['rfc', 'bcp', 'fyi', 'std']:
        # section x of rfc y markup
        text = re.sub(r'(?i)<a href="([^"]*)"[^>]*>(section)\s(\d+(\.\d+)*)</a>(\.?\s+(of|in)\s+)<a href="([^"]*)"[^>]*>(%s[- ]?)([0-9]+)</a>'%n,
            r'<a href="%s?%s%s=\g<9>\g<1>">\g<2>&nbsp;\g<3>\g<5>\g<8>\g<9></a>' % (script, extra, n), text)
        text = re.sub(r'(?i)<a href="([^"]*)"[^>]*>(section)</a>(\n\s+)<a href="(?:[^"]*)"[^>]*>(\d+(\.\d+)*)</a>(\.?\s+(of|in)\s+)<a href="([^"]*)"[^>]*>(%s[- ]?)([0-9]+)</a>'%n,
            r'<a href="%s?%s%s=\g<10>\g<1>">\g<2></a>\g<3><a href="%s?%s%s=\g<10>\g<1>">\g<4>\g<6>\g<9>\g<10></a>' % (script, extra, n, script, extra, n), text)
        # appendix x of rfc y markup
        text = re.sub(r'(?i)<a href="([^"]*)"[^>]*>(appendix)\s([A-Z](\.\d+)*)</a>(\.?\s+(of|in)\s+)<a href="([^"]*)"[^>]*>(%s[- ]?)([0-9]+)</a>'%n,
            r'<a href="%s?%s%s=\g<9>\g<1>">\g<2>&nbsp;\g<3>\g<5>\g<8>\g<9></a>' % (script, extra, n), text)
        text = re.sub(r'(?i)<a href="([^"]*)"[^>]*>(appendix)</a>(\n\s+)<a href="(?:[^"]*)"[^>]*>([A-Z]+(\.\d+)*)</a>(\.?\s+(of|in)\s+)<a href="([^"]*)"[^>]*>(%s[- ]?)([0-9]+)</a>'%n,
            r'<a href="%s?%s%s=\g<10>\g<1>">\g<2></a>\g<3><a href="%s?%s%s=\g<10>\g<1>">\g<4>\g<6>\g<9>\g<10></a>' % (script, extra, n, script, extra, n), text)

        # rfc y, section x markup
        text = re.sub(r'(?i)<a href="([^"]*)"[^>]*>(%s[- ]?)([0-9]+)</a>(,?\s+)<a href="([^"]*)"[^>]*>(section)\s?(([^<]*))</a>'%n,
            r'<a href="%s?%s%s=\g<3>\g<5>">\g<2>\g<3>\g<4>\g<6>&nbsp;\g<7></a>' % (script, extra, n), text)
        # rfc y, appendix x markup
        text = re.sub(r'(?i)<a href="([^"]*)"[^>]*>(%s[- ]?)([0-9]+)</a>(,?\s+)<a href="([^"]*)"[^>]*>(appendix)\s?(([^<]*))</a>'%n,
            r'<a href="%s?%s%s=\g<3>\g<5>">\g<2>\g<3>\g<4>\g<6>&nbsp;\g<7></a>' % (script, extra, n), text)

        # section x of? [rfc y] markup
        text = re.sub(r'(?i)<a href="([^"]*)"[^>]*>(section)\s(\d+(\.\d+)*)</a>(\.?\s+(of\s+|in\s+)?)\[<a href="([^"]*)"[^>]*>(%s[- ]?)([0-9]+)</a>\]'%n,
            r'<a href="%s?%s%s=\g<9>\g<1>">\g<2>&nbsp;\g<3>\g<5>[\g<8>\g<9>]</a>' % (script, extra, n), text)
        text = re.sub(r'(?i)<a href="([^"]*)"[^>]*>(section)</a>(\n\s+)<a href="(?:[^"]*)"[^>]*>(\d+(\.\d+)*)</a>(\.?\s+(of\s+|in\s+)?)\[<a href="([^"]*)"[^>]*>(%s[- ]?)([0-9]+)</a>\]'%n,
            r'<a href="%s?%s%s=\g<10>\g<1>">\g<2></a>\g<3><a href="%s?%s%s=\g<10>\g<1>">\g<4>\g<6>[\g<9>\g<10>]</a>' % (script, extra, n, script, extra, n), text)
        # appendix x of? [rfc y] markup
        text = re.sub(r'(?i)<a href="([^"]*)"[^>]*>(appendix)\s([A-Z](\.\d+)*)</a>(\.?\s+(of\s+|in\s+)?)\[<a href="([^"]*)"[^>]*>(%s[- ]?)([0-9]+)</a>\]'%n,
            r'<a href="%s?%s%s=\g<9>\g<1>">\g<2>&nbsp;\g<3>\g<5>[\g<8>\g<9>]</a>' % (script, extra, n), text)
        text = re.sub(r'(?i)<a href="([^"]*)"[^>]*>(appendix)</a>(\n\s+)<a href="(?:[^"]*)"[^>]*>([A-Z](\.\d+)*)</a>(\.?\s+(of\s+|in\s+)?)\[<a href="([^"]*)"[^>]*>(%s[- ]?)([0-9]+)</a>\]'%n,
            r'<a href="%s?%s%s=\g<10>\g<1>">\g<2></a>\g<3><a href="%s?%s%s=\g<10>\g<1>">\g<4>\g<6>[\g<9>\g<10>]</a>' % (script, extra, n, script, extra, n), text)

        # [rfc y], section x markup
        text = re.sub(r'(?i)\[<a href="([^>"]+)"[^>]*>(%s[- ]?)([0-9]+)</a>\](,?\s+)<a href="([^>"]*)"[^>]*>(section)\s(\d+(\.\d+)*)</a>'%n,
            r'<a href="%s?%s%s=\g<3>\g<5>">[\g<2>\g<3>]\g<4>\g<6>&nbsp;\g<7></a>' % (script, extra, n), text)
        # [rfc y], appendix x markup
        text = re.sub(r'(?i)\[<a href="([^>"]+)"[^>]*>(%s[- ]?)([0-9]+)</a>\](,?\s+)<a href="([^>"]*)"[^>]*>(appendix)\s([A-Z](\.\d+)*)</a>'%n,
            r'<a href="%s?%s%s=\g<3>\g<5>">[\g<2>\g<3>]\g<4>\g<6>&nbsp;\g<7></a>' % (script, extra, n), text)


    # remove section link for section x.x (of|in) <something else>
    old = text
    text = re.sub(r'(?i)<a href="[^"]*"[^>]*>(section\s+)(\d+(\.\d+)*)</a>(\.?[a-z]*\s+(of|in)\s+)(\[?)<a href="([^"]*)"([^>]*)>(.*)</a>(\]?)',
        r'\g<1>\g<2>\g<4>\g<6><a href="\g<7>"\g<8>>\g<9></a>\g<10>', text)
    text = re.sub(r'(?i)(\[?)<a href="([^"]*#ref[^"]*)"([^>]*)>(.*?)</a>(\]?,\s+)<a href="[^"]*"[^>]*>(section\s+)(\d+(\.\d+)*)</a>',
        r'\g<1><a href="\g<2>"\g<3>>\g<4></a>\g<5>\g<6>\g<7>', text)

    # Special fix for referring to the trust legal provisons in
    # boilerplate text:
    text = re.sub(r'(?i)<a href="[^"]*"[^>]*>(section\s+)(\d+(\.\d+)*)</a>(\.?[a-z]*\s+(of|in)\s*\n\s*the Trust Legal Provisions)',
        r'\g<1>\g<2>\g<4>', text)

    # Clean up cross-RFC markers - convert them back to normal RFC text
    text = re.sub(re.escape(CROSSREF_START_TAG) + r'(\d+)' + re.escape(CROSSREF_END_TAG), r'\1', text)

    if paragraph_links:
        text = _paragraph_links(text)

    #
    #text = re.sub("\f", "<div class=\"newpage\" />", text)
    text = re.sub(r"\n?\f\n?", '</pre>\n<pre class="newpage">', text)

    # restore indentation
    if prefixlen:
        text = re.sub(r"\n", "\n"+(" "*prefixlen), text)

    if path:
        text = re.sub(r"%s\?(rfc|bcp|std)=" % script, r"%s/\g<1>" % path, text)
        text = re.sub(r"%s\?draft=" % script, r"%s/" % path, text)

    return text


def main():
    parser = argparse.ArgumentParser(description="Convert RFC .txt files to .html ones.")
    parser.add_argument("files", nargs="+", metavar="FILE", help="text file to htmlize")
    parser.add_argument("-v", "--verbose", action="store_true", help="name the html files as they are created")
    parser.add_argument("-p", "--paragraph-links", action="store_true", help="add link targets and pilcrow links to paragraphs")
    options = parser.parse_args()

    for filename_txt in options.files:
        filename_html = filename_txt + ".html"
        with open(filename_txt) as file_txt:
            with open(filename_html, "w") as file_html:
                file_html.write(markup(file_txt.read(), paragraph_links=options.paragraph_links))
        if options.verbose:
            print(filename_html)


if __name__ == "__main__":
    main()
