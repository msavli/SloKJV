#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zamenjaj_odstavke_p.py

Pretvori odstavke, zapisane kot XML elementi <p> okoli verzov:

    <chapter ...><title ...>1. Poglavje</title>
    <p><verse osisID="Gen.1.1"> ... </verse><verse osisID="Gen.1.2"> ... </verse></p>
    <p><verse osisID="Gen.1.3"> ... </verse></p>
    </chapter>

v obliko, ki jo pricakuje ostanek skript v run_osis2usfm (enako, kot je
nastala iz <milestone type="x-p" .../>):

    <chapter ...><title ...>1. Poglavje</title>
    <verse osisID="Gen.1.1"> ... </verse><verse osisID="Gen.1.2"> ... </verse>
    <verse osisID="Gen.1.3"> \\p ... </verse>
    </chapter>

Pravila:
  * vsak <p> okoli verzov se odstrani, v njegov prvi verz se vstavi " \\p";
  * prvi <p> v poglavju ne dobi "\\p", ker run_osis2usfm vsakemu "\\c N"
    doda "\\p" sam (sicer bi bil \\p podvojen);
  * <p type="..." ...> z atributi (uvodi knjig) ostanejo nespremenjeni.

Uporaba:
    python3 zamenjaj_odstavke_p.py vhod.xml izhod.xml
"""

import re
import sys

CHAPTER_RE = re.compile(
    r"(?P<open><chapter\b[^>]*>)(?P<body>.*?)(?P<close></chapter\s*>)",
    re.DOTALL | re.IGNORECASE,
)

# <p> brez atributov, ki mu sledi <verse ...>
P_OPEN_RE = re.compile(r"<p>(?P<ws>\s*)(?P<verse><verse\b[^>]*>)", re.IGNORECASE)

# </p>, ki zapira odstavek verzov (pred njim je </verse>)
P_CLOSE_RE = re.compile(r"(?P<verse></verse>)(?P<ws>\s*)</p>", re.IGNORECASE)

PARAGRAPH = " \\p"   # presledek + \p (enako kot prej iz milestone oznake)


def convert_chapter_body(body, stats):
    first = True

    def repl(match):
        nonlocal first
        stats["p"] += 1
        if first:
            first = False
            return match.group("ws") + match.group("verse")
        stats["new_paragraphs"] += 1
        return match.group("ws") + match.group("verse") + PARAGRAPH

    body = P_OPEN_RE.sub(repl, body)
    body = P_CLOSE_RE.sub(lambda m: m.group("verse") + m.group("ws"), body)
    return body


def convert(text):
    stats = {"p": 0, "new_paragraphs": 0}

    def repl_chapter(match):
        return (
            match.group("open")
            + convert_chapter_body(match.group("body"), stats)
            + match.group("close")
        )

    return CHAPTER_RE.sub(repl_chapter, text), stats


def main():
    if len(sys.argv) != 3:
        print("Uporaba: python3 zamenjaj_odstavke_p.py vhod.xml izhod.xml",
              file=sys.stderr)
        return 1

    with open(sys.argv[1], "r", encoding="utf-8", newline="") as f:
        text = f.read()

    converted, stats = convert(text)

    with open(sys.argv[2], "w", encoding="utf-8", newline="") as f:
        f.write(converted)

    # Preostali <p> brez atributov bi pomenil nepričakovano zgradbo XML.
    left_open = len(re.findall(r"<p>", converted))
    left_close = len(re.findall(r"</verse>\s*</p>", converted))
    print(f"      Odstavkov <p> v poglavjih: {stats['p']}  "
          f"(vstavljenih \\p: {stats['new_paragraphs']})")
    if left_open or left_close:
        print(f"      OPOZORILO: ostalo je {left_open} <p> in {left_close} </p> "
              f"okoli verzov - preveri zgradbo XML!", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
