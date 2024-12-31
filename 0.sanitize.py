import re

def remove_curly_braces_and_unwanted_lines(file_path, output_path):
    """
    Reads a tab-separated file, removes substrings enclosed in curly braces `{}` from the first column,
    and deletes lines with keys "_about" or those starting with "##". Writes the updated content to a new file.
    Args:
        file_path (str): Path to the input file.
        output_path (str): Path to the output file.
    """
    updated_lines = []
    curly_braces_pattern = re.compile(r"\{.*?\}")

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            columns = line.strip().split('\t')
            if not columns:
                continue

            # Skip lines with "_about" or starting with "##" in the first column
            first_column = columns[0].strip()
            if first_column == "_about" or first_column.startswith("##"):
                continue

            # Remove curly braces and their content from the first column
            columns[0] = re.sub(curly_braces_pattern, '', first_column).strip()

            # Add the cleaned line to the updated lines list
            updated_lines.append('\t'.join(columns))

    # Write the updated content to the output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(updated_lines) + '\n')

    print(f"File processed and saved to {output_path}")


if __name__ == "__main__":
    input_file = "src/eng-ukr_Balla_v1.3.txt"  # Input file path
    output_file = "src/0-sanitized.txt"  # Output file path

    remove_curly_braces_and_unwanted_lines(input_file, output_file)