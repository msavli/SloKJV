import re

# Read the content of the USFM file with explicit encoding (e.g., UTF-8)
with open('19_PSA.usfm', 'r', encoding='utf-8') as file:
    usfm_content = file.read()

# Remove all tags #Start_naslov# and #Konec_naslov# and the text between them
usfm_content = re.sub(r'#Start_naslov#.*?#Konec_naslov#', '', usfm_content, flags=re.DOTALL)

# Insert \cl Psalm before \c 1, but only the first occurrence
usfm_content = usfm_content.replace('\\c 1', '\\cl Psalm\n\\c 1', 1)

# Insert \q1 after each \c xxx tag (xxx represents numbers from 1 to 150)
# Ensures proper handling of numbers from 1 to 150 and optional spaces
#  prej je bilo   usfm_content = re.sub(r'(\\c\s+\d+)', r'\1\n\\q1', usfm_content)
usfm_content = re.sub(r'(\\c\s+\d+)', r'\1\n', usfm_content)

# Save the modified USFM content back to the file with the same encoding
with open('19_PSA.usfm', 'w', encoding='utf-8') as file:
    file.write(usfm_content)

# print("Text modification completed successfully for 19_PSA.usfm.")
