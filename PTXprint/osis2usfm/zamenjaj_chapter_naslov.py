import re

def change_title_to_verse(text):
    # Define the regex pattern to find <title type="chapter">1. Poglavje</title> followed by <verse> on a new line
    pattern = r'<title type="chapter">(.*?)</title>\s*<verse>'
    
    # Replace the pattern with <verse>#Start_naslov#1. Poglavje#Konec_naslov#
    text = re.sub(pattern, r'<verse>#Start_naslov#\1#Konec_naslov#', text, flags=re.DOTALL)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the function to change title to verse
result = change_title_to_verse(bible_lines)

# Write the result to the output file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Title tags have been changed. Check the output in {output_file}.")
