import re

def modify_xml(content):
    # Define the pattern to search for
    pattern = re.compile(r'(</verse></chapter>)\s*<div type="colophon"[^>]*>([^<]*)</div>', re.DOTALL)
    
    # Replace the pattern with the desired format
    modified_content = pattern.sub(r'\\cls \2\n\1', content)
    
    return modified_content

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()

# Apply the modification function
result = modify_xml(content)

# Write output to file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(result)
