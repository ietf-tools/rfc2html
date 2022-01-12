# Htmlizing IETF Text Documents

[![Release](https://img.shields.io/github/release/ietf-tools/rfc2html.svg?style=flat&maxAge=3600)](https://github.com/ietf-tools/rfc2html/releases)
[![License](https://img.shields.io/badge/license-BSD3-blue.svg?style=flat)](https://github.com/ietf-tools/rfc2html/blob/main/LICENSE)

This module contains one single function, `markup(text)` which adds HTML markup
to what is assumed to be an IETF document (usually an [Internet-Draft] or an [RFC]):

```python
from rfc2html import markup
with open('rfc3344.txt') as file:
    text = file.read()
html = markup(text)
```

As a historic artifact of being a document series which was started at the time when the easiest
way of distributing a 'Request For Comments' was to type it up on a typewriter and mimeographing_
it, RFCs and Internet-Drafts have traditionally been published as plaintext documents with a
maximum line length of 72 characters.

This format isn't particularly appropriate in a web-centric world, howerver, so starting in
2002, [Henrik Levkowetz] started using scripts to convert the plaintext documents into HTML
documents with the same look-and-feel as the plaintext originals, but with internal and external
HTML links in order to facilitate browsing.

Since 2004, the resulting documents have been made available on [tools.ietf.org].

This module is a packaging of the htmlization code from version 1.113 of the htmlizing script.
Earlier version of the script are available at [tools.ietf.org/tools/rfcmarkup]

[Internet-Draft]: https://en.wikipedia.org/wiki/Internet_Draft
[RFC]: https://en.wikipedia.org/wiki/Request_for_Comments
[mimeographing]: https://en.wikipedia.org/wiki/Mimeograph
[tools.ietf.org]: https://tools.ietf.org/html/
[tools.ietf.org/tools/rfcmarkup]: https://tools.ietf.org/tools/rfcmarkup
[Henrik Levkowetz]: mailto:henrik@levkowetz.com
