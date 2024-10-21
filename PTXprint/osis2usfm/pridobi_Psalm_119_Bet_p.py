# Open the file and read its contents
with open('19_PSA.usfm', 'r') as file:
    lines = file.readlines()

# Process the lines
new_lines = []
for line in lines:
    new_lines.append(line)
    if line.startswith("\\qa") and line.strip() != "\\qa [ALEF א]":
        new_lines.append("\\p\n")

# Write the modified content back to the file
with open('19_PSA.usfm', 'w') as file:
    file.writelines(new_lines)

# print("The file has been updated successfully.")
