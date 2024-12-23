import os
import zipfile
import shutil

# Define the ZIP file path and destination directory
zip_file = "src/Stardict-en-ua_angloukrayinskii_slovnik_miballa_engukr.zip"
unpack_dir = "temp"

# Unpack the ZIP file
try:
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(unpack_dir)
        print(f"ZIP file {zip_file} unpacked successfully to {unpack_dir}.")
except FileNotFoundError:
    print(f"Error: ZIP file {zip_file} not found.")
    exit(1)
except zipfile.BadZipFile:
    print(f"Error: {zip_file} is not a valid ZIP file.")
    exit(1)

# Define the command for pyglossary
pyglossary_command = (
    "pyglossary temp/Formats/Stardict/en-ua_angloukrayinskii_slovnik_miballa_engukr/eng-ukr_Balla_v1.3.ifo temp/out.txt --write-format=Tabfile"
)

# Run the pyglossary command
os.system(pyglossary_command)

# Define input and output files
input_file = "temp/out.txt"
full_output_file = "dictionary-full.xhtml"
filtered_output_file = "dictionary_letter_a.xhtml"

# Process the generated file and write to XHTML formats
with open(input_file, "r", encoding="utf-8") as infile, \
    open(full_output_file, "w", encoding="utf-8") as full_outfile, \
    open(filtered_output_file, "w", encoding="utf-8") as filtered_outfile:

    # Write headers for both files
    full_outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n<html xmlns:idx="http://www.mobipocket.com/idx"><body>\n')
    filtered_outfile.write('<?xml version="1.0" encoding="UTF-8"?>\n<html xmlns:idx="http://www.mobipocket.com/idx"><body>\n')

    for line in infile:
        if line.strip():
            parts = line.split('\t', 1)  # Adjust delimiter as needed
            if len(parts) == 2:
                headword, definition = parts
                entry = f'<idx:entry><idx:orth>{headword.strip()}</idx:orth><p>{definition.strip()}</p></idx:entry>\n'

                # Write to full dictionary
                full_outfile.write(entry)

                # Write to filtered dictionary if headword starts with A or earlier (lexically before 'B')
                if headword.strip().upper() < "B":
                    filtered_outfile.write(entry)

    # Write closing tags for both files
    full_outfile.write('</body></html>\n')
    filtered_outfile.write('</body></html>\n')

# Remove the temp/ directory
temp_dir = "temp"
try:
    shutil.rmtree(temp_dir)
    print(f"Temporary directory {temp_dir} and its contents deleted successfully.")
except OSError as e:
    print(f"Error deleting temporary directory {temp_dir}: {e}")
