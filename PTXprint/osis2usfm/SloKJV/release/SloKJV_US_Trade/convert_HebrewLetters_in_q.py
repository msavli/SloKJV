import re
import glob

# Vzorec za hebrejski blok: [BESEDA א] ali [BESEDA BESEDA א] ipd.
HEBREW_BLOCK = r'\[[A-Z\-]+ [^\]]+\]'


def fix_verse_line(line):
    """
    Preoblikuje eno \v vrstico:
      \v 1 \p [ALEF א] besedilo [BET ב] besedilo
    →
      \q1 [ALEF א] \v 1 besedilo \q2 [BET ב] besedilo

    Pravila:
    - \p takoj za \v N se odstrani (nadomesti ga \q1)
    - Prva hebrejska črka  → \q1 [BLOK] \v N
    - Druga hebrejska črka → \q2 [BLOK]
    - Tretja in naprej      → \q3 [BLOK]  (za robne primere)
    - Vrstice brez hebrejskih blokov se ne spremenijo
    """
    # Ujemi \v N (in morebitni \p za njim)
    verse_match = re.match(r'^(\\v\s+\d+)\s*(\\p\s*)?', line)
    if not verse_match:
        return line

    verse_marker = verse_match.group(1).strip()   # npr. \v 1
    rest = line[verse_match.end():]               # preostanek brez \v N in \p

    # Najdi vse hebrejske bloke
    blocks = list(re.finditer(HEBREW_BLOCK, rest))
    if not blocks:
        return line  # Ni hebrejskih blokov → pusti kot je

    result_parts = []
    prev_end = 0

    for i, block in enumerate(blocks):
        # Besedilo pred tem blokom
        before = rest[prev_end:block.start()]
        before = re.sub(r'\\p\s*', '', before).strip()  # počisti \p

        if i == 0:
            # PRVI blok: \q1 [BLOK] \v N  (+ morebitno besedilo pred blokom)
            entry = rf'\q1 {block.group()} {verse_marker}'
            if before:
                entry += f' {before}'
            result_parts.append(entry)
        else:
            # NADALJNJI bloki: \q2, \q3, …
            q_level = min(i + 1, 3)          # q2 za drugi, q3 za tretji+
            if before:
                result_parts.append(before)
            result_parts.append(rf'\q{q_level} {block.group()}')

        prev_end = block.end()

    # Preostanek za zadnjim blokom
    tail = rest[prev_end:].strip()
    if tail:
        result_parts.append(tail)

    return ' '.join(result_parts)


def fix_usfm_text(text):
    """Obdela celotno besedilo vrstico po vrstico."""
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

    # Poišči vse *.usfm datoteke v trenutnem imeniku
    usfm_files = glob.glob('*.usfm')

    if not usfm_files:
        print('Ni najdenih *.usfm datotek v trenutnem imeniku.')
    else:
        print(f'Najdenih {len(usfm_files)} *.usfm datotek:\n')
        for input_file in sorted(usfm_files):
            try:
                process_file(input_file)
            except Exception as e:
                print(f'  ✗  {input_file}  →  NAPAKA: {e}')

    print('\nKončano.')
