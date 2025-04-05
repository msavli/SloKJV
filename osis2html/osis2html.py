from lxml import etree
import os
from datetime import datetime

# --- XML Parsing and Setup ---
# Load the XML file containing the SloKJV data
xml_path = "../SloKJV_sword.xml"
try:
    tree = etree.parse(xml_path)
    root = tree.getroot()
    print(f"Successfully loaded XML from: {xml_path}")
    print(f"Root element: {root.tag}")
    print("First few children of root:")
    for i, child in enumerate(root):
        if i < 5:  # Omejimo na prvih 5 elementov
            print(f"  - {child.tag} (attributes: {child.attrib})")
except Exception as e:
    print(f"Error loading XML from {xml_path}: {e}")
    raise

# Define the OSIS namespace used in the XML
ns = {"osis": "http://www.bibletechnologies.net/2003/OSIS/namespace"}

# Create the output directory for HTML files if it doesn't exist
output_dir = "c:/temp/sword/html"
os.makedirs(output_dir, exist_ok=True)

# --- CSS Generation ---
# Define and write CSS styles to a separate file for consistent styling across HTML pages
css_content = """
body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
h1 { color: navy; text-align: center; }
h1 a { color: navy; text-decoration: none; }
h1 a:hover { text-decoration: underline; }
h2 { font-size: 1.4em; margin-top: 30px; color: #333; }
h3 { font-size: 1.2em; font-style: italic; margin: 10px 0; color: #555; }
h4 { font-size: 1.1em; font-weight: bold; margin: 15px 0; color: #444; }
p { margin: 15px 0; text-align: justify; }
sup { font-size: 0.8em; color: #555; vertical-align: super; }
.note { font-size: 0.9em; color: #666; }
.xref { font-size: 0.9em; color: #0066cc; }
.quote-jesus { color: #D43128; } /* Darker red for Jesus' words */
.quote-other { font-style: italic; }
i { font-style: italic; }
b { font-weight: bold; }
del { text-decoration: line-through; color: #888; }
.small-caps { font-variant: small-caps; }
.foreign { font-weight: bold; color: purple; }
.amplified { font-style: italic; color: #ff4500; }
.colophon { color: gray; margin: 15px 0; text-align: left; }
.study-container, .xref-container { position: relative; display: inline; }
.study-ref { font-size: 0.8em; color: green; vertical-align: super; cursor: pointer; }
.xref-ref { font-size: 0.8em; color: #666; vertical-align: sub; cursor: pointer; }
.xref-link { color: #0066cc; text-decoration: none; }
.xref-link:hover { text-decoration: underline; }
.book-nav { text-align: center; margin: 10px 0; }
.book-nav a { margin: 0 10px; color: #0066cc; text-decoration: none; }
.book-nav a:hover { text-decoration: underline; }
.chapter-nav { text-align: center; margin: 10px 0; }
.chapter-nav a { margin: 0 5px; color: #0066cc; text-decoration: none; }
.chapter-nav a:hover { text-decoration: underline; }
.top-link { text-align: right; margin: 10px 0; }
.top-link a { color: #0066cc; text-decoration: none; font-size: 0.9em; }
.top-link a:hover { text-decoration: underline; }
.footer { text-align: center; font-size: 0.9em; color: #666; margin-top: 20px; }
.footer a { color: #0066cc; text-decoration: none; }
.footer a:hover { text-decoration: underline; }
.study-note { font-size: 0.9em; color: green; }
.xref-note { font-size: 0.9em; color: #666; }
.study-note.hidden, .xref-note.hidden { display: none; }
.poetry { margin: 15px 0; }
.poetry-line { margin-left: 20px; }
.study-container:hover .study-note.hidden, .xref-container:hover .xref-note.hidden {
    display: inline-block; position: absolute; background-color: #f9f9f9;
    border: 1px solid #ccc; padding: 5px; z-index: 10; white-space: nowrap;
    top: -2em; left: 1em;
}
button { margin: 10px 5px; padding: 8px 15px; background-color: #0066cc; color: white; border: none; border-radius: 5px; cursor: pointer; }
button:hover { background-color: #005bb5; }
@media print {
    button, .top-link, .footer { display: none; }
    .study-note.hidden, .xref-note.hidden { display: inline-block; }
}
.acrostic-title { font-weight: bold; color: purple; text-align: center; margin: 10px 0; }
"""
with open(f"{output_dir}/style.css", "w", encoding="utf-8") as f:
    f.write(css_content)

# --- JavaScript Generation ---
# Define and write JavaScript for toggling study notes and cross-references
js_content = """
function toggleStudyNotes() {
    const notes = document.querySelectorAll('.study-note');
    const button = document.getElementById('toggle-study');
    notes.forEach(note => note.classList.toggle('hidden'));
    button.textContent = button.textContent === 'Prikaži opombe' ? 'Skrij opombe' : 'Prikaži opombe';
}
function toggleXrefs() {
    const xrefs = document.querySelectorAll('.xref-note');
    const button = document.getElementById('toggle-xrefs');
    xrefs.forEach(xref => xref.classList.toggle('hidden'));
    button.textContent = button.textContent === 'Prikaži reference' ? 'Skrij reference' : 'Prikaži reference';
}
window.onload = function() {
    document.querySelectorAll('.study-note, .xref-note').forEach(note => note.classList.add('hidden'));
};
"""
with open(f"{output_dir}/script.js", "w", encoding="utf-8") as f:
    f.write(js_content)

# --- Book List Extraction ---
# Extract all books and their short titles from the XML
books = root.findall(".//osis:div[@type='book']", namespaces=ns)
book_list = []
for book in books:
    book_id = book.get("osisID")
    title_elem = book.find("osis:title[@type='main']", namespaces=ns)
    short_title = title_elem.get("short", book_id) if title_elem is not None else book_id
    book_list.append((book_id, short_title))

# Split books into Old and New Testament (first 39 are OT, rest are NT)
old_testament = book_list[:39]  # Gen to Mal
new_testament = book_list[39:]  # Mt to Rev

# --- Navigation Generation ---
# Function to generate book navigation HTML for Old and New Testament
def generate_book_nav(main_title):
    nav_html = [
        f'    <h1><a href="index.html">{main_title}</a></h1>',
        '    <div class="book-nav">',
        '      <h3>Stara zaveza</h3>',
        '      <p>' + " ".join(f'<a href="{book_id}.html">{short_title}</a>' for book_id, short_title in old_testament) + '</p>',
        '      <h3>Nova zaveza</h3>',
        '      <p>' + " ".join(f'<a href="{book_id}.html">{short_title}</a>' for book_id, short_title in new_testament) + '</p>',
        '    </div>'
    ]
    return nav_html

# --- Footer Preparation ---
# Get current date and time for the footer
current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

# Extract metadata from XML header for the footer
main_title = root.findtext("osis:osisText/osis:header/osis:work/osis:title", default="Sveto pismo Kralja Jakoba (1769) – SloKJV", namespaces=ns)
rights = root.findtext("osis:osisText/osis:header/osis:work/osis:rights[@type='x-copyright']", default="Licenca: CC BY-NC-ND 4.0", namespaces=ns)
source = root.findtext("osis:osisText/osis:header/osis:work/osis:source", default="TextSource=github.com/msavli/SloKJV", namespaces=ns)
source_link = source.replace("TextSource=", "Vir: <a href='https://") + "'>github.com/msavli/SloKJV</a>"

# Generate footer HTML with creation date, license, and source link
footer_html = [
    f'    <div class="footer">',
    f'      <p>Ustvarjeno: {current_datetime}</p>',
    f'      <p>{rights}</p>',
    f'      <p>{source_link}</p>',
    '    </div>'
]

# --- Index Page Generation ---
# Generate index.html with a list of descriptions from the XML header
header = root.find("osis:osisText/osis:header", namespaces=ns)  # Popravljen XPath
if header is None:
    print("No <header> found in XML!")
else:
    print("Found <header> in XML.")
    work = header.find("osis:work", namespaces=ns)
    if work is None:
        print("No <work> found in <header>!")
    else:
        print("Found <work> in <header>.")

descriptions = root.findall("osis:osisText/osis:header/osis:work/osis:description", namespaces=ns)  # Popravljen XPath

# Debug: Print descriptions to verify they are being retrieved correctly
print("Descriptions found in XML:")
if descriptions:
    for desc in descriptions:
        text = desc.text if desc.text else "(empty)"
        print(f"  - {text}")
else:
    print("  - No descriptions found! Check XML file path or structure.")

# Build index content, ensuring descriptions are included in the unordered list
index_content = [
    "<!DOCTYPE html>",
    '<html lang="sl">',
    "  <head>",
    '    <meta charset="UTF-8">',
    f"    <title>{main_title}</title>",
    '    <link rel="stylesheet" href="style.css">',
    "  </head>",
    "  <body>",
    f"    <h1>{main_title}</h1>",
    "    <div>",
    "      <ul>",
]

# Add descriptions or a fallback message if none are found
if descriptions:
    index_content.extend([f"        <li>{desc.text}</li>" for desc in descriptions if desc.text and desc.text.strip()])
else:
    index_content.append("        <li>No descriptions available in XML.</li>")

index_content.extend([
    "      </ul>",
    "    </div>",
] + generate_book_nav(main_title)[1:] + footer_html + [
    "  </body>",
    "</html>",
])

# Write the index.html file
with open(f"{output_dir}/index.html", "w", encoding="utf-8") as f:
    f.write("\n".join(index_content))
print(f"Wrote file: {output_dir}/index.html")

# --- Helper Functions ---
# Process content inside <note> elements, handling bold text with proper spacing
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
    return content.strip()

# Process content inside <div type='colophon'>, handling added text with proper spacing
def process_colophon_content(colophon_elem):
    content = colophon_elem.text.strip() if colophon_elem.text and colophon_elem.text.strip() else ""
    for child in colophon_elem:
        if child.tag == f"{{{ns['osis']}}}transChange" and child.get("type") == "added":
            added_text = child.text.strip() if child.text and child.text.strip() else ""
            if content and not content.endswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                content += " "
            content += f"<i>{added_text}</i>"
            if child.tail and child.tail.strip() and not child.tail.strip().startswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                content += " "
        if child.tail and child.tail.strip():
            content += child.tail.strip()
    return content.strip()

# Process <q> elements (quotes), handling nested quotes and notes with proper spacing
def process_quote_element(sub_elem, who, chapter_id):
    quote_content = ""
    if sub_elem.text and sub_elem.text.strip():
        quote_content += sub_elem.text.strip()
    for child in sub_elem:
        if child.tag == f"{{{ns['osis']}}}quote":
            quote_content += " " + (child.text or "").strip()
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
        if child.tail and child.tail.strip():
            quote_content += " " + child.tail.strip()
    # Add spaces around the quote for proper separation
    if who == "Jesus":
        return f" <span class='quote-jesus'>{quote_content.strip()}</span> "
    else:
        return f" <span class='quote-other'>{quote_content.strip()}</span> "

# --- Main Processing Loop ---
# Process each book found in the XML
print(f"Found {len(books)} books")

for i, book in enumerate(books):
    if not isinstance(book, etree._Element):
        print(f"Warning: Expected an XML element for book, got {type(book)} instead, skipping...")
        continue
    
    book_id = book.get("osisID")
    if not book_id:
        print("No osisID found for a book, skipping...")
        continue
    
    print(f"Processing book: {book_id}")
    
    # Extract book title information
    title_elem = book.find("osis:title[@type='main']", namespaces=ns)
    short_title = title_elem.get("short", book_id) if title_elem is not None else book_id
    full_title = title_elem.text if title_elem is not None and title_elem.text else book_id
    
    # Initialize HTML content for the book
    html_content = [
        "<!DOCTYPE html>",
        '<html lang="sl">',
        "  <head>",
        '    <meta charset="UTF-8">',
        f"    <title>{full_title}</title>",
        '    <link rel="stylesheet" href="style.css">',
        "  </head>",
        "  <body>",
    ] + generate_book_nav(main_title) + [
        '    <div style="text-align: center;">',
        '      <button id="toggle-study" onclick="toggleStudyNotes()">Prikaži opombe</button>',
        '      <button id="toggle-xrefs" onclick="toggleXrefs()">Prikaži reference</button>',
        "    </div>",
        f"    <h1>{full_title} ({book_id})</h1>",
    ]

    # Generate chapter navigation links
    chapters = book.findall("osis:chapter", namespaces=ns)
    chapter_nums = [chapter.get("osisID").split(".")[1] for chapter in chapters]
    chapter_nav = f"    <div class='chapter-nav'>" + " ".join(f"<a href='#{num}'>{num}</a>" for num in chapter_nums) + "</div>"
    html_content.append(chapter_nav)

    print(f"Found {len(chapters)} chapters in {book_id}")

    # Process each chapter in the book
    for chapter in chapters:
        chapter_id = chapter.get("osisID", "Unknown Chapter")
        chapter_num = chapter_id.split(".")[1]
        if book_id.startswith("Ps"):
            chapter_title = f"Psalm {chapter_num}"
        else:
            chapter_title = f"{short_title}, {chapter_num}. poglavje"
        html_content.append(f"    <h2><span id='{chapter_num}'>{chapter_title}</span></h2>")

        # Handle psalm-specific titles if present
        psalm_title_elem = chapter.find("osis:title[@type='psalm']", namespaces=ns)
        if psalm_title_elem is not None:
            psalm_title = psalm_title_elem.text or ""
            title_content = psalm_title
            xref_counter = 0
            for sub_elem in psalm_title_elem:
                if sub_elem.tag == f"{{{ns['osis']}}}note" and sub_elem.get("type") == "crossReference":
                    xref_counter += 1
                    refs = sub_elem.findall("osis:reference", namespaces=ns)
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
                    title_content += f" <span class='xref-container'><span class='xref-ref'>{xref_counter}</span><span class='xref-note hidden' id='xref-{chapter_id}-{xref_counter}'>[{xref_text}]</span></span>"
                if sub_elem.tail:
                    title_content += sub_elem.tail
            html_content.append(f"    <h3>{title_content.strip()}</h3>")

        # Initialize variables for processing verses
        paragraph = ""
        study_counter = 0
        xref_counter = 0
        poetry_lines = []

        # Process each verse in the chapter
        for elem in chapter:
            if elem.tag == f"{{{ns['osis']}}}verse":
                verse_id = elem.get("osisID", "Unknown Verse")
                verse_num = verse_id.split(".")[-1]
                chap_verse_id = ".".join(verse_id.split(".")[1:])
                verse_content = ""
                if elem.text and elem.text.strip():
                    verse_content += elem.text.strip()
                
                # Handle acrostic titles if present
                for sub_elem in elem:
                    if sub_elem.tag == f"{{{ns['osis']}}}title" and sub_elem.get("type") == "acrostic":
                        foreign_text = sub_elem.findtext(f"{{{ns['osis']}}}foreign") or ""
                        if foreign_text.strip():
                            html_content.append(f"    <div class='acrostic-title'>{foreign_text.strip()}</div>")
                        if sub_elem.tail and sub_elem.tail.strip():
                            verse_content += " " + sub_elem.tail.strip()
                        break

                # Process all sub-elements within the verse
                for sub_elem in elem:
                    if sub_elem.tag == f"{{{ns['osis']}}}milestone" and sub_elem.get("type") == "x-p":
                        if poetry_lines:
                            html_content.append("    <div class='poetry'>")
                            html_content.extend(poetry_lines)
                            html_content.append("    </div>")
                            poetry_lines = []
                        if paragraph.strip():
                            html_content.append(f"    <p>{paragraph.strip()}</p>")
                            paragraph = ""
                    elif sub_elem.tag == f"{{{ns['osis']}}}title" and sub_elem.get("type") == "acrostic":
                        continue
                    elif sub_elem.tag == f"{{{ns['osis']}}}q":
                        who = sub_elem.get("who", "")
                        verse_content += process_quote_element(sub_elem, who, chapter_id)
                    elif sub_elem.tag == f"{{{ns['osis']}}}note":
                        note_type = sub_elem.get("type")
                        if note_type == "study":
                            study_counter += 1
                            study_ref = chr(96 + study_counter)
                            note_text = process_note_content(sub_elem)
                            verse_content += f" <span class='study-container'><span class='study-ref'>{study_ref}</span><span class='study-note hidden' id='study-{chapter_id}-{study_ref}'>[{note_text}]</span></span>"
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
                                elif "." not in chap_verse:
                                    chap_verse_target = chap_verse
                                else:
                                    chap_verse_target = chap_verse
                                ref_link = f"<a href='{ref_book}.html#{chap_verse_target}' class='xref-link'>{ref.text or osis_ref}</a>"
                                ref_texts.append(ref_link)
                            xref_text = "; ".join(ref_texts)
                            verse_content += f" <span class='xref-container'><span class='xref-ref'>{xref_ref}</span><span class='xref-note hidden' id='xref-{chapter_id}-{xref_ref}'>[{xref_text}]</span></span>"
                        if sub_elem.tail and sub_elem.tail.strip():
                            verse_content += " " + sub_elem.tail.strip()
                    elif sub_elem.tag == f"{{{ns['osis']}}}transChange" and sub_elem.get("type") == "added":
                        added_text = sub_elem.text or ""
                        verse_content += f" <i>{added_text}</i>"
                        if sub_elem.tail and sub_elem.tail.strip():
                            verse_content += " " + sub_elem.tail.strip()
                    elif sub_elem.tag == f"{{{ns['osis']}}}hi" and sub_elem.get("type") == "bold":
                        bold_text = sub_elem.text.strip() if sub_elem.text and sub_elem.text.strip() else ""
                        if verse_content and not verse_content.endswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                            verse_content += " "
                        verse_content += f"<b>{bold_text}</b>"
                        if sub_elem.tail and sub_elem.tail.strip() and not sub_elem.tail.strip().startswith((" ", ",", ".", ";", ":", "!", "?", "‹", "›")):
                            verse_content += " "
                        if sub_elem.tail and sub_elem.tail.strip():
                            verse_content += sub_elem.tail.strip()
                    elif sub_elem.tag == f"{{{ns['osis']}}}divineName":
                        divine_text = sub_elem.text or ""
                        if verse_content and not verse_content.endswith(("'", "›", ":", " ")):
                            verse_content += " "
                        verse_content += f"<span class='small-caps'>{divine_text}</span>"
                        if sub_elem.tail and sub_elem.tail.strip():
                            tail_text = sub_elem.tail.strip()
                            if not tail_text.startswith((",", ".", ";", ":", "!", "?", "‹", "›")):
                                verse_content += " "
                            verse_content += tail_text
                    elif sub_elem.tag == f"{{{ns['osis']}}}foreign":
                        foreign_text = sub_elem.text or ""
                        verse_content += f" <span class='foreign'>{foreign_text}</span>"
                        if sub_elem.tail and sub_elem.tail.strip():
                            verse_content += " " + sub_elem.tail.strip()
                    elif sub_elem.tag == f"{{{ns['osis']}}}inscription":
                        inscription_text = sub_elem.text or ""
                        if verse_content and not verse_content.endswith(" "):
                            verse_content += " "
                        verse_content += f"<span class='small-caps'>{inscription_text}</span>"
                        if sub_elem.tail and sub_elem.tail.strip():
                            tail_text = sub_elem.tail.strip()
                            if not tail_text.startswith((",", ".", ";", ":", "!", "?", "‹", "›")):
                                verse_content += " "
                            verse_content += tail_text
                    elif sub_elem.tag == f"{{{ns['osis']}}}seg":
                        seg_text = sub_elem.text or ""
                        if poetry_lines:
                            html_content.append("    <div class='poetry'>")
                            html_content.extend(poetry_lines)
                            html_content.append("    </div>")
                            poetry_lines = []
                        if paragraph.strip():
                            html_content.append(f"    <p>{paragraph.strip()}</p>")
                        html_content.append(f"    <h4>{seg_text}</h4>")
                        paragraph = ""
                        if sub_elem.tail and sub_elem.tail.strip():
                            verse_content += " " + sub_elem.tail.strip()
                    elif sub_elem.tag == f"{{{ns['osis']}}}l":
                        line_text = sub_elem.text or ""
                        poetry_lines.append(f"      <div class='poetry-line'>{line_text}</div>")
                        if sub_elem.tail and sub_elem.tail.strip():
                            verse_content += " " + sub_elem.tail.strip()
                    if sub_elem.tag == f"{{{ns['osis']}}}milestone" and sub_elem.tail and sub_elem.tail.strip():
                        verse_content += " " + sub_elem.tail.strip()
                
                # Add verse content to paragraph
                if verse_content.strip():
                    paragraph += f"<span id='{chap_verse_id}'><sup>{verse_num}</sup> {verse_content.strip()}</span>"
                
                if elem.tail and elem.tail.strip():
                    paragraph += " " + elem.tail.strip()

        # Handle poetry lines if present
        if poetry_lines:
            html_content.append("    <div class='poetry'>")
            html_content.extend(poetry_lines)
            html_content.append("    </div>")
        # Add paragraph content if present
        if paragraph.strip():
            html_content.append(f"    <p>{paragraph.strip()}</p>")
        
        # Process colophons at the chapter level
        colophons = chapter.findall(".//osis:div[@type='colophon']", namespaces=ns)
        for colophon in colophons:
            colophon_text = process_colophon_content(colophon)
            colophon_id = colophon.get("osisID", "")
            if colophon_text:
                if colophon_id:
                    html_content.append(f"    <div class='colophon' id='{colophon_id}'>{colophon_text}</div>")
                else:
                    html_content.append(f"    <div class='colophon'>{colophon_text}</div>")
        
        # Add "Back to top" link after chapter content or colophon
        html_content.append('    <div class="top-link"><a href="#">⇧ Na vrh</a></div>')

    # Process colophons at the book level
    colophons = book.findall(".//osis:div[@type='colophon']", namespaces=ns)
    for colophon in colophons:
        colophon_text = process_colophon_content(colophon)
        colophon_id = colophon.get("osisID", "")
        if colophon_text:
            if colophon_id:
                html_content.append(f"    <div class='colophon' id='{colophon_id}'>{colophon_text}</div>")
            else:
                html_content.append(f"    <div class='colophon'>{colophon_text}</div>")
        
        # Add "Back to top" link after book-level colophon
        html_content.append('    <div class="top-link"><a href="#">⇧ Na vrh</a></div>')

    # Add navigation to previous/next book and index
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

    # Append footer and JavaScript
    html_content.extend(footer_html)
    html_content.append('    <script src="script.js"></script>')
    html_content.extend([
        "  </body>",
        "</html>",
    ])

    # Write the HTML file for the book
    safe_book_id = book_id.replace(".", "_")
    file_path = f"{output_dir}/{safe_book_id}.html"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))
    print(f"Wrote file: {file_path}")

# --- Completion Message ---
print(f"HTML files generated in {output_dir}/")