import os

# Function to process each USFM file
def process_usfm_file(file_path):
    # Read the content of the USFM file
    with open(file_path, 'r') as file:
        usfm_content = file.read()

    # Extract the text between the tags
    start_tag = "#Zacetek_knjige#"
    end_tag = "#Konec_knjige#"
    start_index = usfm_content.find(start_tag) + len(start_tag)
    end_index = usfm_content.find(end_tag)
    extracted_text = usfm_content[start_index:end_index].strip()

    # Remove the tags and the text between them from the USFM content
    usfm_content_modified = usfm_content[:start_index - len(start_tag)] + usfm_content[end_index + len(end_tag):]

    # Find the positions of \h1, \toc1, and \mt2 tags
    h1_index = usfm_content_modified.find("\\h1") + len("\\h1")
    toc1_index = usfm_content_modified.find("\\toc1") + len("\\toc1")
    mt2_index = usfm_content_modified.find("\\mt2") + len("\\mt2")

    # Insert the extracted text after \h1 and \toc1 tags with additional formatting
    new_content = (
        usfm_content_modified[:h1_index] +
        " " + extracted_text +
        usfm_content_modified[h1_index:toc1_index] +
        " " + extracted_text +
        usfm_content_modified[toc1_index:mt2_index] +
        " " + extracted_text +
        "\n\\imt1 Uvod" +
        usfm_content_modified[mt2_index:]
    )

    # Save the modified USFM content back to the file
    with open(file_path, 'w') as file:
        file.write(new_content)

# Process all USFM files in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.usfm'):
        process_usfm_file(filename)

# print("Text extraction and modification completed successfully for all USFM files.")
