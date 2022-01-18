# Changelog

## [2.0.2](https://github.com/ietf-tools/rfc2html/compare/v2.0.1...v2.0.2) (2022-01-18)


### Bug Fixes

* fix:  ([21521cd](https://github.com/ietf-tools/rfc2html/commit/21521cdc677396e4b4a6b53450480a8ad7c42099))

## [2.0.1] - 2019-06-25
### Added
- Added a name= keyword argument to markup(), in order to be able to do special handling dependent on the draft or RFC name.  
- Added special case handling for draft-ietf-dnsop-interim-signed-root-01.
- Added a tox.ini file for test runs across py27 and 3.4-3.6, and a trivial tests.py placeholder.
- Added control character stripping.
- Added code to identify not only the start but also the end of reference section(s).

### Changed
- Changed tabs to spaces for python 3.
- Now importing escape() from html instead of cgi if possible.  
- Corrected the copyright in setup.py; fixed some pyflakes issues, and added sys reload with defaultencoding UTF-8 under py27.

## [2.0.0] - 2017-07-11
### Added
- This is the first stand-alone release of the htmlization function used in https://tools.ietf.org/tools/rfcmarkup, corresponding to rfcmarkup 1.121, with some cleanup.

## [1.121] - 2016-07-13
### Added
- Added handling for 'Section x of RFC y', with an intervening line break after 'Section', and similar cases.

## [1.120] - 2016-07-13
### Changed
- Made the argument clenup slightly less agressive, in order to let URLs through.

## [1.119] - 2016-07-13
### Added
- Added some input argument cleanup to avoid xss attacks.
### Changed
- Changed the draft email alias to point to the alias @ietf.org instead of @tools.ietf.org

## [1.118] - 2016-03-29
### Changed
- Tweaked a regexp to get rid of the incorrect link to section 4 in text referring to section 4.e of the trust legal provisions.

## [1.117] - 2016-03-23
### Changed
- Tweaked the URL continuation markup to not permit embedded '>' when concatenating lines with an url enclosed in angle brackets.

## [1.116] - 2016-01-26
### Changed
- Tweaked the page link regex to not match number ranges like 0..255.

## [1.108] - 2014-07-08
### Changed
- Changed rfcmarkup to handle utf-8-encoded input, and deliver utf-8-encoded output.

## [1.106] - 2013-11-26
### Changed
- Tweaked the regexps to handle a final dot in the section number sequence in cases like "Section 2.3. of [RFC6749]".

## [1.105] - 2013-09-11
### Changed
- Changed the annotation shown for the colour coding for Draft Standard from "(obsolete)" to "(old designation)".
- Now fetching rfc status information from the attribute storage instead of from the earlier status file.

## [1.104] - 2013-04-11
### Changed
- Updated the colour legend popup linked to the colour marking a the top of the html document to match RFC 6410.

## [1.103] - 2013-02-21
### Changed
- Updated the standard levels known and supported to match RFC 6410.
- Tweaked the handling of section titles, to better support RFC2119, which has a keyword as title followed by multiple spaces rather than blank lines, for the first 5 sections.  Thanks to <fleasoft@gmx.net> for the bugreport.

## [1.102] - 2012-12-01
### Added
- Added section title styling (`<h2/>` etc.) for section titles which break across 2 lines.
- Added link markup for http/https/ftp URLs which break across 3 lines.

## [1.101] - 2012-05-01
### Changed
- Fixed two issues with quoting, reported and analysed by Roman Donchenko <dpb@corrigendum.ru>: Missing quoting of double-quotes in DC meta- information, and overquoting in reference link title attributes.
- Fixed an issue found because of an issue report from Leif Halvard Silli <malform@malform.no>,  where Latin-1 content was delivered as utf-8, without re-coding.  This affected the rendering of RFC 2557.

## [1.100] - 2012-03-13
### Added
- Added stripping of whitespace and formfeeds at the end of documents, to avoid blank trailing pages, after bugreport and analysis from Martin J. Duerst <duerst@it.aoyama.ac.jp>

## [1.99] - 2011-11-27
### Added
- Added a link to the xml source file in the top menu, where such exists.
### Changed
- Applied a patch from julian.reschke@gmx.de to make section title numbers into links to self, for ease of emailing links into documents.
- In order to support correct sibling links when the html is used to produce pdfs, the 'staticpath' argument was changes so as to accept a path argument instead of just a boolean.  If the argument is 'true' the path is set to '.' (legacy support).
- In order to support correct page breaking when the html is used to produce pdfs, page breaks are now also indicated by '<!--NewPage-->'.

## [1.98] - 2011-10-24
### Changed
- Fix a bug where every other Section link in a list of section links would fail to receive link markup.

## [1.97] - 2011-10-12
### Added
- Add some support for linking out to STD and FYI documents, in addition to the already supported RFC and BCP numbered documents.
### Changed
- Handle constructs like "Appendix D of RFC 2328" and similar better, so that a link to the referenced RFCs appendix is genereated instead of an internal link to (a possibly nonexistent) Appendix D of the current document.

## [1.96] - 2011-07-27
### Changed
- Don't expose RFC-to-be links, they are intended to be mainly for an RFC:s authors, for proofing.

## [1.95] - 2011-05-17
### Changed
- Internal links for 'section N.N' text were not generated correctly when there was a line break between 'section' and the section number. Fixed.

## [1.94] - 2011-05-13
### Changed
- Call out to idauthors to get author metainformation to put in DC (Dublin Core) metainformation tags, to improve crawler indexing. This is needed for documents for which the relevant document information isn't already available in the regular metainformation store at `http://tools.ietf.org/draft/<<draftname>>/`

## [1.93] - 2011-05-02
### Changed
- Always provide a link to the datatracker, now that there's always a consistent URL available

## [1.92] - 2011-02-25
### Changed
- Fixed a bug where the an incorrect document name was sometimes used.

## [1.91] - 2011-02-23
### Added
- Added more support for a non-standard reference format which doesn't surround the title of the referenced work with quotes.  This also fixes an issue where the wrong title was shown in the tooltip of the referral.

## [1.90] - 2010-04-30
### Added
- Added code from Julian to eliminate incorrect internal section links when the section reference is to an external document
- Added links to xml2rfc-generated html versions of the documents, if available
### Changed
- Updated the [Tracker] link

## [1.89] - 2010-03-20
### Added
- Added [Email] link to draft authors also for non-wg drafts

## [1.88] - 2010-03-15
### Added
- Added support for 'Section N.n' with internal line break.
### Changed
- Changed the indication of errata to be red, and moved the errata link to the top line.

## [1.87] - 2010-03-03
### Added
- Added support for turning reference lists of the form '[4, 5]' and similar into internal links
- Added support for turning section lists of the form  'Sections 3.5, 3.6 and 3.7' and similar into internal links
### Changed
- Don't emit internal links to references which don't exist
- Only try to find a document title in the first 28 lines of the document, rather than the whole document.  Removes spurious boldface of random text sections in some documents.

## [1.86] - 2010-02-10
### Added
- Added support for supplying extra stylesheet text as an argument.
- Added support for links to RFCs-to-be, to provide diffs useful during auth-48
- Added diff link support for replacement documents

## [1.85] - 2009-10-16
### Changed
- Don't generate multiple DC.Creator tags for the same author.
- Convert encoded representation of single quotes in attributes to plain single quotes.

## [1.84] - 2009-09-10
### Added
- Add the appropriate DC Meta profile= attribute to the &lt;head&gt; element
### Changed
- Fix a potential IndexError exception in setdcmeta()

## [1.83] - 2009-08-12
### Added
- Do html escape of all DC metainformation.

## [1.82] - 2009-08-07
### Added
- Added IE-specific CSS, for better IE display

## [1.81] - 2009-07-31
### Changed
- Not all document types had args['doc'] set.  Fixed.

## [1.80] - 2009-07-16
### Changed
- Refined the handling of URLs broken across two lines.  URLs broken across more than two line are not supported.

## [1.79] - 2009-07-07
### Added
- Added a link to the PDF version of a document to the top menulist.

## [1.78] - 2009-06-29
### Changed
- Fixed a bug in generating google search links for work-in-progress titles when the title already contained links.

## [1.77] - 2009-06-25
### Added
- Added dublin core metadata in HTML meta tags (if available)

## [1.76] - 2009-05-18
### Changed
- Fixed a bug in the handling of RFCs with associated IPR notices.

## [1.75] - 2009-05-14
### Added
- Added diff links to the top-menu for RFCs for which the source draft is known and available.

## [1.74] - 2009-02-17
### Added
- Added a link to IPR disclosures related to the document, if such exist.

## [1.73] - 2008-11-18
### Added
- Now recognizing URLs within parentheses also when not split on two lines...

## [1.72] - 2008-11-11
### Added
- Now recognizing URLs within parentheses.

## [1.71] - 2008-11-01
### Changed
- If a reference listing contained a page break with header and footer, those would be inserted in the title, *and* page break markup added later.  Fixed.

## [1.70] - 2008-10-08
### Changed
- Changed the charset specification in the html from us-ascii to utf-8.
- Changed the html which introduces page breaks when printed to use a `<div>` instead of a `<span>`, in order to work with Safari and Opera. Other minor, related, html tweaks.

## [1.69] - 2008-08-31
### Added
- Added indication of replacement draft, where such information is available

## [1.68] - 2008-08-29
### Added
- Added support for CRT-style underline, using underline and backspace characters.  Idea from Tony Hansen.

## [1.67] - 2008-08-24
### Changed
- Respect fragment identifiers starting with 'draft-', don't process as draft references.

## [1.66] - 2008-07-08
### Added
- Added support for a variation of the Section X.X of [RFCYYYY] markup:  Section X.X [RFCYYY].

## [1.65] - 2008-05-05
### Changed
- BCPs and STDs which contain more than one RFC weren't handled properly with respect to page number links.  Fixed, at the cost of using a different page number anchor name scheme than other documents.  Multi-documents now have fragment identifiers with an added document number:  #page-1-13, #page-2-5, etc.

## [1.64] - 2008-05-02
### Added
- Added some limitation on URLs broken across lines: the ':' character (used for instance between domain and port number) is now only recognized on the first line of the URL, in order to handle consecutive lines of URLs better.
### Changed
- The special handling of RFC 2606 domains (.example, example.com, etc.) used too greedy regexes, and could obliterate non-link text.  Fixed. Thanks to Jim Bell for discovering this problem.

## [1.63] - 2008-04-17
### Changed
- Updated the link to datatracker information about drafts to use the new Django tracker URL rather than the old one.
- Replaced the (slightly useless) [Doc Info] link with a mailto: link to the document authors via the draft-xxx-yyy@tools.ietf.org alias

## [1.62] - 2008-03-28
### Changed
- Limit appendix numbering to one uppercase letter, rather than multiple uppercase letters.

## [1.61] - 2008-03-25
### Changed
- Special-case the Kerberos WG, which is named 'krb-wg' (containing a hyphen) when extracting the WG name from a draft name.
- Moved the top menu down to avoid the color legen click area

## [1.60] - 2008-03-14
### Changed
- Use attrib database rather than name to determine WG (if available)

## [1.59] - 2008-02-26
### Added
- Added @ as a character which may occur in URLs
### Changed
- Fixed a bug in the generation of the page title, where the hyphen between RFC NNNN and the rest of the title would not be emitted.
- Ensured that the current version is listed in the version list, even if not mentioned in the 'versions' file.

## [1.58] - 2008-01-02
### Changed
- Fixed the handling of previous version lists which include previous RFCs or replaced drafts.  Some refactoring.  Added better handling of RFC Titles (taken from metadata db if available).

## [1.57] - 2007-12-05
### Added
- Adding 'title="..."' for RFC references broke the mechanism to provide section links to exteranal references.  Fixed more.

## [1.56] - 2007-12-04
### Added
- Adding 'title="..."' for RFC references broke the mechanism to provide section links to exteranal references.  Fixed.

## [1.55] - 2007-11-25
### Changed
- Tweaked the html and css for the document-type color stripe at the top of the doc info header to work right with IE 7

## [1.54] - 2007-11-25
### Added
- Added generation of diff links for drafts replacing older drafts

## [1.53] - 2007-11-12
### Added
- Added generation of diff links for rfcXXXXbis -00 drafts

## [1.52] - 2007-10-19
### Changed
- Changed URL to the RFC Errata

## [1.51] - 2007-09-21
### Added
- Added section markup for appendices

## [1.50] - 2007-07-17
### Changed
- Changed handling of invisible #page-NN anchors to suit Safari better

## [1.49] - 2007-07-13
### Added
- Added option to change or remove inline stylesheet

## [1.48] - 2007-02-16
### Added
- Added ability to handle multiple comment tags

## [1.47] - 2007-02-14
### Changed
- Minor tweak: Adding tooltip titles to the menubar

## [1.46] - 2007-02-07
### Added
- Added another link to the top menu, after the [Diff1] and [Diff2] links: [Nits].  This generates an on-the-fly nits check using the latest version of idnits.

## [1.45] - 2007-01-21
### Changed
- Changed colour legend handling to set innerHTML by javascript, to avoid legacy browsers always seeing the legend at the top of the page.

## [1.44] - 2007-01-14
### Added
- Added colour coding of the document class, in the form of a coloured line at the very top of the browser page.
- Cleaned up the html to be xhtml transitional compliant.

## [1.43] - 2007-01-03
### Changed
- Don't add http links for example domain names (from rfc 2606, that is).  From Julian Reschke. Add 'noprint' class to the doc info at the page top.

## [1.42] - 2006-12-30
### Changed
- The doc info section at the top of the page now has a grey background instead of white, to more clearly differentiate between the original doc and the information added by rfcmarkup.

## [1.41] - 2006-11-17
### Added
- Added a list of links to other versions for drafts
- If a draft has been published as RFC, added a link to the RFC at the end of the list of draft versions
- Added a link to the draft an RFC came from, if known
### Changed
- More refactoring of header layout code
- Fixed up the `<title/>` to not include draft filename twice
- Various minor bug-fixes

## [1.40] - 2006-11-17
### Added
- Added status indication for RFCs - BCP, PS, DS, STD,...
- Added html `<title/>` to the pages, taken from the doc title
- Added google search links to title of "Work in Progress" references
### Changed
- Refactored header layout code

## [1.39] - 2006-10-11
### Added
- Accept https:// URLs
### Changed
- Link directly from RFC references to the RFC, instead of to the reference section

## [1.38] - 2006-10-11
### Added
- Added tooltips to references, giving the reference title
### Changed
- Topmenu now links to /html instead of to /id for I-Ds
- Cleaned out some old commented-out code

## [1.37] - 2006-10-11
### Added
- Accept `http://` URLs enclosed in `'<'` ... `'>'`.
- Also accept `ftp://` URLs.

## [1.36] - 2006-10-11
### Added
- Added links in the topmenu for [Diff] (drafts only)

## [1.35] - 2006-10-09
### Added
- Added links in the topmenu for [WG] and [Doc Info] (drafts only)

## [1.34] - 2006-09-12
### Added
- Added links in the ToC from the section numbers to the corresponding section in the document.

## [1.33] - 2006-09-05
### Added
- Added handling for http links broken across lines, if the break is at a hyphen.

## [1.32] - 2006-08-22
### Added
- Added a 'topmenu' argument, to avoid adding the top menu when not appropriate.
### Changed
- Keeping `\f`, but making it non-display.  Safari seems to not like empty anchors.
- Use script name rather than hardcoded "index.cgi" in the `<form />`

## [1.31] - 2006-07-28
### Added
- Added wrapping of long "Updated by" lines.
- Added markup for Obsoletes: nnnn and Updates: nnnn

## [1.30] - 2006-07-27
### Added
- Added URL textbox to the form shown when no doc spec. given
### Changed
- Changed `\s` to " " many places -- `\s` includes `\n` ...
- Cleaned out un-used CSS.
- Split out the top menu, using it only when showing a htmlized document.
- Changed the text-only link to have an explicit .txt extension.
- Cleaned out extra whitespace at the end of lines.  This makes it possible to simplify some regexps, and makes other work better.
- Reverted an earlier change to the section number regexp.

## [1.29] - 2006-07-26
### Added
- Added regexps to handle RFC, BCP and draft names which cross lines.
- Added code to ignore section headers containing " . . " or "...".
- Added font-size indications for body and headers (1em)
- Added code to normalize indentation, which makes the section markup code work for more drafts
- Added regexp to boldface also the second line of multi-line document titles
### Changed
- Changed the section header regexp to always require a section number to contain one dot (is this right for old RFCs??)
			
## [1.28] - 2006-07-26
### Added
- Added links to plain text version, rfc repository and ID repository at the top of the page 
- Added .header class to css
- Added javascript code to add `<h?/>` markup for modern browsers.
### Changed
- A number of tweaks to make this look right for non-css browsers while keeping the header structure functionality, plus some other stuff.
- Tweaked the css to make page come out with text placement exactly the same as for the plain-text version for recent RFCs.  For early RFCs and Drafts, all bets are off. 
- Minor tweaks

## [1.27] - 2006-07-24

Based on comments from Frank Ellerman:

### Added
- Added a space before `"/>"` in the self-closing <span/>
- Added lang="en" xml:lang="en" to `<html>`
- Added support for "staticpath" option, to generate static files
### Changed
- Changed character-set to "us-ascii"
### Removed
- Removed the page divider line

## [1.26] - 2006-07-23
### Added
- Added regexp for 'section x of [rfc y]' markup, from Julian Reschke
### Changed
- Also fixed the markup for 'rfc y, section x' to work over line breaks.

## [1.25] - 2006-07-23
### Added
- Added greying out of header and footer lines.
### Changed 
- Changed font size for printed page.  
- Fixed the link to the shortcut icon, when run on the tools server.
- Reverted from using `<div class="pre">` to `<pre>`,  because the `<div/>` version doesn't work with lynx.
### Removed
- Removed name="rfxNNNN" attributes again. 
- Removed link indications in printed page. 

## [1.24] - 2006-07-22
### Added
- Added markup for document title.  Fixed xhtml validation errors.  Added Julian's print output page-break fix.   

## [1.23] - 2006-07-22
### Added
- Header tags for each section header, with header level matching section sub-level.  Used with Firefox' document map plugin this makes navigation very easy.
- Added some css styles to support the use of header tags
### Changed
- Cleaned out unused script code
### Removed
- Removed 'relnotes' from the source, maintaining only the separate changelog.

## [1.22] - 2006-07-13
### Changed
- Tweaked the regexp for http URLs to permit '=' in the URL.

## [1.21] - 2006-07-06
### Changed
- Changed the on-server file path used to look for documents.

## [1.20] - 2006-06-15
### Added
- Added href self-references to pages and sections, so people will see that they are linkable.

## [1.19] - 2006-04-15
### Changed
- Handled case where doc.spec had extension appended.

## [1.18] - 2005-11-04
### Added
- Added more sophisticated handling of paths.  The path component will now be matched against pure numeric, bcpNUM, rfcNUM, draft-STRING, etc. and handled appropriately.

## [1.17] - 2005-11-03
### Added
- Added a html form as output when no RFC number or draft name has been given	

## [1.16] - 2005-08-19
### Added
- Added understanding of FYIs, and when called with path info, added use of the script name to indicate what kind of document is requested.

## [1.15] - 2005-08-04
### Changed
- Changed use of bare "&" in href urls to "&amp;".  Added /body and /html end tags for the non-blurb case.

## [1.14] - 2005-08-02
### Added
- Added title keyword and bcp keyword.  Added markup for bcp references

## [1.12] - 2005-03-04
### Added
- Added robots keyword

## [1.11] - 2005-03-01
### Added
- Added blurb keyword

## [1.10] - 2005-02-15

## [1.08] - 2004-09-17
### Added
- Added re-formatting to fix broken page breaks in some cases (should be `\\n\\f\\n` )

## [1.07] - 2004-07-26
### Changed
- Fixed an xhtml bug.  Added support for "--version" on the command line.

## [1.06] - 2004-07-09
### Added
- Added a `<meta/>` tag to prevent robots invoking the script on a very deep tree (all rfc and draft links...).  
- Added ability to handle relative urls with "url=" keyword.  
- Added error message failure to retrieve url.  
### Changed
- Changed redirection mimetype.
- Changed markup generated for draft to use "draft=" keyword
### Removed
- Removed extra newlines at start of html.

## [1.05] - 2004-04-18
### Changed
- Tweaked reference anchor regexp.

## [1.04] - 2004-04-12
### Added
- Added ability to take rfc number as path info

## [1.03] - 2004-02-25
### Changed
- Tweaked reference link regexp.  Added option "header=0" to make the script omit html header.

## [1.02] - 2004-02-22
### Changed
- Changed position of repository spec. in urls in order to permit use of trailing '...#anchor' in markup urls.
- Also tweaked draft/rfc markup regexps to match.

## [1.01] - 2004-01-28
### Added
- Permitted space before section numbers

## [1.00] - 2003-12-14
### Changed
- Bumped version number to 1.00 and fixed documentation output spacing.

## [0.78] - 2003-12-13
### Added
- Added support for 'rfcNNNN section N.N' type links

## [0.77] - 2003-12-09
### Changed
- Documentation output changed to work better within other html generating tools.

## [0.76] - 2003-12-05
### Changed
- Changed page titles for rfc's to include 'rfc', and for drafts to not include 'draft-'.

## [0.75] - 2003-11-12
### Changed
- Changed the action for non txt/plain input to do a http redirect

## [0.74] - 2003-11-11
### Added
- Added mac-to-unix text format conversion.
### Changed
- Changed regexp for `http://` urls to permit port numbers
- Changed regexp for draft-.. words to not include a final point. 

## [0.70] - 2003-03-04
### Changed
- Changed regexp for section numbers somewhat.

## [0.69] - 2003-03-02
### Changed
- Changed comment colour coding to permit consecutive comments.

## [0.68] - 2003-03-28
### Added
- Added colour coding of comments

## [0.67] - 2002-02-01
### Added
- Added escaping of `'<', '>', '&'`.

## [0.66] - 2002-12-08
### Added
- Testing the Content-type of the original document, instead of looking for `&lt;html&gt;` tag to see if it's ok to proceed with markup. 
- Added javascript to hide email address of maintainer from harvesters.
- Added link to download page to manpage text.
- Added a program signature at the end of markup output.

## [0.65] - 2002-12-06
### Added
- Added markup for section N.N references in text

## [0.64] - 2002-12-05
### Added
- Added version and release notes options

## [0.63] - 2002-12-05
### Added
- Added an option for alternative repository location, and manpage text.

## [0.62] - 2002-12-04
### Changed
- Arranged to handle uppercase roman numerals in page numbers, for RFC 2551.

## [0.61] - 2002-12-03
### Changed
- Changed page link regexp to handle CR LF line endings

## [0.6] - 2002-12-02
### Changed
- Fixed bug in rfc and draft field handling

## [0.5] - 2002-12-01
### Added
- Added page link fixup to table of content

## [0.4] - 2002-12-01
### Added
- Added 2 new query fields, in addtion to the existing url= field: rfc= and draft=

## [0.3] - 2002-11-26
### Added
- Added markup for reference links

## [0.2] - 2002-11-22
### Added
- Added markup for explicit `http://` links

## [0.1] - 2002-11-19
### Added
- Original version, markup for rfc and draft refs

[2.0.1]: https://github.com/ietf-tools/rfc2html/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/ietf-tools/rfc2html/compare/v1.121...v2.0.0
[1.121]: https://github.com/ietf-tools/rfc2html/compare/v1.120...v1.121
[1.120]: https://github.com/ietf-tools/rfc2html/compare/v1.119...v1.120
[1.119]: https://github.com/ietf-tools/rfc2html/compare/v1.118...v1.119
[1.118]: https://github.com/ietf-tools/rfc2html/compare/v1.117...v1.118
[1.117]: https://github.com/ietf-tools/rfc2html/compare/v1.116...v1.117
[1.116]: https://github.com/ietf-tools/rfc2html/compare/v1.108...v1.116
[1.108]: https://github.com/ietf-tools/rfc2html/compare/v1.106...v1.108
[1.106]: https://github.com/ietf-tools/rfc2html/compare/v1.105...v1.106
[1.105]: https://github.com/ietf-tools/rfc2html/compare/v1.104...v1.105
[1.104]: https://github.com/ietf-tools/rfc2html/compare/v1.103...v1.104
[1.103]: https://github.com/ietf-tools/rfc2html/compare/v1.102...v1.103
[1.102]: https://github.com/ietf-tools/rfc2html/compare/v1.101...v1.102
[1.101]: https://github.com/ietf-tools/rfc2html/compare/v1.100...v1.101
[1.100]: https://github.com/ietf-tools/rfc2html/compare/v1.99...v1.100
[1.99]: https://github.com/ietf-tools/rfc2html/compare/v1.98...v1.99
[1.98]: https://github.com/ietf-tools/rfc2html/compare/v1.97...v1.98
[1.97]: https://github.com/ietf-tools/rfc2html/compare/v1.96...v1.97
[1.96]: https://github.com/ietf-tools/rfc2html/compare/v1.95...v1.96
[1.95]: https://github.com/ietf-tools/rfc2html/compare/v1.94...v1.95
[1.94]: https://github.com/ietf-tools/rfc2html/compare/v1.93...v1.94
[1.93]: https://github.com/ietf-tools/rfc2html/compare/v1.92...v1.93
[1.92]: https://github.com/ietf-tools/rfc2html/compare/v1.91...v1.92
[1.91]: https://github.com/ietf-tools/rfc2html/compare/v1.90...v1.91
[1.90]: https://github.com/ietf-tools/rfc2html/compare/v1.89...v1.90
[1.89]: https://github.com/ietf-tools/rfc2html/compare/v1.88...v1.89
[1.88]: https://github.com/ietf-tools/rfc2html/compare/v1.87...v1.88
[1.87]: https://github.com/ietf-tools/rfc2html/compare/v1.86...v1.87
[1.86]: https://github.com/ietf-tools/rfc2html/compare/v1.85...v1.86
[1.85]: https://github.com/ietf-tools/rfc2html/compare/v1.84...v1.85
[1.84]: https://github.com/ietf-tools/rfc2html/compare/v1.83...v1.84
[1.83]: https://github.com/ietf-tools/rfc2html/compare/v1.82...v1.83
[1.82]: https://github.com/ietf-tools/rfc2html/compare/v1.81...v1.82
[1.81]: https://github.com/ietf-tools/rfc2html/compare/v1.80...v1.81
[1.80]: https://github.com/ietf-tools/rfc2html/compare/v1.79...v1.80
[1.79]: https://github.com/ietf-tools/rfc2html/compare/v1.78...v1.79
[1.78]: https://github.com/ietf-tools/rfc2html/compare/v1.77...v1.78
[1.77]: https://github.com/ietf-tools/rfc2html/compare/v1.76...v1.77
[1.76]: https://github.com/ietf-tools/rfc2html/compare/v1.75...v1.76
[1.75]: https://github.com/ietf-tools/rfc2html/compare/v1.74...v1.75
[1.74]: https://github.com/ietf-tools/rfc2html/compare/v1.73...v1.74
[1.73]: https://github.com/ietf-tools/rfc2html/compare/v1.72...v1.73
[1.72]: https://github.com/ietf-tools/rfc2html/compare/v1.71...v1.72
[1.71]: https://github.com/ietf-tools/rfc2html/compare/v1.70...v1.71
[1.70]: https://github.com/ietf-tools/rfc2html/compare/v1.69...v1.70
[1.69]: https://github.com/ietf-tools/rfc2html/compare/v1.68...v1.69
[1.68]: https://github.com/ietf-tools/rfc2html/compare/v1.67...v1.68
[1.67]: https://github.com/ietf-tools/rfc2html/compare/v1.66...v1.67
[1.66]: https://github.com/ietf-tools/rfc2html/compare/v1.65...v1.66
[1.65]: https://github.com/ietf-tools/rfc2html/compare/v1.64...v1.65
[1.64]: https://github.com/ietf-tools/rfc2html/compare/v1.63...v1.64
[1.63]: https://github.com/ietf-tools/rfc2html/compare/v1.62...v1.63
[1.62]: https://github.com/ietf-tools/rfc2html/compare/v1.61...v1.62
[1.61]: https://github.com/ietf-tools/rfc2html/compare/v1.60...v1.61
[1.60]: https://github.com/ietf-tools/rfc2html/compare/v1.59...v1.60
[1.59]: https://github.com/ietf-tools/rfc2html/compare/v1.58...v1.59
[1.58]: https://github.com/ietf-tools/rfc2html/compare/v1.57...v1.58
[1.57]: https://github.com/ietf-tools/rfc2html/compare/v1.56...v1.57
[1.56]: https://github.com/ietf-tools/rfc2html/compare/v1.55...v1.56
[1.55]: https://github.com/ietf-tools/rfc2html/compare/v1.54...v1.55
[1.54]: https://github.com/ietf-tools/rfc2html/compare/v1.53...v1.54
[1.53]: https://github.com/ietf-tools/rfc2html/compare/v1.52...v1.53
[1.52]: https://github.com/ietf-tools/rfc2html/compare/v1.51...v1.52
[1.51]: https://github.com/ietf-tools/rfc2html/compare/v1.50...v1.51
[1.50]: https://github.com/ietf-tools/rfc2html/compare/v1.49...v1.50
[1.49]: https://github.com/ietf-tools/rfc2html/compare/v1.48...v1.49
[1.48]: https://github.com/ietf-tools/rfc2html/compare/v1.47...v1.48
[1.47]: https://github.com/ietf-tools/rfc2html/compare/v1.46...v1.47
[1.46]: https://github.com/ietf-tools/rfc2html/compare/v1.45...v1.46
[1.45]: https://github.com/ietf-tools/rfc2html/compare/v1.44...v1.45
[1.44]: https://github.com/ietf-tools/rfc2html/compare/v1.43...v1.44
[1.43]: https://github.com/ietf-tools/rfc2html/compare/v1.42...v1.43
[1.42]: https://github.com/ietf-tools/rfc2html/compare/v1.41...v1.42
[1.41]: https://github.com/ietf-tools/rfc2html/compare/v1.40...v1.41
[1.40]: https://github.com/ietf-tools/rfc2html/compare/v1.39...v1.40
[1.39]: https://github.com/ietf-tools/rfc2html/compare/v1.38...v1.39
[1.38]: https://github.com/ietf-tools/rfc2html/compare/v1.37...v1.38
[1.37]: https://github.com/ietf-tools/rfc2html/compare/v1.36...v1.37
[1.36]: https://github.com/ietf-tools/rfc2html/compare/v1.35...v1.36
[1.35]: https://github.com/ietf-tools/rfc2html/compare/v1.34...v1.35
[1.34]: https://github.com/ietf-tools/rfc2html/compare/v1.33...v1.34
[1.33]: https://github.com/ietf-tools/rfc2html/compare/v1.32...v1.33
[1.32]: https://github.com/ietf-tools/rfc2html/compare/v1.31...v1.32
[1.31]: https://github.com/ietf-tools/rfc2html/compare/v1.30...v1.31
[1.30]: https://github.com/ietf-tools/rfc2html/compare/v1.29...v1.30
[1.29]: https://github.com/ietf-tools/rfc2html/compare/v1.28...v1.29
[1.28]: https://github.com/ietf-tools/rfc2html/compare/v1.27...v1.28
[1.27]: https://github.com/ietf-tools/rfc2html/compare/v1.26...v1.27
[1.26]: https://github.com/ietf-tools/rfc2html/compare/v1.25...v1.26
[1.25]: https://github.com/ietf-tools/rfc2html/compare/v1.24...v1.25
[1.24]: https://github.com/ietf-tools/rfc2html/compare/v1.23...v1.24
[1.23]: https://github.com/ietf-tools/rfc2html/compare/v1.22...v1.23
[1.22]: https://github.com/ietf-tools/rfc2html/compare/v1.21...v1.22
[1.21]: https://github.com/ietf-tools/rfc2html/compare/v1.20...v1.21
[1.20]: https://github.com/ietf-tools/rfc2html/compare/v1.19...v1.20
[1.19]: https://github.com/ietf-tools/rfc2html/compare/v1.18...v1.19
[1.18]: https://github.com/ietf-tools/rfc2html/compare/v1.17...v1.18
[1.17]: https://github.com/ietf-tools/rfc2html/compare/v1.16...v1.17
[1.16]: https://github.com/ietf-tools/rfc2html/compare/v1.15...v1.16
[1.15]: https://github.com/ietf-tools/rfc2html/compare/v1.14...v1.15
[1.14]: https://github.com/ietf-tools/rfc2html/compare/v1.12...v1.14
[1.12]: https://github.com/ietf-tools/rfc2html/compare/v1.11...v1.12
[1.11]: https://github.com/ietf-tools/rfc2html/compare/v1.10...v1.11
[1.10]: https://github.com/ietf-tools/rfc2html/compare/v1.08...v1.10
[1.08]: https://github.com/ietf-tools/rfc2html/compare/v1.07...v1.08
[1.07]: https://github.com/ietf-tools/rfc2html/compare/v1.06...v1.07
[1.06]: https://github.com/ietf-tools/rfc2html/compare/v1.05...v1.06
[1.05]: https://github.com/ietf-tools/rfc2html/compare/v1.04...v1.05
[1.04]: https://github.com/ietf-tools/rfc2html/compare/v1.03...v1.04
[1.03]: https://github.com/ietf-tools/rfc2html/compare/v1.02...v1.03
[1.02]: https://github.com/ietf-tools/rfc2html/compare/v1.01...v1.02
[1.01]: https://github.com/ietf-tools/rfc2html/compare/v1.00...v1.01
[1.00]: https://github.com/ietf-tools/rfc2html/compare/v0.78...v1.00
[0.78]: https://github.com/ietf-tools/rfc2html/compare/v0.77...v0.78
[0.77]: https://github.com/ietf-tools/rfc2html/compare/v0.76...v0.77
[0.76]: https://github.com/ietf-tools/rfc2html/compare/v0.75...v0.76
[0.75]: https://github.com/ietf-tools/rfc2html/compare/v0.74...v0.75
[0.74]: https://github.com/ietf-tools/rfc2html/compare/v0.70...v0.74
[0.70]: https://github.com/ietf-tools/rfc2html/compare/v0.69...v0.70
[0.69]: https://github.com/ietf-tools/rfc2html/compare/v0.68...v0.69
[0.68]: https://github.com/ietf-tools/rfc2html/compare/v0.67...v0.68
[0.67]: https://github.com/ietf-tools/rfc2html/compare/v0.66...v0.67
[0.66]: https://github.com/ietf-tools/rfc2html/compare/v0.65...v0.66
[0.65]: https://github.com/ietf-tools/rfc2html/compare/v0.64...v0.65
[0.64]: https://github.com/ietf-tools/rfc2html/compare/v0.63...v0.64
[0.63]: https://github.com/ietf-tools/rfc2html/compare/v0.62...v0.63
[0.62]: https://github.com/ietf-tools/rfc2html/compare/v0.61...v0.62
[0.61]: https://github.com/ietf-tools/rfc2html/compare/v0.6...v0.61
[0.6]: https://github.com/ietf-tools/rfc2html/compare/v0.5...v0.6
[0.5]: https://github.com/ietf-tools/rfc2html/compare/v0.4...v0.5
[0.4]: https://github.com/ietf-tools/rfc2html/compare/v0.3...v0.4
[0.3]: https://github.com/ietf-tools/rfc2html/compare/v0.2...v0.3
[0.2]: https://github.com/ietf-tools/rfc2html/compare/v0.1...v0.2
[0.1]: https://github.com/ietf-tools/rfc2html/releases/tag/v0.1
