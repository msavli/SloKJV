def process_psalm_file(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    output_lines = []
    for line in lines:
        output_lines.append(line)
        if line.startswith('\\qa') and not line.startswith('\\qa [ALEF א]'):
            output_lines.append('\\p\n')

    with open(input_file, 'w') as file:
        file.writelines(output_lines)

# Process the file
process_psalm_file('19_PSA.usfm')

# print("The file has been processed and saved in '19_PSA.usfm'.")
