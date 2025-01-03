import re
import zipfile
import os

def extract_file_from_zip(zip_path, extract_to):
    """
    Extract a specific file from a zip archive.
    Args:
        zip_path (str): Path to the zip file.
        extract_to (str): Path to extract the file.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract eng-ukr_Balla_v1.3.txt
        zip_ref.extract("eng-ukr_Balla_v1.3.txt", path=os.path.dirname(extract_to))
        extracted_file = os.path.join(os.path.dirname(extract_to), "eng-ukr_Balla_v1.3.txt")
        os.rename(extracted_file, extract_to)
    print(f"Extracted to {extract_to}")

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

    print("\033[1;35mStage 1: Remove redundant metadata\033[0m")
    print(f"File processed and saved to {output_path}")


if __name__ == "__main__":
    zip_path = "src/eng-ukr_Balla_v1.3.zip"  # Path to the zip file
    temp_file = "temp/eng-ukr_Balla_v1.3.txt"  # Path to extract and use the file
    output_file = "temp/00.sanitize.txt"  # Output file path

    # Ensure the temp/ directory exists
    os.makedirs(os.path.dirname(temp_file), exist_ok=True)

    # Extract the file from the zip archive
    extract_file_from_zip(zip_path, temp_file)

    # Process the extracted file
    remove_curly_braces_and_unwanted_lines(temp_file, output_file)

    # Cleanup: Optionally remove the extracted file
    os.remove(temp_file)
    print(f"Temporary file {temp_file} removed.")