import re
import os

def remove_tags_in_file(filename):
    # Regular expression to find and remove text between the #Start_naslov# and #Konec_naslov# tags
    pattern = r" #Start_naslov#.*?#Konec_naslov#"
    
    with open(filename, 'r', encoding='utf-8') as infile:
        content = infile.read()
    
    # Remove the tags and the text between them
    modified_content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write(modified_content)

def process_usfm_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".usfm"):
            remove_tags_in_file(os.path.join(directory, filename))

# Example usage
directory = "."  # Replace with the directory containing your .usfm files
process_usfm_files(directory)

# print("All .usfm files in the directory have been processed to remove tags and text between them.")
