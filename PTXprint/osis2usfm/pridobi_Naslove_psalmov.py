import re

def process_psalm_file(filename):
    # Regular expression to find the psalm title between the #Start_Psalm_title# and #End_Psalm_title# tags
    pattern = r"#Start_Psalm_title#(.*?)#End_Psalm_title#"
    
    with open(filename, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    
    modified_lines = []  # To store modified content
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if the line contains a verse and the tags
        if line.startswith("\\v"):
            match = re.search(pattern, line)
            if match:
                # Extract the text between the tags
                psalm_title = match.group(1).strip()

                # Prepare the \s some_text line
                s_line = f"\\s {psalm_title}\n"

                # Add the \s some_text two lines above the current line
                # First, we add the current line (without tags) to the modified_lines list
                clean_line = re.sub(pattern, '', line).strip() + "\n"

                if len(modified_lines) >= 1:
                    # Insert \s some_text one lines before the current line
                    modified_lines.insert(len(modified_lines) - 1, s_line)
                else:
                    # If there are less than 1 lines, add the \s line at the beginning
                    modified_lines.insert(0, s_line)

                # Add the cleaned-up current line without the tags
                modified_lines.append(clean_line)
            else:
                # No match, so just add the line as is
                modified_lines.append(line)
        else:
            # For non-verse lines, just add them to the modified_lines
            modified_lines.append(line)
        
        i += 1
    
    # Write the modified content back to the same file
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.writelines(modified_lines)

# Example usage
filename = "19_PSA.usfm"
process_psalm_file(filename)

# print("File processing complete.")
