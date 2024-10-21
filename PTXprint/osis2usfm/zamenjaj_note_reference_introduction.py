import re

# Open the file and read its contents
with open('SloKJV_sword.xml', 'r') as file:
    lines = file.readlines()

# Process the lines
new_lines = []
for line in lines:
    if '<div type="introduction">' in line:
        # Remove reference tags but keep the text between them
        line = re.sub(r'<reference[^>]*>(.*?)</reference>', r'\1', line)
    new_lines.append(line)

# Write the modified content back to the file
with open('SloKJV_sword.xml', 'w') as file:
    file.writelines(new_lines)

# print("The file has been updated successfully.")

