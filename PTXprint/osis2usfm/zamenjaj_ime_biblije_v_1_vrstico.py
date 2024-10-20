import re

def process_xml(text):
    # Remove the first line
    text = re.sub(r'^<\?xml version="1.0" encoding="UTF-8" \?>\n', '', text)
    
    # Simplify the <osis> tag
    text = re.sub(r'<osis [^>]+>', r'<osis>', text)
    
    # Extract the title from the <header> and remove the <header> tag
    title_match = re.search(r'<title>(.*?)</title>', text)
    title = title_match.group(1) if title_match else ''
    text = re.sub(r'<header>.*?</header>', '', text, flags=re.DOTALL)
    
    # Incorporate the title into the first verse
    text = re.sub(r'<div type="book">\s*<chapter><verse>', 
                  r'<div type="book"><chapter><verse>#Zacetek_Ime_Biblije#' + title + r'#Konec_ime_Biblije#', 
                  text, count=1)

    # Simplify the <osisText> tag
    # Pojma nimam zakaj je bilo treba dodati tole solato za <osisText> tagom <div type="x-testament"><div type="book"><chapter><verse></verse></chapter></div></div>
    text = re.sub(r'<osisText [^>]+>', r'<osisText><div type="x-testament"><div type="book"><chapter><verse></verse></chapter></div></div>', text)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    xml_content = file.read()

# Apply the function to process the XML content
result = process_xml(xml_content)

# Write the result to the output file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"XML processing complete. Check the output in {output_file}.")
