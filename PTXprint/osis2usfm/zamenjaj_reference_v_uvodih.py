import re

def replace_reference_tags(text):
    # Define the regex pattern to find <reference osisRef="...">...</reference>
    reference_pattern = r'<reference osisRef="[^"]+">(.*?)</reference>'
    
    # Replace <reference> tags
    text = re.sub(reference_pattern, r'\\xo 1,0: \\xt \1\\x*', text)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the replacement function
result = replace_reference_tags(bible_lines)

# Write output to file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Replacements done. Check the output in {output_file}.")
