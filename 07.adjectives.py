import csv
import spacy
import pyinflect  # Ensure pyinflect is installed: pip install pyinflect

def generate_comparative_and_superlative_spacy(adjective, nlp):
    """
    Generate the comparative and superlative forms of an adjective using spaCy and pyinflect.
    Args:
        adjective (str): The base (positive) form of the adjective.
        nlp: A spaCy language model instance.
    Returns:
        tuple: (comparative, superlative) forms, or (None, None) if not applicable.
    """
    doc = nlp(adjective)

    token = doc[0]
    comparative = token._.inflect("JJR")  # Generate comparative form
    superlative = token._.inflect("JJS")  # Generate superlative form

    return comparative, superlative

def process_file(input_path, csv_output_path):
    """
    Process the input file to generate a CSV of adjectives with their comparative and superlative forms
    using spaCy and pyinflect.
    Args:
        input_path (str): Path to the input file.
        csv_output_path (str): Path to the output CSV file.
    """
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    adjective_forms = []
    seen_forms = set()  # Track seen (comparative, superlative) pairs

    # Read the input file
    with open(input_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        original_line = line.strip()
        parts = original_line.split("\t", 1)
        keys = parts[0].strip().split("|")
        second_column = parts[1] if len(parts) > 1 else ""

        # Check if the entry is an adjective
        if '<i class="p"><font color="green">adj</font></i>' in second_column:
            for adjective in keys:
                comparative, superlative = generate_comparative_and_superlative_spacy(adjective, nlp)
                if comparative and superlative:
                    # Skip if the (comparative, superlative) pair has been seen before
                    if (comparative, superlative) in seen_forms:
                        continue
                    seen_forms.add((comparative, superlative))  # Mark the pair as seen
                    adjective_forms.append([adjective, comparative, superlative])

    # Write the adjectives to the CSV file
    with open(csv_output_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(adjective_forms)

    print(f"Adjective forms saved to {csv_output_path}")


if __name__ == "__main__":
    input_file = "temp/05.filter-irregular-nouns.txt"  # Input file path
    csv_output_file = "csv/adjectives.csv"  # CSV output file path

    process_file(input_file, csv_output_file)