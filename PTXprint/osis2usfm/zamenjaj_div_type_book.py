import re

def change_book_div(text):
    # Define the regex pattern to find <div type="book" osisID="Gen">
    pattern = r'<div type="book" osisID="[^"]+">'
    
    # Replace the pattern with <div type="book">
    text = re.sub(pattern, r'<div type="book">', text)
    
    return text

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the function to change book div tags
result = change_book_div(bible_lines)

# Write the result to the output file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Book div tags have been changed. Check the output in {output_file}.")
