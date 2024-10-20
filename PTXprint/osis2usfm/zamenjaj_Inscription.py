import re

def replace_inscription_tags(text):
    # Define the regex pattern to find <inscription>SVETO</inscription>
    inscription_pattern = r'<inscription>(.*?)</inscription>'
    
    # Replace <inscription> tags
    text = re.sub(inscription_pattern, r'\\w \1\\w*', text)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the replacement function
result = replace_inscription_tags(bible_lines)

# Write output to file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Replacements done. Check the output in {output_file}.")
