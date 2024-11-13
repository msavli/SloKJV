import re

# Function to modify the content between the specified tags
def modify_psalm_titles(content):
    # Define the pattern to find the content between the start and end tags
    pattern = re.compile(r'(#Start_Psalm_title#.*?#End_Psalm_title#)', re.DOTALL)
    
    # Find all matches of the pattern
    matches = pattern.findall(content)
    
    # Iterate over each match and replace \add with \it and \add* with \it*
    for match in matches:
        modified_match = match.replace('\\add', '\\bdit').replace('\\add*', '\\bdit*')
        content = content.replace(match, modified_match)
    
    return content

# Read the content of the file
with open('19_PSA.usfm', 'r') as file:
    file_content = file.read()

# Modify the content
modified_content = modify_psalm_titles(file_content)

# Write the modified content back to the file
with open('19_PSA.usfm', 'w') as file:
    file.write(modified_content)

# print("The file has been modified successfully.")
