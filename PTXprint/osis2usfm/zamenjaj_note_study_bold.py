import re

def change_bold_hi(text):
    # Define the regex pattern to find <hi type="bold">some_text</hi>
    pattern = r'<hi type="bold">(.*?)</hi>'
    
    # Replace the pattern with \+bd some_text\+bd*
    text = re.sub(pattern, r'\\+bd \1\\+bd*', text)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the function to change bold hi tags
result = change_bold_hi(bible_lines)

# Write the result to the output file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Bold hi tags have been changed. Check the output in {output_file}.")
