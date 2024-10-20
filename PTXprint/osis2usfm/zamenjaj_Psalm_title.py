import re

def incorporate_psalm_titles(text):
    # Define the regex pattern to find <title type="psalm" canonical="true">...</title> followed by <verse osisID="Ps.3.1">...</verse>
    pattern = r'(<title type="psalm" canonical="true">(.*?)</title>)\s*(<verse osisID="Ps\.\d+\.1">)'
    
    # Replace the pattern with the title incorporated into the verse
    def replace_function(match):
        title = match.group(2).replace('\n', ' ').strip()
        return f'{match.group(3)} #Start_Psalm_title# {title} #End_Psalm_title#'
    
    text = re.sub(pattern, replace_function, text, flags=re.DOTALL)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the function to incorporate psalm titles into verse 1
result = incorporate_psalm_titles(bible_lines)

# Write the result to the output file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)
