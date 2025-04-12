from lxml import etree
import os
from datetime import datetime

# --- XML Parsing and Setup ---
xml_path = "../SloKJV_sword.xml"
try:
    tree = etree.parse(xml_path)
    root = tree.getroot()
    print(f"Successfully loaded XML from: {xml_path}")
    print(f"Root element: {root.tag}")
    print("First few children of root:")
    for i, child in enumerate(root):
        if i < 5:
            print(f"  - {child.tag} (attributes: {child.attrib})")
except Exception as e:
    print(f"Error loading XML from {xml_path}: {e}")
    raise

ns = {"osis": "http://www.bibletechnologies.net/2003/OSIS/namespace"}
output_dir = "c:/temp/sword/html"
os.makedirs(output_dir, exist_ok=True)

# --- CSS Generation ---
css_content = """
html {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 20px;
    background-color: #ffffff;
    color: #000000;
    transition: background-color 0.3s, color 0.3s;
}
html.night-mode {
    background-color: #1a1a1a;
    color: #e0e0e0;
}
h1 { color: navy; text-align: center; transition: color 0.3s; }
h1 a { color: navy; text-decoration: none; transition: color 0.3s; }
h1 a:hover { text-decoration: underline; }
html.night-mode h1, html.night-mode h1 a { color: #87ceeb; }
h2 { font-size: 1.4em; margin-top: 30px; color: #333; font-style: normal; transition: color 0.3s; }
html.night-mode h2 { color: #d3d3d3; }
h3 { font-size: 1.2em; font-style: normal; margin: 10px 0; color: #555; transition: color 0.3s; }
html.night-mode h3 { color: #c0c0c0; }
h4 { font-size: 1.1em; font-weight: bold; margin: 15px 0; color: #444; transition: color 0.3s; }
html.night-mode h4 { color: #b0b0b0; }
p { margin: 15px 0; text-align: justify; }
sup { font-size: 0.8em; color: #555; vertical-align: super; transition: color 0.3s; }
html.night-mode sup { color: #a0a0a0; }
.note { font-size: 0.9em; color: #666; transition: color 0.3s; }
html.night-mode .note { color: #999; }
.xref { font-size: 0.9em; color: #0066cc; transition: color 0.3s; }
html.night-mode .xref { color: #66b3ff; }
.quote-jesus { color: #D43128; }
html.night-mode .quote-jesus { color: #ff6666; }
.quote-other { font-style: italic; }
i { font-style: italic; }
b { font-weight: bold; }
del { text-decoration: line-through; color: #888; transition: color 0.3s; }
html.night-mode del { color: #666; }
.small-caps { font-variant: small-caps; }
.foreign { font-weight: bold; color: purple; transition: color 0.3s; }
html.night-mode .foreign { color: #dda0dd; }
.amplified { font-style: italic; color: #ff4500; transition: color 0.3s; }
html.night-mode .amplified { color: #ff7f50; }
.colophon { color: gray; margin: 15px 0; text-align: left; transition: color 0.3s; }
html.night-mode .colophon { color: #888; }
.study-container, .xref-container { position: relative; display: inline; }
.study-ref { font-size: 0.8em; color: green; vertical-align: super; cursor: pointer; transition: color 0.3s; }
html.night-mode .study-ref { color: #90ee90; }
.xref-ref { font-size: 0.9em; color: #0066cc; vertical-align: sub; cursor: pointer; transition: color 0.3s; }
html.night-mode .xref-ref { color: #66b3ff; }
.xref-link { color: #0066cc; text-decoration: none; transition: color 0.3s; }
html.night-mode .xref-link { color: #66b3ff; }
.xref-link:hover { text-decoration: underline; }
.book-nav { text-align: center; margin: 10px 0; }
.book-nav a { margin: 0 10px; color: #0066cc; text-decoration: none; transition: color 0.3s; }
html.night-mode .book-nav a { color: #66b3ff; }
.book-nav a:hover { text-decoration: underline; }
.chapter-nav { text-align: center; margin: 10px 0; }
.chapter-nav a { margin: 0 5px; color: #0066cc; text-decoration: none; transition: color 0.3s; }
html.night-mode .chapter-nav a { color: #66b3ff; }
.chapter-nav a:hover { text-decoration: underline; }
.top-link { text-align: right; margin: 10px 0; }
.top-link a { color: #0066cc; text-decoration: none; font-size: 0.9em; transition: color 0.3s; }
html.night-mode .top-link a { color: #66b3ff; }
.top-link a:hover { text-decoration: underline; }
.footer { text-align: center; font-size: 0.9em; color: #666; margin-top: 20px; transition: color 0.3s; }
html.night-mode .footer { color: #999; }
.footer a { color: #0066cc; text-decoration: none; transition: color 0.3s; }
html.night-mode .footer a { color: #66b3ff; }
.footer a:hover { text-decoration: underline; }
.study-note { font-size: 0.9em; color: green; transition: color 0.3s; }
html.night-mode .study-note { color: #90ee90; }
.xref-note { font-size: 0.9em; color: #0066cc; transition: color 0.3s; }
html.night-mode .xref-note { color: #66b3ff; }
.study-note.hidden, .xref-note.hidden { display: none; }
.poetry { margin: 15px 0; }
.poetry-line { margin-left: 20px; }
.study-container:hover .study-note.hidden, .xref-container:hover .xref-note.hidden {
    display: inline-block; position: absolute; background-color: #f9f9f9; border: 1px solid #ccc; padding: 5px; z-index: 10; white-space: nowrap; top: -2em; left: 1em; transition: background-color 0.3s, border-color 0.3s;
}
html.night-mode .study-container:hover .study-note.hidden, html.night-mode .xref-container:hover .xref-note.hidden {
    background-color: #333; border-color: #555;
}
button { margin: 10px 5px; padding: 8px 15px; background-color: #0066cc; color: white; border: none; border-radius: 5px; cursor: pointer; transition: background-color 0.3s; }
button:hover { background-color: #005bb5; }
html.night-mode button { background-color: #4682b4; }
html.night-mode button:hover { background-color: #5a9bd4; }
@media print {
    button, .top-link, .footer { display: none; }
    .study-note.hidden, .xref-note.hidden { display: inline-block; }
}
.acrostic-title { font-weight: bold; color: purple; text-align: center; margin: 10px 0; transition: color 0.3s; }
html.night-mode .acrostic-title { color: #dda0dd; }
/* Stili za zemljevide */
.maps-section { text-align: center; margin-top: 30px; }
.maps-section h2 { color: #333; transition: color 0.3s; }
html.night-mode .maps-section h2 { color: #d3d3d3; }
.map-preview { max-width: 250px; height: auto; margin: 15px; border: 1px solid #ccc; transition: border-color 0.3s; cursor: pointer; }
html.night-mode .map-preview { border-color: #555; }
.map-preview:hover { border-color: #0066cc; }
"""
with open(f"{output_dir}/style.css", "w", encoding="utf-8") as f:
    f.write(css_content)

# --- JavaScript Generation ---
js_content = """
function toggleStudyNotes() {
    const notes = document.querySelectorAll('.study-note');
    const button = document.getElementById('toggle-study');
    console.log('Toggling study notes');
    notes.forEach(note => note.classList.toggle('hidden'));
    const isVisible = !notes[0].classList.contains('hidden');
    button.textContent = isVisible ? 'Skrij opombe' : 'Prikaži opombe';
    localStorage.setItem('studyNotesVisible', isVisible ? 'true' : 'false');
}

function toggleXrefs() {
    const xrefs = document.querySelectorAll('.xref-note');
    const button = document.getElementById('toggle-xrefs');
    console.log('Toggling xrefs');
    xrefs.forEach(xref => xref.classList.toggle('hidden'));
    const isVisible = !xrefs[0].classList.contains('hidden');
    button.textContent = isVisible ? 'Skrij reference' : 'Prikaži reference';
    localStorage.setItem('xrefsVisible', isVisible ? 'true' : 'false');
}

function toggleMode() {
    const body = document.body;
    const button = document.getElementById('toggle-mode');
    body.classList.toggle('night-mode');
    const isNightMode = body.classList.contains('night-mode');
    button.textContent = isNightMode ? 'Dnevni način' : 'Nočni način';
    localStorage.setItem('theme', isNightMode ? 'night' : 'day');
}

window.onload = function() {
    console.log('Window loaded, initializing');
    const studyNotes = document.querySelectorAll('.study-note');
    const xrefNotes = document.querySelectorAll('.xref-note');
    const toggleStudyButton = document.getElementById('toggle-study');
    const toggleXrefsButton = document.getElementById('toggle-xrefs');
    const toggleModeButton = document.getElementById('toggle-mode');

    // Initialize study notes
    const studyNotesVisible = localStorage.getItem('studyNotesVisible');
    if (studyNotesVisible === 'true') {
        studyNotes.forEach(note => note.classList.remove('hidden'));
        toggleStudyButton.textContent = 'Skrij opombe';
    } else {
        studyNotes.forEach(note => note.classList.add('hidden'));
        toggleStudyButton.textContent = 'Prikaži opombe';
    }

    // Initialize cross-references
    const xrefsVisible = localStorage.getItem('xrefsVisible');
    if (xrefsVisible === 'true') {
        xrefNotes.forEach(xref => xref.classList.remove('hidden'));
        toggleXrefsButton.textContent = 'Skrij reference';
    } else {
        xrefNotes.forEach(xref => xref.classList.add('hidden'));
        toggleXrefsButton.textContent = 'Prikaži reference';
    }

    // Initialize theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'night') {
        document.body.classList.add('night-mode');
        toggleModeButton.textContent = 'Dnevni način';
    } else {
        document.body.classList.remove('night-mode');
        toggleModeButton.textContent = 'Nočni način';
    }
};
"""
with open(f"{output_dir}/script.js", "w", encoding="utf-8") as f:
    f.write(js_content)

# --- Book List Extraction ---
books = root.findall(".//osis:div[@type='book']", namespaces=ns)
book_list = []
for book in books:
    book_id = book.get("osisID")
    title_elem = book.find("osis:title[@type='main']", namespaces=ns)
    short_title = title_elem.get("short", book_id) if title_elem is not None else book_id
    book_list.append((book_id, short_title))

old_testament = book_list[:39]
new_testament = book_list[39:]

# --- Navigation Generation ---
def generate_book_nav(main_title, is_index=False):
    if is_index:
        title_line = f'    <h1>{main_title}</h1>'
    else:
        title_line = f'    <h1><a href="index.html">{main_title}</a></h1>'
    nav_html = [
        title_line,
        '    <div class="book-nav">',
        '      <h3>Stara zaveza</h3>',
        '      <p>' + " ".join(f'<a href="{book_id}.html">{short_title}</a>' for book_id, short_title in old_testament) + '</p>',
        '      <h3>Nova zaveza</h3>',
        '      <p>' + " ".join(f'<a href="{book_id}.html">{short_title}</a>' for book_id, short_title in new_testament) + '</p>',
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
    f'      <p>Ustvarjeno: {current_datetime}</p>',
    f'      <p>{rights}</p>',
    f'      <p>{source_link}</p>',
    '    </div>'
]

# --- Index Page Generation ---
header = root.find("osis:osisText/osis:header", namespaces=ns)
if header is None:
    print("No <header> found in XML!")
else:
    print("Found <header> in XML.")
    work = header.find("osis:work", namespaces=ns)
    if work is None:
        print("No <work> found in <header>!")
    else:
        print("Found <work> in <header>.")

descriptions = root.findall("osis:osisText/osis:header/osis:work/osis:description", namespaces=ns)
print("Descriptions found in XML:")
if descriptions:
    for desc in descriptions:
        text = desc.text if desc.text else "(empty)"
        print(f"  - {text}")
else:
    print("  - No descriptions found! Check XML file path or structure.")

index_content = [
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
] + generate_book_nav(main_title, is_index=True) + [
    "    <div>",
    "      <ul>",
]
if descriptions:
    index_content.extend([f"        <li>{desc.text}</li>" for desc in descriptions if desc.text and desc.text.strip()])
else:
    index_content.append("        <li>No descriptions available in XML.</li>")
index_content.extend([
    "      </ul>",
    "    </div>",
    "    <div class='maps-section'>",
    "      <h2>Zemljevidi</h2>",
    "      <p>Kliknite na sliko za ogled v polni velikosti:</p>",
    "      <a href='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Ancient_World_Patriarchs_Slo.jpg' target='_blank'>",
    "        <img src='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Ancient_World_Patriarchs_Slo_thumb.jpg' alt='Stari svet patriarhov' class='map-preview'>",
    "      </a>",
    "      <a href='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Exodus_and_Canaan_Conquest_Slo.jpg' target'slo_thumb.jpg' alt='_blank'>",
    "        <img src='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Exodus_and_Canaan_Conquest_Slo_thumb.jpg' alt='Eksodus in osvajanje Kanaana' class='map-preview'>",
    "      </a>",
    "      <a href='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Paul_Journeys_Slo.jpg' target='_blank'>",
    "        <img src='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Paul_Journeys_Slo_thumb.jpg' alt='Pavlova potovanja' class='map-preview'>",
    "      </a>",
    "      <a href='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Israel_New_Testament_Slo.jpg' target='_blank'>",
    "        <img src='https://raw.githubusercontent.com/msavli/Bible-Maps/main/Map_Israel_New_Testament_Slo_thumb.jpg' alt='Izrael v času Nove zaveze' class='map-preview'>",
    "      </a>",
    "    </div>",
    '    <div style="text-align: center;">',
    '      <button id="toggle-mode" onclick="toggleMode()">Nočni način</button>',
    "    </div>",
] + footer_html + [
    '    <script src="./script.js"></script>',
    "  </body>",
    "</html>",
])

index_content.extend([
    "    <div style='text-align: center;'>",
    "      <button id='toggle-mode' onclick='toggleMode()'>Nočni način</button>",
    "      <br><br>",
    "      <a href='search.php'>Iskanje po Svetem pismu</a>",
    "    </div>",
])

with open(f"{output_dir}/index.html", "w", encoding="utf-8") as f:
    f.write("\n".join(index_content))
print(f"Wrote file: {output_dir}/index.html")

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
        if sub_elem.tag == f"{{{ns['osis']}}}transChange" and sub_elem.get("type") == "added":
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
    
    print(f"Processing book: {book_id}")
    
    title_elem = book.find("osis:title[@type='main']", namespaces=ns)
    short_title = title_elem.get("short", book_id) if title_elem is not None else book_id
    full_title = title_elem.text if title_elem is not None and title_elem.text else book_id
    
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
    ] + generate_book_nav(main_title, is_index=False) + [
        '    <div style="text-align: center;">',
        '      <button id="toggle-study" onclick="toggleStudyNotes()">Prikaži opombe</button>',
        '      <button id="toggle-xrefs" onclick="toggleXrefs()">Prikaži reference</button>',
        '      <button id="toggle-mode" onclick="toggleMode()">Nočni način</button>',
        "    </div>",
        f"    <h1>{full_title} ({book_id})</h1>",
    ]
    
    chapters = book.findall("osis:chapter", namespaces=ns)
    chapter_nums = [chapter.get("osisID").split(".")[1] for chapter in chapters]
    chapter_nav = f"    <div class='chapter-nav'>" + " ".join(f"<a href='#{num}'>{num}</a>" for num in chapter_nums) + "</div>"
    html_content.append(chapter_nav)

    print(f"Found {len(chapters)} chapters in {book_id}")
    for chapter in chapters:
        chapter_id = chapter.get("osisID", "Unknown Chapter")
        chapter_num = chapter_id.split(".")[1]
        if book_id.startswith("Ps"):
            chapter_title = f"Psalm {chapter_num}"
        else:
            chapter_title = f"{short_title}, {chapter_num}. poglavje"
        html_content.append(f"    <h2><span id='{chapter_num}'>{chapter_title}</span></h2>")

        psalm_title_elem = chapter.find("osis:title[@type='psalm']", namespaces=ns)
        if psalm_title_elem is not None:
            title_content = process_title_content(psalm_title_elem, chapter_id)
            html_content.append(f"    <h3>{title_content}</h3>")

        paragraph = ""
        study_counter = 0
        xref_counter = 0
        poetry_lines = []

        first_verse_in_paragraph = True
        for elem in chapter:
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

                if verse_content.strip():
                    if first_verse_in_paragraph:
                        paragraph += f"<span id='{chap_verse_id}'><sup>{verse_num}</sup> {verse_content.strip()}</span>"
                        first_verse_in_paragraph = False
                    else:
                        paragraph += f" <span id='{chap_verse_id}'><sup>{verse_num}</sup> {verse_content.strip()}</span>"

                if elem.tail and elem.tail.strip():
                    paragraph += " " + elem.tail.strip()

        if poetry_lines:
            html_content.append("    <div class='poetry'>")
            html_content.extend(poetry_lines)
            html_content.append("    </div>")
        if paragraph.strip():
            html_content.append(f"    <p>{paragraph.strip()}</p>")
        
        colophons = chapter.findall(".//osis:div[@type='colophon']", namespaces=ns)
        for colophon in colophons:
            colophon_text = process_colophon_content(colophon)
            colophon_id = colophon.get("osisID", "")
            if colophon_text:
                if colophon_id:
                    html_content.append(f"    <div class='colophon' id='{colophon_id}'>{colophon_text}</div>")
                else:
                    html_content.append(f"    <div class='colophon'>{colophon_text}</div>")
        
        html_content.append('    <div class="top-link"><a href="#">⇧ Na vrh</a></div>')

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
    nav_links.append('      <a href="index.html">Kazalo</a>')
    if next_book:
        nav_links.append(f'      <a href="{next_book}.html">Naslednja knjiga</a>')
    nav_links.append('    </div>')
    html_content.extend(nav_links)

    html_content.extend(footer_html)
    html_content.append('    <script src="./script.js"></script>')
    html_content.extend([
        "  </body>",
        "</html>",
    ])

    safe_book_id = book_id.replace(".", "_")
    file_path = f"{output_dir}/{safe_book_id}.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))
    print(f"Wrote file: {file_path}")

print(f"HTML files generated in {output_dir}/")