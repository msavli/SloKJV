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
output_dir = "m:/trgovina_s_knjigami/root"
os.makedirs(output_dir, exist_ok=True)

# --- Book List Extraction ---
books = root.findall(".//osis:div[@type='book']", namespaces=ns)
book_list = []
for book in books:
    book_id = book.get("osisID")
    title_elem = book.find("osis:title[@type='main']", namespaces=ns)
    short_title = title_elem.get("short", book_id) if title_elem is not None else book_id
    # Add non-breaking space for two-word book names
    if " " in short_title:
        short_title = short_title.replace(" ", "&nbsp;")
    book_list.append((book_id, short_title))

old_testament = book_list[:39]
new_testament = book_list[39:]

# --- Navigation Generation ---
def generate_book_nav(main_title, is_index=False):
    if is_index:
        title_line = f'    <h1>{main_title}</h1>'
    else:
        title_line = f'    <h1><a href="index.php">{main_title}</a></h1>'
    nav_html = [
        title_line,
        '    <div class="book-nav">',
        '      <h3>Stara zaveza</h3>',
        '      <p>' + "  ".join(f'<a href="{book_id}.html">{short_title}</a>' for book_id, short_title in old_testament) + '</p>',
        '      <h3>Nova zaveza</h3>',
        '      <p>' + "  ".join(f'<a href="{book_id}.html">{short_title}</a>' for book_id, short_title in new_testament) + '</p>',
        '    </div>'
    ]
    return nav_html

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
    '// Poizvedba za izbiro naključne vrstice',
    '$sql = "SELECT book, chapter, verse, text FROM verses ORDER BY RAND() LIMIT 1";',
    '$result = $conn->query($sql);',
    '$random_verse = "";',
    'if ($result->num_rows > 0) {',
    '    $row = $result->fetch_assoc();',
    '    $random_verse = "<p><a href=\'{$row[\'book\']}.html#{$row[\'chapter\']}.{$row[\'verse\']}\'><strong>{$row[\'book\']} {$row[\'chapter\']}:{$row[\'verse\']}</strong></a> {$row[\'text\']}</p>";',
    '} else {',
    '    $random_verse = "<p>Ni podatkov v bazi.</p>";',
    '}',
    '$conn->close();',
    '?>',
    '',
    "<!DOCTYPE html>",
    '<html lang="sl">',
    "  <head>",
    '    <meta charset="UTF-8">',
    '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
    f"    <title>{main_title}</title>",
    '    <link rel="stylesheet" href="./style.css">',
    '    <script>',
    '      (function() {',
    '        const savedTheme = localStorage.getItem("theme");',
    '        if (savedTheme === "night") {',
    '          document.documentElement.classList.add("night-mode");',
    '        }',
    '      })();',
    '    </script>',
    "  </head>",
    "  <body>",
    '',
    # === NOV MENI IN TEMA GUMB (tukaj vstavljeno) ===
    ' <div class="menu-container">',
    '     <button class="menu-toggle" onclick="toggleMenu(event)" aria-label="Odpri meni">',
    '         <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
    '             <line x1="3" y1="6" x2="21" y2="6"></line>',
    '             <line x1="3" y1="12" x2="21" y2="12"></line>',
    '             <line x1="3" y1="18" x2="21" y2="18"></line>',
    '         </svg>',
    '     </button>',
    '     <div id="dropdownMenu" class="dropdown-menu">',
    '         <ul>',
    '             <li><a href="index.php">Domov</a></li>',
    '             <li><a href="knjige/index.php">Spletni viri in naročila knjig</a></li>',
    '             <li><a href="knjige/Jezus.php">Jezus</a></li>',
    '             <li><a href="knjige/o_nas.php">O nas</a></li>',
    '         </ul>',
    '     </div>',
    ' </div>',
    ' <!-- TEMA GUMB (desno zgoraj) -->',
    ' <div class="theme-toggle-container">',
    '     <button type="button" id="toggle-mode" onclick="toggleMode()" aria-label="Preklopi nočni/dnevni način">',
    '         <svg id="theme-icon-sun" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
    '             <circle cx="12" cy="12" r="5"></circle>',
    '             <line x1="12" y1="1" x2="12" y2="3"></line>',
    '             <line x1="12" y1="21" x2="12" y2="23"></line>',
    '             <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>',
    '             <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>',
    '             <line x1="1" y1="12" x2="3" y2="12"></line>',
    '             <line x1="21" y1="12" x2="23" y2="12"></line>',
    '             <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>',
    '             <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>',
    '         </svg>',
    '         <svg id="theme-icon-moon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
    '             <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>',
    '         </svg>',
    '     </button>',
    ' </div>',
    '',
] + generate_book_nav(main_title, is_index=True) + [
    '    <div class="center-buttons">',
    '      <input type="text" id="search-input" placeholder="Vpiši iskalni niz" class="search-input">',
    '      <button id="search-button" onclick="performSearch()">Izpiši</button>',
    '    </div>',
    '    <div class="random-verse">',
    '      <button id="refresh-verse">Naključna vrstica</button>',
    '      <div id="random-verse"><?php echo $random_verse; ?></div>',
    '    </div>',
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
    f"         Ustvarjeno: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}<br>",
    "          Licenca: CC BY-NC-ND 4.0<br>",
    "          Vir: <a href='https://github.com/msavli/SloKJV'>github.com/msavli/SloKJV</a>",
    "      </p>",
    "    </div>",
    '    <script src="./script.js"></script>',
    "  </body>",
    "</html>",
]

with open(f"{output_dir}/index.php", "w", encoding="utf-8") as f:
    f.write("\n".join(index_content))
print(f"      Wrote file: {output_dir}/index.php")

# --- Helper Functions ---
def process_note_content(note_elem):
    content = note_elem.text.strip() if note_elem.text and note_elem.text.strip() else ""
    for child in note_elem:
        if child.tag == f"{{{ns['osis']}}}hi" and child.get("type") == "bold":
            bold_text = child.text.strip() if child.text and child.text.strip() else ""
            if content and not content.endswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                content += " "
            content += f"<b>{bold_text}</b>"
            if child.tail and child.tail.strip() and not child.tail.strip().startswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                content += " "
        if child.tail and child.tail.strip():
            content += child.tail.strip()
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
                    ref_link = f"<a href='{ref_book}.html#{chap_verse_target}' class='xref-link'>{ref.text or osis_ref}</a>"
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
        if sub_elem.tag == f"{{{ns['osis']}}}transChange" and child.get("type") == "added":
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
                    ref_link = f"<a href='{ref_book}.html#{chap_verse_target}' class='xref-link'>{ref.text or osis_ref}</a>"
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
    short_title = title_elem.get("short", book_id) if title_elem is not None else book_id
    full_title = title_elem.text if title_elem is not None and title_elem.text else book_id
    # Add non-breaking space for two-word book names
    if " " in short_title:
        short_title = short_title.replace(" ", "&nbsp;")
    if " " in full_title:
        full_title = full_title.replace(" ", "&nbsp;")
    
    html_content = [
        "<!DOCTYPE html>",
        '<html lang="sl">',
        "  <head>",
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"    <title>{full_title}</title>",
        '    <link rel="stylesheet" href="./style.css">',
        '    <script>',
        '      (function() {',
        '        const savedTheme = localStorage.getItem("theme");',
        '        if (savedTheme === "night") {',
        '          document.documentElement.classList.add("night-mode");',
        '        }',
        '      })();',
        '    </script>',
        "  </head>",
        "  <body>",
        '',
        # === NOV MENI IN TEMA GUMB (tukaj vstavljeno) ===
        ' <div class="menu-container">',
        '     <button class="menu-toggle" onclick="toggleMenu(event)" aria-label="Odpri meni">',
        '         <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
        '             <line x1="3" y1="6" x2="21" y2="6"></line>',
        '             <line x1="3" y1="12" x2="21" y2="12"></line>',
        '             <line x1="3" y1="18" x2="21" y2="18"></line>',
        '         </svg>',
        '     </button>',
        '     <div id="dropdownMenu" class="dropdown-menu">',
        '         <ul>',
        '             <li><a href="index.php">Domov</a></li>',
        '             <li><a href="knjige/index.php">Spletni viri in naročila knjig</a></li>',
        '             <li><a href="knjige/Jezus.php">Jezus</a></li>',
        '             <li><a href="knjige/o_nas.php">O nas</a></li>',
        '         </ul>',
        '     </div>',
        ' </div>',
        ' <!-- TEMA GUMB (desno zgoraj) -->',
        ' <div class="theme-toggle-container">',
        '     <button type="button" id="toggle-mode" onclick="toggleMode()" aria-label="Preklopi nočni/dnevni način">',
        '         <svg id="theme-icon-sun" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
        '             <circle cx="12" cy="12" r="5"></circle>',
        '             <line x1="12" y1="1" x2="12" y2="3"></line>',
        '             <line x1="12" y1="21" x2="12" y2="23"></line>',
        '             <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>',
        '             <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>',
        '             <line x1="1" y1="12" x2="3" y2="12"></line>',
        '             <line x1="21" y1="12" x2="23" y2="12"></line>',
        '             <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>',
        '             <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>',
        '         </svg>',
        '         <svg id="theme-icon-moon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
        '             <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>',
        '         </svg>',
        '     </button>',
        ' </div>',
        '',
    ] + generate_book_nav(main_title, is_index=False) + [
        '    <div class="center-buttons">',
        '      <button id="toggle-study" onclick="toggleStudyNotes()">Odpri opombe</button>',
        '      <button id="toggle-xrefs" onclick="toggleXrefs()">Odpri reference</button>',
        '      <input type="text" id="search-input" placeholder="Vpiši iskalni niz" class="search-input">',
        '      <button id="search-button" onclick="performSearch()">Izpiši</button>',
        '    </div>',
        f"    <h2>{full_title} ({book_id})</h2>",
    ]
    
    chapters = book.findall("osis:chapter", namespaces=ns)
    chapter_nums = [chapter.get("osisID").split(".")[1] for chapter in chapters]
    chapter_nav = f"    <div class='chapter-nav'>" + " ".join(f"<a href='#{num}'>{num}</a>" for num in chapter_nums) + "</div>"
    html_content.append(chapter_nav)

    print(f"        Found {len(chapters)} chapters in {book_id}")
    for chapter in chapters:
        chapter_id = chapter.get("osisID", "Unknown Chapter")
        chapter_num = chapter_id.split(".")[1]
        if book_id.startswith("Ps"):
            chapter_title = f"Psalm {chapter_num}"
        else:
            chapter_title = f"{short_title}, {chapter_num}. poglavje"
        html_content.append(f"    <h3><span id='{chapter_num}'>{chapter_title}</span></h3>")

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
                    if sub_elem.tag == f"{{{ns['osis']}}}title" and sub_elem.get("type") == "acrostic":
                        foreign_text = sub_elem.findtext(f"{{{ns['osis']}}}foreign") or ""
                        if foreign_text.strip():
                            html_content.append(f"    <div class='acrostic-title'>{foreign_text.strip()}</div>")
                        if sub_elem.tail and sub_elem.tail.strip():
                            verse_content += " " + sub_elem.tail.strip()
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
                                ref_link = f"<a href='{ref_book}.html#{chap_verse_target}' class='xref-link'>{ref.text or osis_ref}</a>"
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

    colophons = book.findall(".//osis:div[@type='colophon']", namespaces=ns)
    for colophon in colophons:
        colophon_text = process_colophon_content(colophon)
        colophon_id = colophon.get("osisID", "")
        if colophon_text:
            if colophon_id:
                html_content.append(f"    <div class='colophon' id='{colophon_id}'>{colophon_text}</div>")
            else:
                html_content.append(f"    <div class='colophon'>{colophon_text}</div>")
        html_content.append('    <div class="top-link"><a href="#">⇧ Na vrh</a></div>')

    prev_book = book_list[i - 1][0] if i > 0 else None
    next_book = book_list[i + 1][0] if i < len(book_list) - 1 else None
    nav_links = ['    <div class="book-nav">']
    if prev_book:
        nav_links.append(f'      <a href="{prev_book}.html">Prejšnja knjiga</a>')
    nav_links.append('      <a href="index.php">Kazalo</a>')
    if next_book:
        nav_links.append(f'      <a href="{next_book}.html">Naslednja knjiga</a>')
    nav_links.append('    </div>')
    html_content.extend(nav_links)

    html_content.extend(footer_html)
    html_content.extend([
    '    <script src="./script.js"></script>',
    "  </body>",
    "</html>",
    ])

    safe_book_id = book_id.replace(".", "_")
    file_path = f"{output_dir}/{safe_book_id}.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))
    print(f"        Wrote file: {file_path}")

print(f"    HTML files generated in {output_dir}/")

print("\n" + "    " + "="*60)
print("    KONCAL KREIRANJE .html DATOTEK z osis2html.py")
print("    " + "="*60)
print("\n")