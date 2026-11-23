<div align="center">
    
<img src="https://raw.githubusercontent.com/ietf-tools/common/main/assets/logos/rfc2html.svg" alt="RFC2HTML" height="125" />
    
[![Release](https://img.shields.io/github/release/ietf-tools/rfc2html.svg?style=flat&maxAge=600)](https://github.com/ietf-tools/rfc2html/releases)
[![License](https://img.shields.io/github/license/ietf-tools/rfc2html)](https://github.com/ietf-tools/rfc2html/blob/main/LICENSE)
[![PyPI - Version](https://img.shields.io/pypi/v/rfc2html)](https://pypi.org/project/rfc2html/)
[![PyPI - Status](https://img.shields.io/pypi/status/rfc2html)](https://pypi.org/project/rfc2html/)
[![PyPI - Format](https://img.shields.io/pypi/format/rfc2html)](https://pypi.org/project/rfc2html/)
    
##### Htmlizing IETF Text Documents
    
</div>

- [Changelog](https://github.com/ietf-tools/rfc2html/blob/main/CHANGELOG.md)
- [Contributing](https://github.com/ietf-tools/.github/blob/main/CONTRIBUTING.md)
- [Release Procedure](https://github.com/ietf-tools/.github/blob/main/CONTRIBUTING.md#release-procedure)

---

### Usage

This module contains one single function, `markup(text)` which adds HTML markup
to what is assumed to be an IETF document (usually an [Internet-Draft] or an [RFC]):

```python
from rfc2html import markup
with open('rfc3344.txt') as file:
    text = file.read()
html = markup(text)
```

This function can be used via the CLI:

```bash
$ rfc2html -v rfc3344.txt
rfc3344.txt.html
```

#### Paragraph links

Paragraph links are off by default. Pass `paragraph_links=True` (CLI: `-p`/`--paragraph-links`)
to add a link target at the start of each paragraph and a pilcrow link at its end:

```html
   <a id="section-1-1"></a>Paragraph text...<a href="#section-1-1" class="pilcrow">¶</a>
```

The ids follow the scheme of the HTML generated from RFCs published as XML (`section-abstract-1`,
`section-boilerplate.1-1`, `section-2.1-3`, `section-appendix.a-1`, ...). Plain-text documents carry
no explicit structure, so only ordinary paragraphs get ids; figures, tables and lists are detected
heuristically and only advance the paragraph counter. No CSS is included: style `a.pilcrow` as needed.

### History

As a historic artifact of being a document series which was started at the time when the easiest
way of distributing a *Request For Comments* was to type it up on a typewriter and [mimeographing]
it, RFCs and Internet-Drafts before RFC 8650 were published as plaintext documents with a
maximum line length of 72 characters. Some Internet-Drafts are still created only in this form.

This format isn't particularly appropriate in a web-centric world, howerver, so starting in
2002, [Henrik Levkowetz] started using scripts to convert the plaintext documents into HTML
documents with the same look-and-feel as the plaintext originals, but with internal and external
HTML links in order to facilitate browsing.

Henrik served the resulting documents at tools.ietf.org starting in 2004. These are now served
from the IETF [Datatracker].

This module began as a packaging of the htmlization code from version 1.113 of the htmlizing script.

[Internet-Draft]: https://en.wikipedia.org/wiki/Internet_Draft
[RFC]: https://en.wikipedia.org/wiki/Request_for_Comments
[mimeographing]: https://en.wikipedia.org/wiki/Mimeograph
[Henrik Levkowetz]: mailto:henrik@levkowetz.com
[Datatracker]: https://datatracker.ietf.org/
