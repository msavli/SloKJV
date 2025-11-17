#!/home/melmoth/dev/swordstuff/bin/python
# -*- coding: utf-8 -*-

import Sword
import sys
from jinja2 import Template, FileSystemLoader, Environment
from functools import lru_cache

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)

def printf_format(value, format_spec):
    return format(int(value), format_spec)

env.filters['printf'] = printf_format


def getAllBooks(versification="KJV"):
    vk = Sword.VerseKey()
    vk.setVersificationSystem(versification)
    out = []
    for i in range(1, 3):
        vk.setTestament(i)
        for j in range(1, vk.bookCount(i) + 1):
            vk.setBook(j)
            tmp = {}
            tmp['name'] = vk.bookName(i, j)
            tmp['abbr'] = vk.getBookAbbrev()
            tmp['testament'] = i
            tmp['bookCount'] = j
            out.append(tmp)
    return out

def getInfoBasedOnAbbr(abbr):
    for cur in getAllBooks(versification):
        if cur['abbr'] == abbr:
            return cur
    sys.exit("no such book : %s" % abbr)

def getVerseMax(moduleName, bookName, chapterNbr, mgr):
    mod = mgr.getModule(moduleName)
    versification = mod.getConfigEntry("Versification")
    vk = Sword.VerseKey()
    vk.setVersificationSystem(versification)
    vk.setBookName(bookName)
    vk.setChapter(chapterNbr)
    return vk.getVerseMax()

def getNbrChapter(moduleName, bookAbbr, mgr):
    mod = mgr.getModule(moduleName)
    versification = mod.getConfigEntry("Versification")
    vk = Sword.VerseKey()
    vk.setVersificationSystem(versification)
    targetBook = next((b for b in getAllBooks(versification) if b["abbr"] == bookAbbr), None)
    return vk.chapterCount(targetBook['testament'], targetBook['bookCount'])

@lru_cache(maxsize=None)
def get_verse(bookStr, chapterInt, verseNbr, moduleName, mgr):
    mod = mgr.getModule(moduleName)
    versification = mod.getConfigEntry("Versification")
    vk = Sword.VerseKey()
    vk.setVersificationSystem(versification)
    vk.setBookName(bookStr)
    vk.setChapter(chapterInt)
    vk.setVerse(verseNbr)
    mod.setKey(vk)
    mgr.setGlobalOption("Hebrew Vowel Points", "Off")
    mgr.setGlobalOption("Hebrew Cantillation", "Off")
    mgr.setGlobalOption("Strong's Numbers", "Off")
    mgr.setGlobalOption("Headings", "Off")
    mgr.setGlobalOption("Footnotes", "Off")
    mgr.setGlobalOption("Textual Variants", "On")
    mgr.setGlobalOption("Morphological Tags", "Off")
    mgr.setGlobalOption("Lemmas", "Off")
    mgr.setGlobalOption("Greek Accents", "Off")
    return mod.renderText()

def bookPrefix(bookAbbr):
    cnt = 1
    for b in getAllBooks(versification):
        if b["abbr"] == bookAbbr:
            return cnt
        cnt += 1
    return 0

def createChapter(moduleName, bookAbbr, mgr, chapter):
    bookName = getInfoBasedOnAbbr(bookAbbr)["name"]
    config = Sword.SWConfig("/home/pc/Dokumenti/GitHub/SloKJV/ePUB/templates/sl-utf8.conf")
    book_full_name = config.get("Text", bookName)

    curChapter = {}
    curChapter["bookname"] = book_full_name
    curChapter["id"] = "%s-%s" % (bookAbbr, chapter)
    curChapter["nbr"] = chapter
    curChapter["verses"] = []

    verseMax = getVerseMax(moduleName, bookAbbr, chapter, mgr)
    for verseInd in range(verseMax):
        verseNbr = verseInd + 1
        verseContent = get_verse(bookAbbr, chapter, verseNbr, moduleName, mgr)
        curChapter["verses"].append({
            "content": verseContent.getRawData(),
            "nbr": str(verseNbr),
            "osisId": "%s %s:%s" % (bookAbbr, chapter, verseNbr)
        })

    prefix = int(bookPrefix(bookAbbr)) + tocOffset
    fileOutput = f"html/{prefix:02d}-{bookAbbr}-{chapter:04d}.html"
    chapterTemplate = env.get_template("chapter.html")
    chapterOutput = chapterTemplate.render(chapter=curChapter)
    with open(fileOutput, "w") as f:
        f.write(chapterOutput)
    return curChapter

# --- Glavni del ---
outputType = Sword.FMT_PLAIN
markup = Sword.MarkupFilterMgr(outputType)
markup.thisown = False
mgr = Sword.SWMgr(markup)

moduleName = "SloKJV"
mod = mgr.getModule(moduleName)
versification = mod.getConfigEntry("Versification")
moduleLang = mod.getConfigEntry("Lang")

toc = []
toc.append({"navpointId": "1", "playOrderId": "1", "name": "Kazalo knjig", "file": "01-toc.html"})
toc.append({"navpointId": "2", "playOrderId": "2", "name": "Kolofon in predgovor", "file": "02-foreword.html"})
toc.append({"navpointId": "3", "playOrderId": "3", "name": "Jezus, reši me!", "file": "03-jezus.html"})

tocOffset = 3
uniqueID = tocOffset + 1

# Dodaj knjige v TOC (brez ustvarjanja datotek!)
for cur in getAllBooks(versification):
    if cur['testament'] == 4:
        continue
    bookAbbr = cur["abbr"]
    prefix = int(bookPrefix(bookAbbr)) + tocOffset

    # Dodaj knjigo v TOC
    curBook = {
        "file": f"{prefix:02d}-{bookAbbr}.html",
        "name": Sword.SWConfig("/home/pc/Dokumenti/GitHub/SloKJV/ePUB/templates/sl-utf8.conf").get("Text", getInfoBasedOnAbbr(bookAbbr)["name"]),
        "navpointId": uniqueID,
        "playOrderId": uniqueID,
        "chapters": []
    }
    uniqueID += 1
    toc.append(curBook)

    # Ustvari poglavja in dodaj v TOC
    for chapterInd in range(getNbrChapter(moduleName, bookAbbr, mgr)):
        chapter = chapterInd + 1
        chapterData = createChapter(moduleName, bookAbbr, mgr, chapter)

        curChapter = {
            "navpointId": uniqueID,
            "playOrderId": uniqueID,
            "name": f"{chapterData['bookname']} {chapter}",
            "file": f"{prefix:02d}-{bookAbbr}-{chapter:04d}.html"
        }
        uniqueID += 1
        toc[-1]["chapters"].append(curChapter)

# Ustvari TOC datoteke
tocTemplate = env.get_template("toc.ncx")
with open("toc.ncx", "w") as f:
    f.write(tocTemplate.render(books=toc))

htmlTocTemplate = env.get_template("toc.html")
with open("html/01-toc.html", "w") as f:
    f.write(htmlTocTemplate.render(books=toc))
