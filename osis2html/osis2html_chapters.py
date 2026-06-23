from lxml import etree
import os
from datetime import datetime

# --- XML Parsing and Setup ---
xml_path = "m:/SloKJVA/SloKJV_sword_removed_apokrif_ref.xml"
try:
    tree = etree.parse(xml_path)
    root = tree.getroot()
    print("\n" + "    " + "="*60)
    print("    KREIRA .html DATOTEKE z osis2html.py")
    print("    " + "="*60)
    print("\n")
    print(f"    Successfully loaded XML from: {xml_path}")
    print(f"    Root element: {root.tag}")
    print("     First few children of root:")
    for i, child in enumerate(root):
        if i < 5:
            print(f"      - {child.tag} (attributes: {child.attrib})")
except Exception as e:
    print(f"Error loading XML from {xml_path}: {e}")
    raise

ns = {"osis": "http://www.bibletechnologies.net/2003/OSIS/namespace"}
# Global counters for study notes and cross-references used inside quotes
study_counter = 0
xref_counter = 0
output_dir = "m:/trgovina_s_knjigami/root"
os.makedirs(output_dir, exist_ok=True)

# --- Book List Extraction ---
books = root.findall(".//osis:div[@type='book']", namespaces=ns)
book_list = []
slovenian_abbr = {
    "Gen": "1 Mz",
    "Exod": "2 Mz",
    "Lev": "3 Mz",
    "Num": "4 Mz",
    "Deut": "5 Mz",
    "Josh": "Joz",
    "Judg": "Sod",
    "Ruth": "Rut",
    "1Sam": "1 Sam",
    "2Sam": "2 Sam",
    "1Kgs": "1 Kr",
    "2Kgs": "2 Kr",
    "1Chr": "1 Krn",
    "2Chr": "2 Krn",
    "Ezra": "Ezr",
    "Neh": "Neh",
    "Esth": "Est",
    "Job": "Job",
    "Ps": "Ps",
    "Prov": "Prg",
    "Eccl": "Prd",
    "Song": "Pp",
    "Isa": "Iz",
    "Jer": "Jer",
    "Lam": "Žal",
    "Ezek": "Ezk",
    "Dan": "Dan",
    "Hos": "Oz",
    "Joel": "Jl",
    "Amos": "Am",
    "Obad": "Abd",
    "Jonah": "Jon",
    "Mic": "Mih",
    "Nah": "Nah",
    "Hab": "Hab",
    "Zeph": "Sof",
    "Hag": "Ag",
    "Zech": "Zah",
    "Mal": "Mal",
    "Matt": "Mt",
    "Mark": "Mr",
    "Luke": "Lk",
    "John": "Jn",
    "Acts": "Apd",
    "Rom": "Rim",
    "1Cor": "1 Kor",
    "2Cor": "2 Kor",
    "Gal": "Gal",
    "Eph": "Ef",
    "Phil": "Flp",
    "Col": "Kol",
    "1Thess": "1 Tes",
    "2Thess": "2 Tes",
    "1Tim": "1 Tim",
    "2Tim": "2 Tim",
    "Titus": "Tit",
    "Phlm": "Flm",
    "Heb": "Heb",
    "Jas": "Jak",
    "1Pet": "1 Pt",
    "2Pet": "2 Pt",
    "1John": "1 Jn",
    "2John": "2 Jn",
    "3John": "3 Jn",
    "Jude": "Jud",
    "Rev": "Raz",
}
for book in books:
    book_id = book.get("osisID")
    title_elem = book.find("osis:title[@type='main']", namespaces=ns)
    short_title = slovenian_abbr.get(book_id, book_id) if title_elem is not None else book_id
    # Add non-breaking space for two-word book names
    if " " in short_title:
        short_title = short_title.replace(" ", "&nbsp;")
    book_list.append((book_id, short_title))

old_testament = book_list[:39]
new_testament = book_list[39:]

# --- Navigation Generation ---
def generate_book_nav(main_title, is_index=False):
    """Vrne vrstico za vključitev navigation_bible.php (skupna nav po knjigah)."""
    return ['<?php require_once __DIR__ . "/navigation_bible.php"; ?>']

# --- Footer Preparation ---
current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
main_title = root.findtext("osis:osisText/osis:header/osis:work/osis:title", default="Sveto pismo Kralja Jakoba (1769) – SloKJV", namespaces=ns)
rights = root.findtext("osis:osisText/osis:header/osis:work/osis:rights[@type='x-copyright']", default="Licenca: CC BY-NC-ND 4.0", namespaces=ns)
source = root.findtext("osis:osisText/osis:header/osis:work/osis:source", default="TextSource=github.com/msavli/SloKJV", namespaces=ns)
source_link = source.replace("TextSource=", "Vir: <a href='https://") + "'>github.com/msavli/SloKJV</a>"
footer_html = [
    f'    <div class="footer">',
    f'      <p>',
    f'         Ustvarjeno:',
    f'          {current_datetime}<br>',
    f'          {rights}<br>',
    f'          {source_link}',
    f'      </p>',
    '    </div>'
]

# --- Index Page Generation ---
header = root.find("osis:osisText/osis:header", namespaces=ns)
if header is None:
    print("No <header> found in XML!")
else:
    print("    Found <header> in XML.")
    work = header.find("osis:work", namespaces=ns)
    if work is None:
        print("No <work> found in <header>!")
    else:
        print("    Found <work> in <header>.")

descriptions = root.findall("osis:osisText/osis:header/osis:work/osis:description", namespaces=ns)
print("    Descriptions found in XML:")
if descriptions:
    for desc in descriptions:
        text = desc.text if desc.text else "(empty)"
        print(f"      {text}")
else:
    print("- No descriptions found! Check XML file path or structure.")

index_content = [
    '<?php',
    '/* ------------------------------------------',
    '   Vključitve & inicializacija',
    '------------------------------------------- */',
    "header('Content-Type: text/html; charset=UTF-8');",
    "if (!defined('SLOKJV_APP')) {",
    "    define('SLOKJV_APP', true); // omogoči varno vključitev config.php",
    '}',
    "require_once __DIR__ . '/../config_biblija.php'; // DB konfiguracija + slokjv_db()",
    'session_start();',
    "// Enable error reporting",
    "ini_set('display_errors', 1);",
    "ini_set('display_startup_errors', 1);",
    'error_reporting(E_ALL);',
    '// Get database connection',
    '$conn = slokjv_db();',
    '// Naključna vrstica se pridobi prek AJAX klica (ne ob nalaganju strani)',
    'if (false) {',
    '    $row = $result->fetch_assoc();',
    '    $random_verse = "<p><a href=\'{$row[\'book\']}.php?ch={$row[\'chapter\']}#{$row[\'chapter\']}.{$row[\'verse\']}\'><strong>{$row[\'book\']} {$row[\'chapter\']},{$row[\'verse\']}</strong></a> {$row[\'text\']}</p>";',
    '} else {',
    '    $random_verse = "<p>Ni podatkov v bazi.</p>";',
    '}',
    '// Naključna vrstica se naloži prek AJAX (nakljucna_vrstica.php)',
    '?>',
    '',
    "<!DOCTYPE html>",
    '<html lang="sl">',
    "  <head>",
    '    <meta charset="UTF-8">',
    '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
    f"    <title>{main_title}</title>",
    '    <link rel="stylesheet" href="./style.css">',
    "  </head>",
    "  <body>",
    "    <a id='top'></a>",
    ' <div class="content">',
    '',
    '<?php require_once __DIR__ . "/meni.php"; ?>',
    '',
] + generate_book_nav(main_title, is_index=True) + [
    '    <div class="center-buttons">',
    '      <input type="text" id="search-input" placeholder="Išči" class="search-input">',
    '      <button id="search-button" class="search-icon-btn" onclick="performSearch()" aria-label="Išči" title="Išči"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg></button>',
    '    </div>',
    '    <div class="random-verse">',
    '      <button id="refresh-verse" onclick="naloziNakljucnoVrstico()">Naključna vrstica</button>',
    '      <div id="random-verse"><em>Klikni gumb za naključno vrstico.</em></div>',
    '    </div>',
    '    <script>',
    '    function naloziNakljucnoVrstico() {',
    '      fetch("nakljucna_vrstica.php")',
    '        .then(r => r.text())',
    '        .then(html => { document.getElementById("random-verse").innerHTML = html; })',
    '        .catch(() => { document.getElementById("random-verse").textContent = "Napaka pri nalaganju."; });',
    '    }',
    '    // Ob prvem nalaganju strani avtomatsko naloži vrstico',
    '    document.addEventListener("DOMContentLoaded", naloziNakljucnoVrstico);',
    '    </script>',
    "    <div class='maps-section'>",
    "      <h2>Zemljevidi</h2>",
    "      <a href='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Ancient_World_Patriarchs_Slo.jpg' target='_blank'>",
    "        <img src='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Ancient_World_Patriarchs_Slo_thumb.jpg' alt='Stari svet patriarhov' class='map-preview'>",
    "      </a>",
    "      <a href='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Exodus_and_Canaan_Conquest_Slo.jpg' target='_blank'>",
    "        <img src='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Exodus_and_Canaan_Conquest_Slo_thumb.jpg' alt='Eksodus in osvajanje Kanaana' class='map-preview'>",
    "      </a>",
    "      <a href='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Paul_Journeys_Slo.jpg' target='_blank'>",
    "        <img src='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Paul_Journeys_Slo_thumb.jpg' alt='Pavlova potovanja' class='map-preview'>",
    "      </a>",
    "      <a href='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Israel_New_Testament_Slo.jpg' target='_blank'>",
    "        <img src='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Israel_New_Testament_Slo_thumb.jpg' alt='Izrael v času Nove zaveze' class='map-preview'>",
    "      </a>",
    "    </div>",
    "    <div>",
    "      <ul>",
    "        <li>Sveto Pismo kralja Jakoba, poznano tudi kot Avtorizirana Verzija</li>",
    "        <li>Posebnosti prevoda:</li>",
    "        <li>- dodane opombe in reference iz KJV 1611 Cambridge edition</li>",
    "        <li>- Jezusove besede izpisane z rdečo</li>",
    "        <li>- [ ] opomba prevajalca, ni v originalu</li>",
    "        <li>- § razlika med besedilom KJV in ostalimi slovenskimi prevodi</li>",
    "      </ul>",
    "      <p>Papirne izvode SloKJV Svetih pisem in ostale knjige lahko naročite v <a href='https://slokjv.si/knjige/'>spletni trgovini.</a> </p>",
    "    </div>",
    ' <?php require_once __DIR__ . \'/footer.php\'; ?>',
    '    <div class="footer">',
    "      <p>",
    f"         Ustvarjeno: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}<br>",
    "          Licenca: CC BY-NC-ND 4.0<br>",
    "          Vir: <a href='https://github.com/msavli/SloKJV'>github.com/msavli/SloKJV</a>",
    "      </p>",
    "    </div>",
    '    <script src="./script.js"></script>',
    '    <script src="./common.js"></script>',
    ' </div>',          # <-- dodano: zapremo .content
    "  </body>",
    "</html>",
]

with open(f"{output_dir}/index.php", "w", encoding="utf-8") as f:
    f.write("\n".join(index_content))
print(f"      Wrote file: {output_dir}/index.php")

# --- Helper Functions ---
def process_note_content(note_elem):
    # Začnemo z začetnim besedilom opombe
    content = note_elem.text if note_elem.text else ""
    
    for child in note_elem:
        tag_name = child.tag.replace(f"{{{ns['osis']}}}", "")
        
        # Obdelava taga <hi type="bold">
        if tag_name == "hi" and child.get("type") == "bold":
            inner_text = child.text if child.text else ""
            content += f"<b>{inner_text}</b>"
        
        # Obdelava taga <divineName> (Gospod)
        elif tag_name == "divineName":
            inner_text = child.text if child.text else ""
            content += f"<span class='small-caps'>{inner_text}</span>"
            
        # Obdelava taga <transChange type="added"> (ležeče)
        elif tag_name == "transChange":
            inner_text = child.text if child.text else ""
            content += f"<i>{inner_text}</i>"
        
        # Če so znotraj taga še drugi elementi (npr. gnezdenje), 
        # bi tukaj lahko dodali rekurzijo, a za OSIS opombe je to dovolj.
        
        # Ključno: dodajanje "tail" besedila, ki sledi zaprtemu tagu
        if child.tail:
            content += child.tail

    # Čiščenje odvečnih presledkov in oklepajev
    content = content.strip()
    if content.startswith("[") and content.endswith("]"):
        content = content[1:-1].strip()
    
    return content

def process_colophon_content(colophon_elem):
    content = colophon_elem.text.strip() if colophon_elem.text and colophon_elem.text.strip() else ""
    for child in colophon_elem:
        if child.tag == f"{{{ns['osis']}}}transChange" and child.get("type") == "added":
            added_text = child.text.strip() if child.text and child.text.strip() else ""
            if content and not content.endswith(" "):
                content += " "
            content += f"<i>{added_text}</i>"
            if child.tail and child.tail.strip():
                tail_text = child.tail.strip()
                if not tail_text.startswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")) and not content.endswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                    content += " "
                content += tail_text
    return content.strip()

def process_quote_element(sub_elem, who, chapter_id):
    quote_content = ""
    if sub_elem.text and sub_elem.text.strip():
        quote_content += sub_elem.text.strip()
    for child in sub_elem:
        if child.tag == f"{{{ns['osis']}}}quote":
            quote_content += " " + (child.text or "").strip()
        elif child.tag == f"{{{ns['osis']}}}transChange" and child.get("type") == "added":
            added_text = child.text.strip() if child.text and child.text.strip() else ""
            if quote_content and not quote_content.endswith(" "):
                quote_content += " "
            quote_content += f"<i>{added_text}</i>"
            if child.tail and child.tail.strip():
                tail_text = child.tail.strip()
                if not tail_text.startswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")) and not quote_content.endswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                    quote_content += " "
                quote_content += tail_text
        elif child.tag == f"{{{ns['osis']}}}note":
            note_type = child.get("type")
            if note_type == "study":
                global study_counter
                study_counter += 1
                study_ref = chr(96 + study_counter)
                note_text = process_note_content(child)
                quote_content += f" <span class='study-container'><span class='study-ref'>{study_ref}</span><span class='study-note hidden' id='study-{chapter_id}-{study_ref}'>[{note_text}]</span></span>"
            elif note_type == "crossReference":
                global xref_counter
                xref_counter += 1
                xref_ref = str(xref_counter)
                refs = child.findall("osis:reference", namespaces=ns)
                ref_texts = []
                for ref in refs:
                    osis_ref = ref.get("osisRef", ref.text or "")
                    ref_book = osis_ref.split(".")[0]
                    chap_verse = ".".join(osis_ref.split(".")[1:])
                    if "-" in chap_verse:
                        chap_verse_target = chap_verse.split("-")[0]
                    elif "." not in chap_verse:
                        chap_verse_target = chap_verse
                    else:
                        chap_verse_target = chap_verse
                    chap_num = chap_verse_target.split('.')[0] if '.' in chap_verse_target else chap_verse_target
                    ref_link = f"<a href='{ref_book}.php?ch={chap_num}#{chap_verse_target}' class='xref-link'>{ref.text or osis_ref}</a>"
                    ref_texts.append(ref_link)
                xref_text = "; ".join(ref_texts)
                quote_content += f" <span class='xref-container'><span class='xref-ref'>{xref_ref}</span><span class='xref-note hidden' id='xref-{chapter_id}-{xref_ref}'>[{xref_text}]</span></span>"
        if child.tag != f"{{{ns['osis']}}}transChange" and child.tail and child.tail.strip():
            tail_text = child.tail.strip()
            if not quote_content.endswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                quote_content += " "
            quote_content += tail_text
    if who == "Jesus":
        return f" <span class='quote-jesus'>{quote_content.strip()}</span> "
    else:
        return f" <span class='quote-other'>{quote_content.strip()}</span> "

def process_title_content(title_elem, chapter_id):
    title_content = title_elem.text.strip() if title_elem.text and title_elem.text.strip() else ""
    study_counter = 0
    xref_counter = 0
    for sub_elem in title_elem:
        if sub_elem.tag == f"{ns['osis']}transChange" and sub_elem.get("type") == "added":
            added_text = sub_elem.text.strip() if sub_elem.text and sub_elem.text.strip() else ""
            if title_content and not title_content.endswith(" "):
                title_content += " "
            title_content += f"<i>{added_text}</i>"
            if sub_elem.tail and sub_elem.tail.strip() and not sub_elem.tail.strip().startswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                title_content += " "
        elif sub_elem.tag == f"{{{ns['osis']}}}divineName":
            divine_text = sub_elem.text.strip() if sub_elem.text and sub_elem.text.strip() else ""
            if title_content and not title_content.endswith(" "):
                title_content += " "
            title_content += f"<span class='small-caps'>{divine_text}</span>"
            if sub_elem.tail and sub_elem.tail.strip() and not sub_elem.tail.strip().startswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                title_content += " "
        elif sub_elem.tag == f"{{{ns['osis']}}}note":
            note_type = sub_elem.get("type")
            title_content = title_content.rstrip()
            if note_type == "study":
                study_counter += 1
                study_ref = chr(97 + ((study_counter - 1) % 26))
                note_text = process_note_content(sub_elem)
                title_content += f"<span class='study-container'><span class='study-ref'>{study_ref}</span><span class='study-note hidden' id='study-{chapter_id}-{study_ref}'>[{note_text}]</span></span>"
            elif note_type == "crossReference":
                xref_counter += 1
                xref_ref = str(xref_counter)
                refs = sub_elem.findall("osis:reference", namespaces=ns)
                ref_texts = []
                for ref in refs:
                    osis_ref = ref.get("osisRef", ref.text or "")
                    ref_book = osis_ref.split(".")[0]
                    chap_verse = ".".join(osis_ref.split(".")[1:])
                    if "-" in chap_verse:
                        chap_verse_target = chap_verse.split("-")[0]
                    else:
                        chap_verse_target = chap_verse
                    chap_num = chap_verse_target.split('.')[0] if '.' in chap_verse_target else chap_verse_target
                    ref_link = f"<a href='{ref_book}.php?ch={chap_num}#{chap_verse_target}' class='xref-link'>{ref.text or osis_ref}</a>"
                    ref_texts.append(ref_link)
                xref_text = "; ".join(ref_texts)
                title_content += f"<span class='xref-container'><span class='xref-ref'>{xref_ref}</span><span class='xref-note hidden' id='xref-{chapter_id}-{xref_ref}'>[{xref_text}]</span></span>"
            if sub_elem.tail and sub_elem.tail.strip() and not sub_elem.tail.strip().startswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                title_content += " "
        if sub_elem.tail and sub_elem.tail.strip():
            title_content += sub_elem.tail.strip()
    return title_content.strip()

# --- Main Processing Loop ---
for i, book in enumerate(books):
    if not isinstance(book, etree._Element):
        print(f"Warning: Expected an XML element for book, got {type(book)} instead, skipping...")
        continue
    
    book_id = book.get("osisID")
    if not book_id:
        print("No osisID found for a book, skipping...")
        continue
    
    print(f"      Processing book: {book_id}")
    
    title_elem = book.find("osis:title[@type='main']", namespaces=ns)
    short_title = slovenian_abbr.get(book_id, book_id) if title_elem is not None else book_id
    full_title = title_elem.text if title_elem is not None and title_elem.text else book_id
    # Add non-breaking space for two-word book names
    if " " in short_title:
        short_title = short_title.replace(" ", "&nbsp;")
    if " " in full_title:
        full_title = full_title.replace(" ", "&nbsp;")
    
    is_old_testament = i < 39  # First 39 books are Old Testament
    
    safe_book_id = book_id.replace(".", "_")
    html_content = [
        "<?php",
        "// Določi trenutno poglavje iz GET parametra",
        "$ch = isset($_GET['ch']) ? max(1, (int)$_GET['ch']) : 1;",
        f"$total_ch = NUM_CHAPTERS_PLACEHOLDER;",
        "if ($ch > $total_ch) { $ch = $total_ch; }",
        "?>",
        "<!DOCTYPE html>",
        '<html lang="sl">',
        "  <head>",
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"    <title><?php echo $ch; ?>. poglavje &ndash; {full_title.replace('&nbsp;', ' ')} ({short_title.replace('&nbsp;', ' ')})</title>",
        f'    <link rel="canonical" href="<?php echo htmlspecialchars(\"{safe_book_id}.php?ch=$ch\"); ?>">',
        '    <link rel="stylesheet" href="./style.css">',
        "  </head>",
        "  <body>",
        "    <a id='top'></a>",
        ' <div class="content">',
        '',
        '<?php require_once __DIR__ . "/meni.php"; ?>',
        '',
    ] + generate_book_nav(main_title, is_index=False) + [
        '    <div class="center-buttons">',
        '      <button id="toggle-study" onclick="toggleStudyNotes()" class="icon-toggle-btn" title="Skrij/Odpri opombe" aria-label="Preklopi opombe"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg></button>',
        '      <button id="toggle-xrefs" onclick="toggleXrefs()" class="icon-toggle-btn" title="Skrij/Odpri reference" aria-label="Preklopi reference"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg></button>',
        '      <input type="text" id="search-input" placeholder="Išči" class="search-input">',
        '      <button id="search-button" class="search-icon-btn" onclick="performSearch()" aria-label="Išči" title="Išči"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg></button>',
        '    </div>',
        f"    <h2>{full_title.replace('&nbsp;', ' ')} ({short_title.replace('&nbsp;', ' ')})</h2>",
    ]
    

    # Najdi vsa poglavja v trenutni knjigi
    chapters = book.findall("osis:chapter", namespaces=ns)

    # Iz osisID (npr. "Ps.150") pridobi samo številko poglavja ("150")
    chapter_nums = [ch.get("osisID", "").split(".")[1] for ch in chapters]
    total_chapters = len(chapters)

    # Navigacija poglavij: vsako poglavje je ?ch=N link
    chapter_nav = (
        " <div class='chapter-nav'>"
        + " ".join(f"<a href='?ch={num}'>{num}</a>" for num in chapter_nums)
        + "</div>"
    )
    html_content.append(chapter_nav)

    print(f"        Found {len(chapters)} chapters in {book_id}")
    for chapter in chapters:
        chapter_id = chapter.get("osisID", "Unknown Chapter")
        chapter_num = chapter_id.split(".")[1]

        # Določi naslov poglavja
        if book_id == "Ps":
            chapter_title = f"Psalm {chapter_num}"
        else:
            chapter_title = f"{short_title.replace('&nbsp;', ' ')}, {chapter_num}. poglavje"

        # PHP if blok - začetek poglavja
        html_content.append(f"<?php if ($ch == {chapter_num}): ?>")

        # Sidro in h3 naslov
        top_link_html = f"""
        <a id='{book_id}.{chapter_num}'></a>
        <h3 id="ch-title">
          <span id='{chapter_num}'>{chapter_title}</span>
        </h3>"""
        html_content.append(top_link_html)

        psalm_title_elem = chapter.find("osis:title[@type='psalm']", namespaces=ns)
        if psalm_title_elem is not None:
            title_content = process_title_content(psalm_title_elem, chapter_id)
            html_content.append(f"    <h3>{title_content}</h3>")

        paragraph = ""
        study_counter = 0
        xref_counter = 0
        poetry_lines = []
        first_verse_in_paragraph = True

        for elem in chapter.iter():
            if elem.tag == f"{{{ns['osis']}}}verse":
                verse_id = elem.get("osisID", "Unknown Verse")
                verse_num = verse_id.split(".")[-1]
                chap_verse_id = ".".join(verse_id.split(".")[1:])
                verse_content = ""
                if elem.text and elem.text.strip():
                    verse_content += elem.text.strip()

                for sub_elem in elem:
                    if sub_elem.tag == f"{{{ns['osis']}}}foreign":
                        # Preverite, če je hebrejska črka (ima atribut n)
                        hebrew_letter = sub_elem.get("n", "")
                        foreign_text = sub_elem.text or ""
                        
                        # Če je hebrejska črka, prikažite v oglatih oklepajih
                        if hebrew_letter and foreign_text:
                            # Pokažemo celoten vsebnik z oglatimi oklepaji
                            display_text = f"{foreign_text.strip()}"
                            # Če želite ohraniti hebrejski znak tudi v oglatih oklepajih:
                            # display_text = f"[{foreign_text.strip()} {hebrew_letter}]"
                        else:
                            display_text = foreign_text.strip() if foreign_text else ""
                        
                        if display_text:
                            # Dodamo kot besedilo v vrstico, ne kot poseben naslov
                            if verse_content and not verse_content.endswith(" "):
                                verse_content += " "
                            verse_content += display_text
                        
                        if sub_elem.tail and sub_elem.tail.strip():
                            if not sub_elem.tail.strip().startswith(" "):
                                verse_content += " "
                            verse_content += sub_elem.tail.strip()
                    elif sub_elem.tag == f"{{{ns['osis']}}}milestone" and sub_elem.get("type") == "x-p":
                        if poetry_lines:
                            html_content.append("    <div class='poetry'>")
                            html_content.extend(poetry_lines)
                            html_content.append("    </div>")
                            poetry_lines = []
                        if paragraph.strip():
                            html_content.append(f"    <p>{paragraph.strip()}</p>")
                            paragraph = ""
                            first_verse_in_paragraph = True
                        if sub_elem.tail and sub_elem.tail.strip():
                            verse_content += " " + sub_elem.tail.strip()
                    elif sub_elem.tag == f"{{{ns['osis']}}}q":
                        who = sub_elem.get("who", "")
                        verse_content += process_quote_element(sub_elem, who, chapter_id)
                        if sub_elem.tail and sub_elem.tail.strip():
                            verse_content += " " + sub_elem.tail.strip()
                    elif sub_elem.tag == f"{{{ns['osis']}}}note":
                        note_type = sub_elem.get("type")
                        verse_content = verse_content.rstrip()
                        if note_type == "study":
                            study_counter += 1
                            study_ref = chr(97 + ((study_counter - 1) % 26))
                            note_text = process_note_content(sub_elem)
                            verse_content += f"<span class='study-container'><span class='study-ref'>{study_ref}</span><span class='study-note hidden' id='study-{chapter_id}-{study_ref}'>[{note_text}]</span></span>"
                        elif note_type == "crossReference":
                            xref_counter += 1
                            xref_ref = str(xref_counter)
                            refs = sub_elem.findall("osis:reference", namespaces=ns)
                            ref_texts = []
                            for ref in refs:
                                osis_ref = ref.get("osisRef", ref.text or "")
                                ref_book = osis_ref.split(".")[0]
                                chap_verse = ".".join(osis_ref.split(".")[1:])
                                if "-" in chap_verse:
                                    chap_verse_target = chap_verse.split("-")[0]
                                else:
                                    chap_verse_target = chap_verse
                                chap_num = chap_verse_target.split('.')[0] if '.' in chap_verse_target else chap_verse_target
                                ref_link = f"<a href='{ref_book}.php?ch={chap_num}#{chap_verse_target}' class='xref-link'>{ref.text or osis_ref}</a>"
                                ref_texts.append(ref_link)
                            xref_text = "; ".join(ref_texts)
                            verse_content += f"<span class='xref-container'><span class='xref-ref'>{xref_ref}</span><span class='xref-note hidden' id='xref-{chapter_id}-{xref_ref}'>[{xref_text}]</span></span>"
                        if sub_elem.tail and sub_elem.tail.strip():
                            verse_content += " " + sub_elem.tail.strip()
                    elif sub_elem.tag == f"{{{ns['osis']}}}transChange" and sub_elem.get("type") == "added":
                        added_text = sub_elem.text.strip() if sub_elem.text and sub_elem.text.strip() else ""
                        if verse_content and not verse_content.endswith((" ", "›", "‹")):
                            verse_content += " "
                        verse_content += f"<i>{added_text}</i>"
                        if sub_elem.tail and sub_elem.tail.strip():
                            tail_text = sub_elem.tail.strip()
                            if not tail_text.startswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")) and not verse_content.endswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                                verse_content += " "
                            verse_content += tail_text
                    elif sub_elem.tag == f"{{{ns['osis']}}}divineName":
                        divine_text = sub_elem.text.strip() if sub_elem.text and sub_elem.text.strip() else ""
                        if verse_content and not verse_content.endswith((" ", "›", "‹")):
                            verse_content += " "
                        verse_content += f"<span class='small-caps'>{divine_text}</span>"
                        if sub_elem.tail and sub_elem.tail.strip():
                            tail_text = sub_elem.tail.strip()
                            if not tail_text.startswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")) and not verse_content.endswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                                verse_content += " "
                            verse_content += tail_text
                    elif sub_elem.tag == f"{{{ns['osis']}}}inscription":
                        inscription_text = sub_elem.text.strip() if sub_elem.text and sub_elem.text.strip() else ""
                        if verse_content and not verse_content.endswith((" ", "›", "‹")):
                            verse_content += " "
                        verse_content += f"<span class='inscription'>{inscription_text}</span>"
                        if sub_elem.tail and sub_elem.tail.strip():
                            tail_text = sub_elem.tail.strip()
                            if not tail_text.startswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")) and not verse_content.endswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                                verse_content += " "
                            verse_content += tail_text
                    else:
                        print(f"Unhandled tag in {verse_id}: {sub_elem.tag}")

                if verse_content.strip():
                    if first_verse_in_paragraph:
                        paragraph += f"<span id='{chap_verse_id}'><sup>{verse_num}</sup> {verse_content.strip()}</span>"
                        first_verse_in_paragraph = False
                    else:
                        paragraph += f" <span id='{chap_verse_id}'><sup>{verse_num}</sup> {verse_content.strip()}</span>"

                if elem.tail and elem.tail.strip():
                    paragraph += " " + elem.tail.strip()

            elif elem.tag == f"{{{ns['osis']}}}lg":
                for line_elem in elem.findall(f"{{{ns['osis']}}}l"):
                    line_text = ""
                    if line_elem.text and line_elem.text.strip():
                        line_text += line_elem.text.strip()
                    for sub_line in line_elem:
                        if sub_line.tag == f"{{{ns['osis']}}}q":
                            who = sub_line.get("who", "")
                            line_text += process_quote_element(sub_line, who, chapter_id)
                        if sub_line.tail and sub_line.tail.strip():
                            line_text += " " + sub_line.tail.strip()
                    if line_text.strip():
                        poetry_lines.append(f"    <div class='poetry-line'>{line_text.strip()}</div>")
                    if line_elem.tail and line_elem.tail.strip():
                        poetry_lines.append(f"    <div class='poetry-line'>{line_elem.tail.strip()}</div>")

        if poetry_lines:
            html_content.append("    <div class='poetry'>")
            html_content.extend(poetry_lines)
            html_content.append("    </div>")
            poetry_lines = []
        if paragraph.strip():
            html_content.append(f"    <p>{paragraph.strip()}</p>")
            paragraph = ""

        colophons = chapter.findall(".//osis:div[@type='colophon']", namespaces=ns)
        for colophon in colophons:
            colophon_text = process_colophon_content(colophon)
            colophon_id = colophon.get("osisID", "")
            if colophon_text:
                if colophon_id:
                    html_content.append(f"    <div class='colophon' id='{colophon_id}'>{colophon_text}</div>")
                else:
                    html_content.append(f"    <div class='colophon'>{colophon_text}</div>")

        # ---- PHP: navigacija prev/next poglavje znotraj if bloka ----
        prev_ch = int(chapter_num) - 1
        next_ch = int(chapter_num) + 1
        prev_book = book_list[i - 1][0] if i > 0 else None
        next_book = book_list[i + 1][0] if i < len(book_list) - 1 else None

        # SVG puščice za navigacijo med poglavji
        SVG_LEFT  = '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>'
        SVG_RIGHT = '<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>'
        SVG_UP    = '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>'

        # Leva puščica (prejšnje poglavje / prejšnja knjiga)
        if prev_ch >= 1:
            prev_arrow = f'<a href="?ch={prev_ch}" class="ch-arrow ch-prev ch-smooth" aria-label="Prejšnje poglavje">{SVG_LEFT}</a>'
        elif prev_book:
            prev_arrow = f'<a href="{prev_book}.php" class="ch-arrow ch-prev" aria-label="Prejšnja knjiga">{SVG_LEFT}</a>'
        else:
            prev_arrow = f'<span class="ch-arrow ch-prev ch-disabled">{SVG_LEFT}</span>'

        # Desna puščica (naslednje poglavje / naslednja knjiga)
        if next_ch <= total_chapters:
            next_arrow = f'<a href="?ch={next_ch}" class="ch-arrow ch-next ch-smooth" aria-label="Naslednje poglavje">{SVG_RIGHT}</a>'
        elif next_book:
            next_arrow = f'<a href="{next_book}.php" class="ch-arrow ch-next" aria-label="Naslednja knjiga">{SVG_RIGHT}</a>'
        else:
            next_arrow = f'<span class="ch-arrow ch-next ch-disabled">{SVG_RIGHT}</span>'

        top_arrow = f'<a href="#top" class="ch-arrow ch-top" title="Na vrh strani" aria-label="Na vrh">{SVG_UP}</a>'

        ch_nav = [
            '    <div class="chapter-prev-next">',
            f'      {prev_arrow}',
            '      <a href="index.php" class="ch-home">Kazalo</a>',
            f'      {next_arrow}',
            f'      {top_arrow}',
            '    </div>',
        ]
        html_content.extend(ch_nav)

        # ---- PHP: konec if bloka za to poglavje ----
        html_content.append(f"<?php endif; // ch == {chapter_num} ?>")

    # Colophon na nivoju knjige (ne poglavja) - prikazan vedno
    colophons = book.findall(".//osis:div[@type='colophon']", namespaces=ns)
    has_colophon = False

    for colophon in colophons:
        colophon_text = process_colophon_content(colophon)
        colophon_id = colophon.get("osisID", "")
        if colophon_text:
            has_colophon = True
            if colophon_id:
                html_content.append(
                    f"    <div class='colophon' id='{colophon_id}'>{colophon_text}</div>"
                )
            else:
                html_content.append(
                    f"    <div class='colophon'>{colophon_text}</div>"
                )

    # (global-top-link ni več potreben – ↑ je v chapter-prev-next)

    html_content.extend(footer_html)
    html_content.extend([
    '    <script src="./script.js"></script>',
    '    <script src="./common.js"></script>',
    '    <script>',
    '    /* Gladka navigacija: ob kliku ch-smooth se stran naloži in prikaže pri h3#ch-title */',
    '    document.querySelectorAll("a.ch-smooth").forEach(function(link) {',
    '      link.addEventListener("click", function(e) {',
    '        e.preventDefault();',
    '        window.location = this.href + "#ch-title";',
    '      });',
    '    });',
    '    window.addEventListener("DOMContentLoaded", function() {',
    '      if (window.location.hash === "#ch-title") {',
    '        var h3 = document.getElementById("ch-title");',
    '        if (h3) setTimeout(function() { h3.scrollIntoView({ behavior: "auto", block: "start" }); }, 50);',
    '      }',
    '    });',
    '    </script>',
    ' </div>',
    "  </body>",
    "</html>",
    ])

    # Zapiši .php datoteko in popravi NUM_CHAPTERS_PLACEHOLDER
    file_content = "\n".join(html_content)
    file_content = file_content.replace("NUM_CHAPTERS_PLACEHOLDER", str(total_chapters))

    file_path = f"{output_dir}/{safe_book_id}.php"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)
    print(f"        Wrote file: {file_path}")

print(f"    PHP files generated in {output_dir}/")

print("\n" + "    " + "="*60)
print("    KONCAL KREIRANJE .php DATOTEK z osis2html.py")
print("    " + "="*60)
print("\n")