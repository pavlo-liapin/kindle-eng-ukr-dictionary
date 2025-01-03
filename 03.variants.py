import csv

def load_variants(csv_path):
    """
    Load British-American spelling variants from the CSV file into a dictionary.
    Args:
        csv_path (str): Path to the CSV file containing spelling variants.
    Returns:
        dict: A dictionary where keys are British spellings and values are American spellings.
    """
    variants = {}
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for british, american in reader:
            variants[british] = american
            variants[american] = british
    return variants

def process_txt_file(txt_path, variants, output_path):
    """
    Process the TXT file to add vertical-tabbed spelling variants from the CSV.
    Skip adding variants if both already exist as separate items in the file.
    Args:
        txt_path (str): Path to the input TXT file.
        variants (dict): Dictionary of spelling variants.
        output_path (str): Path to the output TXT file.
    """
    # Load existing entries into a set for fast lookup
    all_existing_synonyms = set()

    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.strip():
                continue
            synonyms = line.split("\t")[0].split("|")
            all_existing_synonyms.update(synonyms)

    # Process the file line by line
    processed_lines = []

    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.strip():
                processed_lines.append(line)
                continue

            # Split the line into the synonym list and the rest of the line
            parts = line.strip().split("\t")
            synonyms = parts[0].split("|")
            existing_synonyms = set(synonyms)

            # Check and add missing spelling variants
            for synonym in synonyms:
                if synonym in variants:
                    variant = variants[synonym]
                    # Only add the variant if it doesn't already exist and is not a separate item in the file
                    if variant not in existing_synonyms and not ({synonym, variant} <= all_existing_synonyms):
                        synonyms.append(variant)
                        existing_synonyms.add(variant)

            # Rebuild the line with updated synonyms
            updated_line = f"{'|'.join(synonyms)}"
            if len(parts) > 1:
                updated_line += "\t" + "\t".join(parts[1:])
            processed_lines.append(updated_line)

    # Write the updated file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(processed_lines))

    print(f"Updated file saved as: {output_path}")


# Usage
if __name__ == "__main__":
    csv_path = "temp/british_american_variants.csv"  # Path to the CSV file
    txt_path = "temp/01.crosslinks.txt"  # Path to the input TXT file
    output_path = "temp/03.british-american-variants.txt"  # Path to the output TXT file

    # Load spelling variants
    variants = load_variants(csv_path)

    # Process the TXT file and save the output
    process_txt_file(txt_path, variants, output_path)