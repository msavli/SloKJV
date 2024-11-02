# Open the file and read its contents
with open('19_PSA.usfm', 'r') as file:
    lines = file.readlines()

# Process the lines
new_lines = []
for line in lines:

# If the line starts with "\qa", add "\\p\n" before it

#    if line.startswith("\\qa"):
#        new_lines.append("\\p\n" + line)
#    else:
#        new_lines.append(line)
#
#    # Add "\\p\n" after each "\qa" line except "\qa [ALEF א]"
#    if line.startswith("\\qa") and line.strip() != "\\qa [ALEF א]":
#        new_lines.append("\\p\n")

    new_lines.append(line)
    if line.startswith("\\qa") and line.strip() != "\\qa [ALEF א]":
        new_lines.append("\\p\n")

# Write the modified content back to the file
with open('19_PSA.usfm', 'w') as file:
    file.writelines(new_lines)

# print("The file has been updated successfully.")
