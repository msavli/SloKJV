# Read the content of the USFM file
with open('01_GEN.usfm', 'r') as file:
    usfm_content = file.read()

# Extract the text between the tags
start_tag = "#Zacetek_zaveze#"
end_tag = "#Konec_zaveze#"
start_index = usfm_content.find(start_tag) + len(start_tag)
end_index = usfm_content.find(end_tag)
extracted_text = usfm_content[start_index:end_index].strip()

# Remove the tags and the text between them from the USFM content
usfm_content_modified = usfm_content[:start_index - len(start_tag)] + usfm_content[end_index + len(end_tag):]

# Find the position of \toc3 tag
toc3_index = usfm_content_modified.find("\\toc3") + len("\\toc3")

# Insert the extracted text after \toc3 tag with additional formatting
new_content = (
    usfm_content_modified[:toc3_index] +
    # "\n\\pb\n\\mt1 " + extracted_text + "\n\\pb\n\\pb" +
    usfm_content_modified[toc3_index:]
)

# Save the modified USFM content back to the file
with open('01_GEN.usfm', 'w') as file:
    file.write(new_content)

# print("Text extraction and modification completed successfully.")


# Read the content of the USFM file
with open('41_MAT.usfm', 'r') as file:
    usfm_content = file.read()

# Extract the text between the tags
start_tag = "#Zacetek_zaveze#"
end_tag = "#Konec_zaveze#"
start_index = usfm_content.find(start_tag) + len(start_tag)
end_index = usfm_content.find(end_tag)
extracted_text = usfm_content[start_index:end_index].strip()

# Remove the tags and the text between them from the USFM content
usfm_content_modified = usfm_content[:start_index - len(start_tag)] + usfm_content[end_index + len(end_tag):]

# Find the position of \toc3 tag
toc3_index = usfm_content_modified.find("\\toc3") + len("\\toc3")

# Insert the extracted text after \toc3 tag with additional formatting
new_content = (
    usfm_content_modified[:toc3_index] +
    # "\n\\pb\n\\mt1 " + extracted_text + "\n\\pb\n\\pb" +
    usfm_content_modified[toc3_index:]
)

# Save the modified USFM content back to the file
with open('41_MAT.usfm', 'w') as file:
    file.write(new_content)
# print("Text extraction and modification completed successfully.")
