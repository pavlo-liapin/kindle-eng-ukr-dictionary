import csv
import os

def merge_csvs(csv_paths, merged_csv_path):
    """
    Merge multiple CSV files into a single CSV file, ensuring no duplicate variants exist across files.
    Args:
        csv_paths (list): List of paths to CSV files.
        merged_csv_path (str): Path to save the merged CSV file.
    """
    all_variants = {}
    
    for csv_path in csv_paths:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header if exists
            for row in reader:
                key = row[0]
                values = set(row[1:])
                if key not in all_variants:
                    all_variants[key] = values
                else:
                    all_variants[key].update(values)

    # Eliminate duplicates across the entire dataset
    all_used_variants = set()
    for key in all_variants:
        filtered_values = set()
        for value in all_variants[key]:
            if value not in all_used_variants:
                filtered_values.add(value)
                all_used_variants.add(value)
        all_variants[key] = filtered_values

    # Write the merged data to the new CSV file
    with open(merged_csv_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for key, values in all_variants.items():
            writer.writerow([key] + sorted(values))
    
    print(f"Merged CSV saved as: {merged_csv_path}")

def load_variants_from_csv(csv_path):
    """
    Load variants from a single CSV file into a dictionary.
    Args:
        csv_path (str): Path to the CSV file.
    Returns:
        dict: A dictionary where keys are the base words and values are lists of their variants.
    """
    variants = {}
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            key = row[0]
            values = row[1:]
            if key not in variants:
                variants[key] = values
            else:
                for value in values:
                    if value not in variants[key]:
                        variants[key].append(value)
    return variants

def process_txt_file(txt_path, variants, output_path):
    """
    Process the TXT file to add variants from the CSVs.
    Skip adding variants if they already exist in the array or as separate items in the file.
    Args:
        txt_path (str): Path to the input TXT file.
        variants (dict): Dictionary of base words and their variants.
        output_path (str): Path to the output TXT file.
    """
    all_existing_synonyms = set()

    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.strip():
                continue
            synonyms = line.split("\t")[0].split("|")
            all_existing_synonyms.update(synonyms)

    processed_lines = []

    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            if not line.strip():
                processed_lines.append(line)
                continue

            parts = line.strip().split("\t")
            synonyms = parts[0].split("|")
            existing_synonyms = set(synonyms)

            for synonym in synonyms:
                if synonym in variants:
                    for variant in variants[synonym]:
                        if variant not in existing_synonyms and variant not in all_existing_synonyms:
                            synonyms.append(variant)
                            existing_synonyms.add(variant)

            updated_synonyms = sorted(synonyms, key=lambda x: (x not in variants, synonyms.index(x)))
            updated_line = f"{'|'.join(updated_synonyms)}"
            if len(parts) > 1:
                updated_line += "\t" + "\t".join(parts[1:])
            processed_lines.append(updated_line)

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(processed_lines))

    print(f"Updated file saved as: {output_path}")

if __name__ == "__main__":
    csv_paths = ["temp/nouns-regular.csv", "temp/adjectives.csv", "temp/verbs-regular.csv"]
    merged_csv_path = "temp/all_inflections.csv"
    txt_path = "temp/08.filter-irregular-verbs.txt"
    output_path = "temp/11.all-inflections.txt"

    merge_csvs(csv_paths, merged_csv_path)
    variants = load_variants_from_csv(merged_csv_path)
    process_txt_file(txt_path, variants, output_path)