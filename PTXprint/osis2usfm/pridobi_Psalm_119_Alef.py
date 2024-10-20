import re

def process_file(input_filename, output_filename):
    # Regular expression to find and extract text between the #Zacetek_Alef# and #Konec_Alef# tags
    pattern = r"\\p #Zacetek_Alef#(.*?)#Konec_Alef#"
    
    with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Find the text between the tags
            match = re.search(pattern, line)
            if match:
                # Extract the text and move it to the line before the current one
                extracted_text = match.group(1).strip()
                line = re.sub(pattern, '', line).strip()  # Remove the tags and extracted text from the line
                
                # Write the extracted text and then the modified line
                if extracted_text:
                    outfile.write(f"{extracted_text}\n\\q1\n")
                if line:
                    outfile.write(f"{line}\n")
            else:
                # Write the line unchanged if no match is found
                if line.strip():  # Avoid writing blank lines
                    outfile.write(line)

# Example usage
input_filename = "19_PSA.usfm"
output_filename = "19_PSA_modified.usfm"
process_file(input_filename, output_filename)

# print("File processing complete. Check the output file.")
