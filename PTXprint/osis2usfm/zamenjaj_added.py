import re
import sys
import os

def replace_transChange(text):
    # Define the regex pattern to find <transChange type="added">some text</transChange>
    pattern = r'<transChange type="added">(.*?)</transChange>'
    
    # Define the regex pattern to find Jesus speaking
    jesus_speaking_pattern = r'<q who="Jesus" marker="">(.*?)</q>'
    
    # Find all instances where Jesus is speaking
    jesus_speaking_matches = re.findall(jesus_speaking_pattern, text, re.DOTALL)
    
    # Replace <transChange> tags within Jesus speaking sections
    for match in jesus_speaking_matches:
        replaced_text = re.sub(pattern, r'\\+add \1\\+add*', match)
        text = text.replace(match, replaced_text)
    
    # Replace remaining <transChange> tags outside Jesus speaking sections
    text = re.sub(pattern, r'\\add \1\\add*', text)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the replacement function
result = replace_transChange(bible_lines)

# Write output to file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"            Replacements done. Check the output in {output_file}.")
