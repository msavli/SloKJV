import os
import glob

# Nastavljiva vrednost za zamenjavo
P_VALUE = 93

# Mapa z .usfm datotekami (nastavi pot po potrebi)
USFM_DIR = "."

def process_usfm_file(filepath):
    lines = []
    with open(filepath, encoding="utf-8") as f:
        content = f.read().splitlines()

    book_id = None
    current_chapter = None
    last_verse = 0
    results = []

    for line in content:
        stripped = line.strip()

        # Poberi ID knjige iz prve vrstice
        if stripped.startswith("\\id ") and book_id is None:
            book_id = stripped.split()[1]
            continue

        # Nova poglavje
        if stripped.startswith("\\c "):
            parts = stripped.split()
            if len(parts) >= 2 and parts[1].isdigit():
                current_chapter = int(parts[1])
                last_verse = 0  # resetiraj ob novem poglavju
            continue

        # Številka vrstice za \v
        if stripped.startswith("\\v ") and current_chapter is not None:
            parts = stripped.split()
            if len(parts) >= 2 and parts[1].isdigit():
                last_verse = int(parts[1])
            continue

        # \p — zapiši z (zadnja vrstica - 1)
        if stripped == "\\p" and current_chapter is not None and book_id is not None:
            verse_ref = last_verse  # \p je pred naslednjo \v, torej last_verse je pravilna vrednost pred \p
            results.append(f'at {book_id} {current_chapter}:{verse_ref} "\\\\p" > "\\\\p^{P_VALUE}"')

    return book_id, results


def main():
    usfm_files = sorted(glob.glob(os.path.join(USFM_DIR, "*.usfm")))

    if not usfm_files:
        print(f"Ni najdenih .usfm datotek v: {os.path.abspath(USFM_DIR)}")
        return

    all_output = []

    for filepath in usfm_files:
        book_id, results = process_usfm_file(filepath)
        if results:
            all_output.append("\n".join(results))

    print("\n\n".join(all_output))


if __name__ == "__main__":
    main()
