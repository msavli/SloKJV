import re

# ─────────────────────────────────────────────
# KORAK 1: Očisti <foreign> značke iz XML
# ─────────────────────────────────────────────
def clean_osis_xml(text):
    pattern = r'<foreign[^>]*>([\s\S]*?)</foreign>'
    cleaned_text = re.sub(pattern, lambda m: m.group(1).strip(), text)
    return cleaned_text


# ─────────────────────────────────────────────
# KORAK 2: Pretvori XML v UFT format
# (to je obstoječa logika tvojih skript –
#  tukaj jo poenostavljeno nakažemo)
# ─────────────────────────────────────────────
def xml_to_uft(text):
    """
    Predpostavlja, da obstoječe skripte že pretvorijo XML v UFT.
    Ta funkcija je mesto, kjer se to zgodi – vrne UFT besedilo.
    Ker te skripte niso priložene, jo pustimo kot placeholder.
    """
    return text


# ─────────────────────────────────────────────
# KORAK 3: Popravi vrstice v UFT formatu
#
# Vhod (en primer vrstice):
#   \v 1 \p [ALEF א] Hvalite... \nd Gospoda\nd*, [BET ב] \add ki\add*...
#
# Izhod:
#   \q1 [ALEF א] \v 1 Hvalite... \nd Gospoda\nd*, \q2 [BET ב] \add ki\add*...
# ─────────────────────────────────────────────

# Vzorec za hebrejski blok: [BESEDA א] ali [BESEDA BESEDA א] ipd.
HEBREW_BLOCK = r'\[[A-Z\-]+ [^\]]+\]'

def fix_uft_verse_line(line):
    """
    Preoblikuje eno \v vrstico UFT formata:
    - Pred vsak hebrejski blok doda \q1 (prvi) ali \q2 (drugi, tretji…)
    - \v N prestavi takoj za prvi hebrejski blok (\q1)
    - Odstrani \p znotraj vrstice (ker je \q1/\q2 nadomesti)
    """

    # Ujemi začetek vrstice: \v ŠTEVILKA (s presledki in morebitnim \p)
    verse_match = re.match(r'^(\\v\s+\d+)\s*(\\p\s*)?', line)
    if not verse_match:
        return line  # Ni \v vrstice – pusti kot je

    verse_marker = verse_match.group(1).strip()   # npr. \v 1
    rest = line[verse_match.end():]               # preostanek brez \v N in \p

    # Najdi vse hebrejske bloke in njihove pozicije
    blocks = list(re.finditer(HEBREW_BLOCK, rest))

    if not blocks:
        return line  # Ni hebrejskih blokov – pusti kot je

    result_parts = []
    prev_end = 0

    for i, block in enumerate(blocks):
        # Besedilo PRED tem hebrejskim blokom
        before = rest[prev_end:block.start()]

        # Počisti morebitni \p in odvečne presledke v vmesnem besedilu
        before = re.sub(r'\\p\s*', '', before).strip()

        if i == 0:
            # PRVI hebrejski blok:
            # → \q1 [HEBREJSKI BLOK] \v N besedilo_pred_naslednjim_blokom
            q_marker = r'\q1'
            result_parts.append(f'{q_marker} {block.group()} {verse_marker}')
            if before:
                # Če je kaj besedila pred prvim blokom (redko), ga dodamo za \v N
                result_parts[-1] += f' {before}'
        else:
            # DRUGI, TRETJI… hebrejski blok:
            # → besedilo_pred + \q2 [HEBREJSKI BLOK]
            q_marker = r'\q2' if i == 1 else r'\q3'
            if before:
                result_parts.append(before)
            result_parts.append(q_marker + ' ' + block.group())

        prev_end = block.end()

    # Preostanek besedila za zadnjim hebrejskim blokom
    tail = rest[prev_end:].strip()
    if tail:
        result_parts.append(tail)

    return ' '.join(result_parts)


def fix_uft_file(text):
    """Obdela celotno UFT besedilo vrstico po vrstico."""
    lines = text.splitlines()
    fixed = []
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\\v\s+\d+', stripped):
            fixed.append(fix_uft_verse_line(stripped))
        else:
            fixed.append(line)
    return '\n'.join(fixed)


# ─────────────────────────────────────────────
# GLAVNA LOGIKA
# ─────────────────────────────────────────────
if __name__ == '__main__':

    # --- KORAK 1: Očisti XML ---
    xml_input  = 'SloKJV_sword.xml'
    xml_output = 'SloKJV_sword1.xml'

    try:
        with open(xml_input, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        cleaned_xml = clean_osis_xml(content)

        with open(xml_output, 'w', encoding='utf-8') as f:
            f.write(cleaned_xml)

        print(f'[1/2] XML očiščen → {xml_output}')

    except Exception as e:
        print(f'Napaka pri XML: {e}')
        raise

    # --- KORAK 2: Popravi UFT datoteko ---
    # Predpostavljamo, da tvoje obstoječe skripte že ustvarijo UFT datoteko.
    # Tukaj jo samo preberemo in popravimo \q1/\q2 strukturo.

    uft_input  = 'SloKJV_sword.uft'   # ← UFT datoteka iz tvojih obstoječih skript
    uft_output = 'SloKJV_sword_q.uft' # ← končni izhod s \q1/\q2

    try:
        with open(uft_input, 'r', encoding='utf-8', errors='ignore') as f:
            uft_content = f.read()

        fixed_uft = fix_uft_file(uft_content)

        with open(uft_output, 'w', encoding='utf-8') as f:
            f.write(fixed_uft)

        print(f'[2/2] UFT popravljen → {uft_output}')

    except FileNotFoundError:
        print(f'UFT datoteka "{uft_input}" ni najdena.')
        print('Zaženi najprej svoje obstoječe skripte, ki ustvarijo UFT,')
        print('nato pa poženi to skripto za \q1/\q2 popravek.')
    except Exception as e:
        print(f'Napaka pri UFT: {e}')
        raise
