import re

def change_acrostic_title(text):
    # Define the regex pattern to find <title type="acrostic" canonical="true"><foreign n="א">some text</foreign> </title>
    pattern = r'<title type="acrostic" canonical="true"><foreign n="[^"]+">(.*?)</foreign> </title>'
    
    # Replace the pattern with \qa [some text]
    text = re.sub(pattern, r'#Zacetek_Alef#\\qa \1#Konec_Alef#', text)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the function to change acrostic titles
result = change_acrostic_title(bible_lines)

# Write the result to the output file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Acrostic titles have been changed. Check the output in {output_file}.")
