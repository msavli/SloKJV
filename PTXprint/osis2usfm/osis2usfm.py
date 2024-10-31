#!/usr/bin/env python

# osis2usfm.py
# OSIS to USFM transformation script.
#
# Copyright (C) 2012 Jaakko Luttinen
#
# This file is licensed under Version 3.0 of the GNU General Public
# License.

"""
Python script for transforming Bible in OSIS format to USFM format.
The script transforms OSIS Bible to USFM Bible. It is assumed that the
XML structure of the OSIS file is:

    <osis>
      <osisText>
        <header>
          ... this is ignored ...
        </header>
        <div type="x-testament">
          <div type="book">
            <chapter>
              <verse>
              </verse>
              ...
            </chapter>
            ...
          </div>
        </div>
        <div type="x-testament">
          <div type="book">
            <chapter>
              <verse>
              </verse>
              ...
            </chapter>
            ...
          </div>
        </div>
      </osisText>
    </osis>

No other tags are understood, thus it is a very simple transformation.

Usage:

    python osis2usfm.py inputfile.osis

Outputs a set of files named inputfile_##_XXX.usfm where ## is the
number of the book and XXX is the id of the book.

It is also possible to give the names of the books as a separate text
file. This file should have syntax:

    GEN=Genesis
    EXO=Exodus
    ...
    XXX=Whatever name you want to give to the book
    ...

where XXX is the ID of the book.  Usage:

    python osis2usfm.py inputfile.osis booknames.txt

"""

import xml.etree.ElementTree as ET
import codecs
import sys
from os.path import splitext

filename = sys.argv[1]
basename = splitext(filename)[0]

# Parse XML
tree = ET.parse(filename)

root = tree.getroot()

# Book IDs
ids = (
    'GEN',
    'EXO',
    'LEV',
    'NUM',
    'DEU',
    'JOS',
    'JDG',
    'RUT',
    '1SA',
    '2SA',
    '1KI',
    '2KI',
    '1CH',
    '2CH',
    'EZR',
    'NEH',
    'EST',
    'JOB',
    'PSA',
    'PRO',
    'ECC',
    'SNG',
    'ISA',
    'JER',
    'LAM',
    'EZK',
    'DAN',
    'HOS',
    'JOL',
    'AMO',
    'OBA',
    'JON',
    'MIC',
    'NAM',
    'HAB',
    'ZEP',
    'HAG',
    'ZEC',
    'MAL',
    '___',
    'MAT',
    'MRK',
    'LUK',
    'JHN',
    'ACT',
    'ROM',
    '1CO',
    '2CO',
    'GAL',
    'EPH',
    'PHP',
    'COL',
    '1TH',
    '2TH',
    '1TI',
    '2TI',
    'TIT',
    'PHM',
    'HEB',
    'JAS',
    '1PE',
    '2PE',
    '1JN',
    '2JN',
    '3JN',
    'JUD',
    'REV',
)

# Use booknames if given
booknames = {}
if len(sys.argv) >= 3:
    # namefile = open(sys.argv[2])
    namefile = codecs.open(sys.argv[2],
                           mode='r',
                           encoding='utf-8')
    while True:
        line = namefile.readline()
        if not line:
            break
        pass  # do something    while
        (id, name) = line.split("=")
        booknames[id] = unicode.strip(name)
    namefile.close()

id_ind = 0
for testament in root[0][1:]:
    for (book_ind, book) in enumerate(testament):
        # Write each book in a separate file
        outfile = ('%02d_' % (id_ind+1)) + ids[id_ind] + '.usfm'
        f = codecs.open(outfile,
                        mode='w',
                        encoding='utf-8')

        f.write(u"\\id " + ids[id_ind] + "\n")
        if ids[id_ind] in booknames and booknames[ids[id_ind]]:
            f.write(u"\\h  " + booknames[ids[id_ind]] + u"\n")
            f.write(u"\\h1 " + booknames[ids[id_ind]] + u"\n")
            f.write(u"\\toc2 " + booknames[ids[id_ind]] + u"\n")
            f.write(u"\\mt1 " + booknames[ids[id_ind]] + u"\n")
        else:
            f.write(u"\\h  \n")
            f.write(u"\\h1 \n")
            f.write(u"\\toc1 \n")
            f.write(u"\\toc2 \n")
            f.write(u"\\toc3 \n")
            f.write(u"\\mt1 \n")
        for (chapter_ind, chapter) in enumerate(book):
            f.write(u"\\c %d\n" % (chapter_ind+1))
#            f.write(u"\\p \n")   #  Paratex se ne strinja z \p
            for (verse_ind, verse) in enumerate(chapter):
                f.write(u"\\v %d " % (verse_ind+1))
                if verse.text:
                   f.write(verse.text)
        id_ind += 1

        f.close()
