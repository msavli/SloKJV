import re

def move_and_change_colophon_tags(text):
    # Split the text into lines for processing
    lines = text.splitlines()
    output_lines = []
    
    # Buffer for holding the colophon lines until it can be moved
    colophon_buffer = []
    in_colophon = False

    for line in lines:
        # Start capturing the colophon if it starts with <div type="colophon">
        if '<div type="colophon"' in line:
            in_colophon = True
            colophon_buffer.append(line)
            continue
        
        # If we're inside a colophon, keep buffering lines until the closing </div>
        if in_colophon:
            colophon_buffer.append(line)
            if '</div>' in line:
                in_colophon = False  # Stop capturing after closing </div>
            continue
        
        # When encountering </verse></chapter>, insert the buffered colophon if present
        if '</verse></chapter>' in line and colophon_buffer:
            # First, insert the buffered colophon lines before the </verse></chapter> line
            colophon_text = ''.join(colophon_buffer)
            colophon_text = re.sub(r'<div type="colophon"[^>]*>(.*?)</div>', r'\\cls \1', colophon_text, flags=re.DOTALL)
            output_lines.append(colophon_text)
            colophon_buffer = []  # Clear the buffer after use

        # Add the current line to the output lines
        output_lines.append(line)

    # Join the processed lines back into a single text
    return '\n'.join(output_lines)

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the function to move and change colophon lines
result = move_and_change_colophon_tags(bible_lines)

# Write the result to the output file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Colophon lines have been moved and changed. Check the output in {output_file}.")
