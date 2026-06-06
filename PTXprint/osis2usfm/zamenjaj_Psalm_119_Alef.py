import re

def clean_osis_xml(text):
    # 1. Regex, ki varno najde <foreign>...</foreign>
    # <foreign[^>]*>  --> najde začetno značko z vsemi atributi (n=...)
    # ([\s\S]*?)      --> najde ČISTO VSE vmes (tudi nove vrstice in čudne znake)
    # </foreign>     --> najde zaključek
    pattern = r'<foreign[^>]*>([\s\S]*?)</foreign>'
    
    # 2. Zamenja celotno značko samo z vsebino, ki je bila vmes
    # strip() odstrani morebitne odvečne presledke ali nove vrstice
    cleaned_text = re.sub(pattern, lambda m: m.group(1).strip(), text)
    
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
