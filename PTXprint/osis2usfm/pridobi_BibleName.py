# Read the content of the USFM file
with open('01_GEN.usfm', 'r') as file:
    usfm_content = file.read()

# Extract the text between the tags
start_tag = "#Zacetek_Ime_Biblije#"
end_tag = "#Konec_ime_Biblije#"
start_index = usfm_content.find(start_tag) + len(start_tag)
end_index = usfm_content.find(end_tag)
extracted_text = usfm_content[start_index:end_index].strip()

# Save the extracted text to 00_BibleName.txt
with open('00_BibleName.txt', 'w') as output_file:
    output_file.write(extracted_text)

# Remove the tags and the text between them from the USFM content
usfm_content_modified = usfm_content[:start_index - len(start_tag)] + usfm_content[end_index + len(end_tag):]

# Save the modified USFM content back to the file
with open('01_GEN.usfm', 'w') as file:
    file.write(usfm_content_modified)
