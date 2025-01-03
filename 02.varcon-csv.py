import csv
import zipfile
import os

def extract_varcon(zip_path, extract_to):
    """
    Extract varcon.txt from the given zip file to the specified location.
    Args:
        zip_path (str): Path to the zip file containing varcon.txt.
        extract_to (str): Path where varcon.txt should be extracted.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract varcon.txt to the specified location
        zip_ref.extract("varcon.txt", path=os.path.dirname(extract_to))
        # Rename the extracted file to match the expected path
        extracted_file = os.path.join(os.path.dirname(extract_to), "varcon.txt")
        os.rename(extracted_file, extract_to)
    print(f"Extracted varcon.txt to {extract_to}")


def parse_varcon(varcon_path, output_csv_path):
    """
    Parse varcon.txt and extract British and American spelling variants into a CSV.
    British spelling comes first in the output, followed by American spelling.
    Ignore any usage information after a " | " and skip identical pairs.
    If a British spelling key already exists, it skips adding a new pair with a different American value.
    Args:
        varcon_path (str): Path to the varcon.txt file.
        output_csv_path (str): Path to the output CSV file.
    """
    british_to_american = {}  # Dictionary to track British to American spelling

    with open(varcon_path, 'r', encoding='latin-1') as file:
        for line in file:
            # Skip comments and empty lines
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Ignore usage information after "|"
            line = line.split('|')[0].strip()

            # Extract British (B or Z) and American (A) spellings
            american = None
            british = None
            parts = line.split('/')
            for part in parts:
                if ': ' not in part:
                    continue  # Skip invalid lines

                # Split only the first occurrence of ': '
                tags, word = part.split(': ', 1)
                word = word.strip()
                tags = tags.split()

                if 'A' in tags:  # American spelling
                    american = word
                if 'B' in tags or 'Z' in tags:  # British spelling
                    british = word

            # Skip identical pairs and duplicate keys
            if british and american and british != american:
                if british not in british_to_american:
                    british_to_american[british] = american

    # Write to CSV without a header
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(british_to_american.items())

    print(f"Output written to {output_csv_path}")


# Usage
if __name__ == "__main__":
    varcon_zip_path = "src/varcon.zip"  # Path to varcon.zip
    varcon_txt_path = "temp/varcon.txt"  # Temporary path for extracted varcon.txt
    output_csv_path = "csv/british_american_variants.csv"  # Output CSV file path

    # Create temp/ directory if it doesn't exist
    os.makedirs(os.path.dirname(varcon_txt_path), exist_ok=True)

    # Extract varcon.txt from zip
    extract_varcon(varcon_zip_path, varcon_txt_path)

    # Parse varcon.txt and create the CSV
    parse_varcon(varcon_txt_path, output_csv_path)

    # Cleanup: Optionally remove the temp file
    os.remove(varcon_txt_path)
    print(f"Temporary file {varcon_txt_path} removed.")