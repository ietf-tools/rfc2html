Htmlizing IETF Text Documents
=============================

This module contains one single function, ```markup(text)``` which adds HTML markup
to what is assumed to be an IETF document (usually an Internet-Draft_ or an RFC_)::

  from rfc2html import markup
  with open('rfc3344.txt') as file:
      text = file.read()
  html = markup(text)

As a historic artifact of being a document series which was started at the time when the easiest
way of distributing a 'Request For Comments' was to type it up on a typewriter and mimeographing_
it, RFCs and Internet-Drafts have traditionally been published as plaintext documents with a
maximum line length of 72 characters.

This format isn't particularly appropriate in a web-centric world, howerver, so starting in
2002, `Henrik Levkowetz`_ started using scripts to convert the plaintext documents into HTML
documents with the same look-and-feel as the plaintext originals, but with internal and external
HTML links in order to facilitate browsing.

Since 2004, the resulting documents have been made available on `tools.ietf.org`_.

This module is a packaging of the htmlization code from version 1.113 of the htmlizing script.
Earlier version of the script are available at `tools.ietf.org/tools/rfcmarkup`_

.. _Internet-Draft: https://en.wikipedia.org/wiki/Internet_Draft
.. _RFC: https://en.wikipedia.org/wiki/Request_for_Comments
.. _mimeographing: https://en.wikipedia.org/wiki/Mimeograph
.. _`tools.ietf.org`: https://tools.ietf.org/html/
.. _`tools.ietf.org/tools/rfcmarkup`: https://tools.ietf.org/tools/rfcmarkup
.. _`Henrik Levkowetz`: mailto:henrik@levkowetz.com

