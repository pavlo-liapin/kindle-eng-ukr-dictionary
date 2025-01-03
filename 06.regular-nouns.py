import inflect
import csv

# Initialize the inflect engine
p = inflect.engine()

def load_irregular_nouns(irregular_csv_path):
    """
    Load irregular nouns from a CSV file into a set.
    Args:
        irregular_csv_path (str): Path to the irregular nouns CSV file.
    Returns:
        set: A set of all singular and plural forms of irregular nouns.
    """
    irregular_nouns = set()
    with open(irregular_csv_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            irregular_nouns.update(row)  # Add all singular and plural forms
    return irregular_nouns

def generate_plural(singular):
    """
    Generate the plural form of an English noun using the inflect library.
    Args:
        singular (str): The singular noun.
    Returns:
        str: The plural form.
    """
    return p.plural(singular)

def is_plural(word):
    """
    Check if a word is plural using the inflect library.
    Args:
        word (str): The word to check.
    Returns:
        bool: True if the word is plural, False otherwise.
    """
    return p.singular_noun(word) is not False

def process_file(input_path, irregular_csv_path, csv_output_path):
    """
    Process the input file to generate regular plural forms for nouns,
    excluding those found in the irregular nouns list, and write the singular
    and plural forms into a CSV file.
    Args:
        input_path (str): Path to the input file (src/3-inflected.txt).
        irregular_csv_path (str): Path to the irregular nouns CSV file.
        csv_output_path (str): Path to the output CSV file (temp/nouns-regular.csv).
    """
    # Load irregular nouns
    irregular_nouns = load_irregular_nouns(irregular_csv_path)
    regular_nouns = []

    # Read the input file
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Parse existing entries to detect duplicates globally
    existing_entries = set()
    global_plural_forms = set()  # Track plural forms added globally
    for line in lines:
        key = line.split("\t", 1)[0].strip()  # Extract the key
        for part in key.split("|"):
            existing_entries.add(part)

    for line in lines:
        original_line = line.strip()
        parts = original_line.split("\t", 1)
        keys = parts[0].strip().split("|")
        second_column = parts[1] if len(parts) > 1 else ""

        # Check if the entry is a noun
        if '<i class="p"><font color="green">n</font></i>' in second_column:
            for singular in keys:
                # Skip if the input word is already plural
                if is_plural(singular):
                    continue
                
                if singular in irregular_nouns:
                    continue  # Skip irregular nouns
                
                plural = generate_plural(singular)
                
                # Skip if plural or singular forms are in the irregular nouns list
                if plural in irregular_nouns:
                    continue
                
                # Add the plural if it's not already in the key array, the document, or globally
                if plural not in existing_entries and plural not in global_plural_forms:
                    regular_nouns.append([singular, plural])
                    global_plural_forms.add(plural)  # Mark plural as used globally

    # Write the regular nouns to the CSV file
    with open(csv_output_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(regular_nouns)

    print(f"Processed regular nouns saved to {csv_output_path}")


if __name__ == "__main__":
    input_file = "temp/05.filter-irregular-nouns.txt"  # Input file path
    irregular_csv_path = "temp/nouns-irregular.csv"  # Irregular nouns CSV file path
    csv_output_file = "temp/nouns-regular.csv"  # CSV output file path

    process_file(input_file, irregular_csv_path, csv_output_file)