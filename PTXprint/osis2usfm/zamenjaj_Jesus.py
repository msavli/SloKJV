import re

def replace_jesus_speaking_tags(text):
    # Replace <q who="Jesus" marker=""> with \wj
    text = re.sub(r'<q who="Jesus" marker="">', r'\\wj ', text)
    
    # Replace </q> with \wj*
    text = re.sub(r'</q>', r'\\wj*', text)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the replacement function
result = replace_jesus_speaking_tags(bible_lines)

# Write output to file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Replacements done. Check the output in {output_file}.")
