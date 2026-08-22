import re

def clean_osis_xml(text):
    # 1. Regex, ki varno najde <foreign>...</foreign>
    # <foreign[^>]*>  --> najde začetno značko z vsemi atributi (n=...)
    # ([\s\S]*?)      --> najde ČISTO VSE vmes (tudi nove vrstice in čudne znake)
    # </foreign>     --> najde zaključek
    pattern = r'<foreign[^>]*>([\s\S]*?)</foreign>'

    # Hebrejski unicode blok (osnovne črke + niqqud + ligature): U+0590 - U+05FF
    hebrew_pattern = r'([\u0590-\u05FF]+)'

    def replace_foreign(m):
        inner = m.group(1).strip()
        # 2. Znotraj vsebine oklenemo strnjene hebrejske znake z \wh ... \wh*
        inner = re.sub(hebrew_pattern, r'\\wh \1\\wh*', inner)
        return inner

    # 3. Zamenja celotno značko samo z (obdelano) vsebino, ki je bila vmes
    cleaned_text = re.sub(pattern, replace_foreign, text)

    return cleaned_text

# Branje z eksplicitnim kodiranjem
input_file = 'SloKJV_sword.xml'
output_file = 'SloKJV_sword1.xml'

try:
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    result = clean_osis_xml(content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"Uspešno končano. Preveri datoteko {output_file}")
except Exception as e:
    print(f"Napaka: {e}")
