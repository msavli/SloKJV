import re

def change_lb_and_introduction(text):
    # Replace <lb /> with \ip
    #  lb sem odstranil iz izvorne datoteke pri škrlatni črv, ker čudno razporedi opombo in se to ne uporablja več.
    text = re.sub(r'<lb\s*/>', r'\\ip', text)
    
    # Define the regex pattern to find <div type="introduction">...</div> followed by <chapter><verse>
    pattern = r'<div type="introduction">\s*<p type="x-noindent" subType="x-introduction">(.*?)</p>\s*</div>\s*<chapter><verse>'
    
    # Replace the pattern with the introduction incorporated into the verse
    text = re.sub(pattern, r'<chapter><verse>#Zacetek_Uvoda#\1#Konec_Uvoda#', text, flags=re.DOTALL)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the function to change <lb /> and incorporate introduction into verse
result = change_lb_and_introduction(bible_lines)

# Write the result to the output file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"<lb /> tags have been changed and introduction lines have been incorporated into verse lines. Check the output in {output_file}.")
