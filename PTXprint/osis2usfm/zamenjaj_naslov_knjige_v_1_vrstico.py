import re

def incorporate_title_into_verse(text):
    # Define the regex pattern to find <title type="main" short="Geneza">...</title> followed by <chapter><verse>
    pattern = r'<title type="main" short="[^"]+">(.*?)</title>\s*<chapter><verse>'
    
    # Replace the pattern with the title incorporated into the verse
    text = re.sub(pattern, r'<chapter><verse>#Zacetek_knjige#\1#Konec_knjige#', text, flags=re.DOTALL)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the function to incorporate title into verse
result = incorporate_title_into_verse(bible_lines)

# Write the result to the output file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Title lines have been incorporated into verse lines. Check the output in {output_file}.")
