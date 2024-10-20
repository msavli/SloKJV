import re

def change_chapter_tag(text):
    # Define the regex pattern to find <chapter osisID="Gen.1" chapterTitle="1. Poglavje">
    pattern = r'<chapter osisID="[^"]+" chapterTitle="[^"]+">'
    
    # Replace the pattern with <chapter>
    text = re.sub(pattern, r'<chapter>', text)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the function to change chapter tags
result = change_chapter_tag(bible_lines)

# Write the result to the output file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Chapter tags have been changed. Check the output in {output_file}.")
