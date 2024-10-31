import os

# Function to process each USFM file
def process_usfm_file(file_path):
    # Read the content of the USFM file
    with open(file_path, 'r') as file:
        usfm_content = file.read()

    # Extract the text between the tags
    start_tag = "#Zacetek_Uvoda#"
    end_tag = "#Konec_Uvoda#"
    start_index = usfm_content.find(start_tag) + len(start_tag)
    end_index = usfm_content.find(end_tag)
    extracted_text = usfm_content[start_index:end_index].strip()

    # Split the extracted text by \ip tags and format it
    formatted_text = "\n".join([f"\\imi {line.strip()}" for line in extracted_text.split("\\ip") if line.strip()])

    # Remove the tags and the text between them from the USFM content
    usfm_content_modified = usfm_content[:start_index - len(start_tag)] + usfm_content[end_index + len(end_tag):]

    # Find the position of \imt1 Uvod tag
    imt1_uvod_index = usfm_content_modified.find("\\imt1 Uvod") + len("\\imt1 Uvod")

    # Insert the formatted text after \imt1 Uvod tag
    new_content = (
        usfm_content_modified[:imt1_uvod_index] +
        "\n" + formatted_text +
        usfm_content_modified[imt1_uvod_index:]
    )

    # Save the modified USFM content back to the file
    with open(file_path, 'w') as file:
        file.write(new_content)

# Process all USFM files in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.usfm'):
        process_usfm_file(filename)

# print("Text extraction and modification completed successfully for all USFM files.")
