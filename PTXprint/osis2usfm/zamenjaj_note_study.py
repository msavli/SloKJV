import re
import sys
import os

def replace_notes(text):
    # Define the regex pattern to find <note type="study">some text</note>
    note_pattern = r'<note type="study">(.*?)</note>'
    
    #x Define the regex pattern to find Jesus speaking
    #x jesus_speaking_pattern = r'<q who="Jesus" marker="">(.*?)</q>'
    
    # Define the regex pattern to extract the chapter and verse numbers from <verse osisID="Matt.4.7">
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
        
        # Check if the line contains a note and replace it accordingly
        line = replace_notes_in_line(line, current_chapter, current_verse)
        
        output_lines.append(line)
    
    # Join the processed lines back into a single text
    return '\n'.join(output_lines)

def replace_notes_in_line(line, chapter, verse):
    """
    Replace <note> tags in the given line based on whether they appear inside Jesus speaking or not,
    and use the current chapter and verse for reference numbers.
    """
    # Define the regex pattern to find <note type="study">some text</note>
    note_pattern = r'<note type="study">(.*?)</note>'
    
    #x Define the regex pattern to find Jesus speaking
    #x jesus_speaking_pattern = r'<q who="Jesus" marker="">(.*?)</q>'
    
    #x Replace <note> when Jesus is speaking
    #x if re.search(jesus_speaking_pattern, line):
    #x    # Jesus is speaking: Replace with the +f format
    #x    line = re.sub(note_pattern, lambda m: f"\\+f + \\fr {chapter},{verse}: \\+ft {m.group(1)}\\f*", line)
    #xelse:
    #x    # Jesus is not speaking: Replace with the standard f format
    line = re.sub(note_pattern, lambda m: f"\\f + \\fr {chapter},{verse}: \\ft {m.group(1)}\\f*", line)
    
    return line

# Read input from file
input_file = 'SloKJV_sword.xml'
with open(input_file, 'r') as file:
    bible_lines = file.read()

# Apply the replacement function
result = replace_notes(bible_lines)

# Write output to file
output_file = 'SloKJV_sword1.xml'
with open(output_file, 'w') as file:
    file.write(result)

# print(f"Replacements done. Check the output in {output_file}.")
