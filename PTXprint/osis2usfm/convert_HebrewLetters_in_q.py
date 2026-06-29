import re
import glob

# Vzorec za hebrejski blok: [BESEDA א] ali [BESEDA BESEDA א] ipd.
# Ujame [IME_ČRKE hebrejska_črka] - npr. [ALEF א] ali [ŠIN ש]
# Izogne pa se dolgim tekstovnim opombam v oklepajih
HEBREW_BLOCK = r'\[[^\W\d][\w\-]*\s+[\u0590-\u05FF]\]'


def fix_verse_line(line):
    r"""
    Preoblikuje eno \v vrstico:
      \v 1 \p [ALEF א] besedilo [BET ב] besedilo
    →
      \q1 [ALEF א] \v 1 besedilo \q2 [BET ב] besedilo

    Pravila:
    - Obstoječe \q1 / \q2 / \q3 oznake se najprej odstranijo
    - \p takoj za \v N se odstrani (nadomesti ga \q1)
    - Prva hebrejska črka  → \q1 [BLOK] \v N
    - Druga in tretja       → \q2 [BLOK]
    - Vrstice brez hebrejskih blokov se ne spremenijo
    r"""
    verse_match = re.match(r'^(\\v\s+\d+)\s*(\\p\s*)?', line)
    if not verse_match:
        return line

    verse_marker = verse_match.group(1).strip()
    rest = line[verse_match.end():]

    # Počisti obstoječe \q oznake in \p
    rest = re.sub(r'\\q\d\s*', '', rest)
    rest = re.sub(r'\\p\s*', '', rest).strip()

    blocks = list(re.finditer(HEBREW_BLOCK, rest, re.UNICODE))
    if not blocks:
        return line

    result_parts = []
    prev_end = 0

    for i, block in enumerate(blocks):
        before = rest[prev_end:block.start()].strip()

        if i == 0:
            entry = rf'\q1 {block.group()} {verse_marker}'
            if before:
                entry += f' {before}'
            result_parts.append(entry)
        else:
            # Drugi in tretji blok → vedno \q2
            if before:
                result_parts.append(before)
            result_parts.append(rf'\q2 {block.group()}')

        prev_end = block.end()

    tail = rest[prev_end:].strip()
    if tail:
        result_parts.append(tail)

    return ' '.join(result_parts)


def fix_usfm_text(text):
    r"""Obdela celotno besedilo vrstico po vrstico."""
    lines = text.splitlines()
    fixed = []
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\\v\s+\d+', stripped):
            fixed.append(fix_verse_line(stripped))
        else:
            fixed.append(line)
    return '\n'.join(fixed)


def process_file(input_path):
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    result = fix_usfm_text(content)
    with open(input_path, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f'  ✓  {input_path}  (prepisano)')


# ─────────────────────────────────────────────
# GLAVNA LOGIKA
# ─────────────────────────────────────────────
if __name__ == '__main__':

    usfm_files = glob.glob('*.usfm')

    if not usfm_files:
        print('Ni najdenih *.usfm datotek v trenutnem imeniku.')
    else:
        print(f'\n   Zamenja vrstni red Hrebrejskh oklepajev\n   Najdenih {len(usfm_files)} *.usfm datotek:\n')
        for input_file in sorted(usfm_files):
            try:
                process_file(input_file)
            except Exception as e:
                print(f'       ✗  {input_file}  →  NAPAKA: {e}')

    print('\nKončano.')
