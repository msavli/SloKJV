import re
import sys
import os

def replace_cross_references(text):
    # Define the regex pattern to find <note type="crossReference"> containing one or more <reference osisRef="..."> tags
    cross_ref_pattern = r'<note type="crossReference">(.+?)</note>'
    
    # Define the regex pattern to extract <reference osisRef="..."> tags and their text inside the note
    reference_pattern = r'<reference osisRef="[^"]+">(.*?)</reference>'
    
    #x Define the regex pattern to find Jesus speaking
    #x jesus_speaking_pattern = r'<q who="Jesus" marker="">(.*?)</q>'
    
    # Define the regex pattern to extract the chapter and verse numbers from <verse osisID="...">
    verse_pattern = r'<verse osisID="[^"]+?(\d+)\.(\d+)">'
    
    # Store current chapter and verse
    current_chapter = None
    current_verse = None
    
    # Split the text into lines to process each one
    lines = text.splitlines()
    output_lines = []
    
    for line in lines:
        # Check if the line contains a <verse> tag and extract chapter and verse numbers
        verse_match = re.search(verse_pattern, line)
        if verse_match:
            current_chapter = verse_match.group(1)
            current_verse = verse_match.group(2)
        
        # Check if the line contains a cross-reference note and replace it accordingly
        #x line = replace_cross_references_in_line(line, current_chapter, current_verse, reference_pattern, jesus_speaking_pattern)
        line = replace_cross_references_in_line(line, current_chapter, current_verse, reference_pattern)
        
        output_lines.append(line)
    
    # Join the processed lines back into a single text
    return '\n'.join(output_lines)

#x def replace_cross_references_in_line(line, chapter, verse, reference_pattern, jesus_speaking_pattern):
def replace_cross_references_in_line(line, chapter, verse, reference_pattern):
    """
    Replace <note> tags containing one or more <reference> tags in the given line based on whether they appear inside
    Jesus speaking or not, and use the current chapter and verse for reference numbers.
    """
    # Define the regex pattern to find <note type="crossReference"> containing one or more <reference> tags
    cross_ref_pattern = r'<note type="crossReference">(.+?)</note>'
    
    #x Replace <note> when Jesus is speaking
    #x if re.search(jesus_speaking_pattern, line):
    #x     # Jesus is speaking: Replace with the +x format
    #x     line = re.sub(cross_ref_pattern, lambda m: replace_references(m.group(1), chapter, verse, reference_pattern, is_jesus=True), line)
    #x else:
    #x    # Jesus is not speaking: Replace with the standard x format
    #x    line = re.sub(cross_ref_pattern, lambda m: replace_references(m.group(1), chapter, verse, reference_pattern, is_jesus=False), line)
    line = re.sub(cross_ref_pattern, lambda m: replace_references(m.group(1), chapter, verse, reference_pattern), line)
    
    return line

#x def replace_references(note_content, chapter, verse, reference_pattern, is_jesus):
def replace_references(note_content, chapter, verse, reference_pattern):
    """
    Replace the <reference> tags inside a <note> tag with the appropriate format.
    """
    # Find all references inside the note
    references = re.findall(reference_pattern, note_content)
    
    # Join the references with "; " if there are multiple
    formatted_references = "; ".join(references)
    
    #x Format based on whether Jesus is speaking or not
    #x if is_jesus:
    #x    # return f"\\+x - \\xo {chapter},{verse}: \\xt {formatted_references} \\+x*"
    #x    # Umaknil sem + pri \+x ker se je PTXprint pritoževal
    #x    return f"\\x - \\xo {chapter},{verse}: \\xt {formatted_references} \\x*"
    #x else:
    #x    return f"\\x - \\xo {chapter},{verse}: \\xt {formatted_references} \\x*"
    return f"\\x - \\xo {chapter},{verse}: \\xt {formatted_references} \\x*"

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the replacement function
result = replace_cross_references(bible_lines)

# Write output to file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Replacements done. Check the output in {output_file}.")
