import re

def remove_introduction_divs(text):
    # Define the regex pattern to match <div type="introduction"> and its content
    introduction_pattern = r'<div type="introduction">.*?</div>'
    
    # Remove <div type="introduction"> and its content
    text = re.sub(introduction_pattern, '', text, flags=re.DOTALL)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r', encoding='utf-8') as file:
    bible_lines = file.read()

# Apply the removal function
result = remove_introduction_divs(bible_lines)

# Write output to file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(result)
