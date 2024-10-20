import re

def replace_divineName_tags(text):
    # Define the regex pattern to find <divineName>Gospod</divineName>
    divineName_pattern = r'<divineName>(.*?)</divineName>'
    
    # Define the regex pattern to find Jesus speaking
    jesus_speaking_pattern = r'<q who="Jesus" marker="">(.*?)</q>'
    
    # Define the regex pattern to find inscription tags
    inscription_pattern = r'<inscription>(.*?)</inscription>'
    
    # Find all instances where Jesus is speaking
    jesus_speaking_matches = re.findall(jesus_speaking_pattern, text, re.DOTALL)
    
    # Replace <divineName> tags within Jesus speaking sections
    for match in jesus_speaking_matches:
        replaced_text = re.sub(divineName_pattern, r'\\+nd \1\\+nd*', match)
        text = text.replace(match, replaced_text)
    
    # Replace <divineName> tags within inscription sections
    inscription_matches = re.findall(inscription_pattern, text, re.DOTALL)
    for match in inscription_matches:
        replaced_text = re.sub(divineName_pattern, r'\\+nd \1\\+nd*', match)
        text = text.replace(match, replaced_text)
    
    # Replace remaining <divineName> tags outside Jesus speaking and inscription sections
    text = re.sub(divineName_pattern, r'\\nd \1\\nd*', text)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the replacement function
result = replace_divineName_tags(bible_lines)

# Write output to file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Replacements done. Check the output in {output_file}.")

